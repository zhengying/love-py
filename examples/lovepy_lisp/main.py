import os
import sys
from typing import List

import love


_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_SIMPLELISP_DIR = os.path.join(_BASE_DIR, "libs", "simplelisp")
if _SIMPLELISP_DIR not in sys.path:
    sys.path.insert(0, _SIMPLELISP_DIR)

from eval import EvalError, lisp_eval
from lexer import LexerError
from lisp_types import LispList, LispString, is_void
from parser import ParseError, parse
from primitives import create_global_env, set_load_function


_env = None
_font = None
_output_lines: List[str] = []
_history: List[str] = []
_history_index: int = 0
_history_saved_line: str = ""
_buffer: str = ""
_current_line: str = ""
_cursor_pos: int = 0
_cursor_x_px: float = 0.0
_cursor_dirty: bool = True
_scroll_offset: int = 0
_char_advances: List[float] = []


def _clamp(n: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, n))


def _mark_cursor_dirty() -> None:
    global _cursor_dirty
    _cursor_dirty = True


def _prepare_font_advances() -> None:
    global _char_advances, _font
    if _font is None:
        _char_advances = [0.0] * 128
        return

    advances = [0.0] * 128
    for i in range(128):
        ch = chr(i)
        if ch == "\x00":
            continue
        try:
            advances[i] = float(_font.getWidth(ch))
        except Exception:
            advances[i] = 0.0

    if advances[ord(" ")] == 0.0:
        advances[ord(" ")] = advances[ord("a")] * 0.5

    _char_advances = advances


def _text_advance(text: str) -> float:
    global _char_advances, _font
    if not _char_advances:
        try:
            return float(_font.getWidth(text))
        except Exception:
            return 0.0

    total = 0.0
    for ch in text:
        o = ord(ch)
        if 0 <= o < 128:
            total += _char_advances[o]
    return total


def _recompute_cursor_x(prompt_prefix: str, margin: int) -> None:
    global _cursor_x_px, _cursor_dirty, _font
    left_text = prompt_prefix + _current_line[:_cursor_pos]
    _cursor_x_px = float(margin) + _text_advance(left_text)
    _cursor_dirty = False


def _wrap_line(line: str, max_chars: int) -> List[str]:
    if max_chars <= 0:
        return [line]
    if len(line) <= max_chars:
        return [line]
    out = []
    start = 0
    while start < len(line):
        out.append(line[start : start + max_chars])
        start += max_chars
    return out


def _estimated_max_chars() -> int:
    global _font
    if _font is None:
        return 120
    w, _h = love.graphics.getDimensions()
    margin = 12
    try:
        char_w = max(1, int(_font.getWidth("M")))
    except Exception:
        char_w = 8
    usable = max(10, int(w) - margin * 2)
    return max(10, usable // char_w)


def _append_output(text: str) -> None:
    global _output_lines, _scroll_offset
    max_chars = _estimated_max_chars()
    for raw_line in str(text).splitlines() or [""]:
        for part in _wrap_line(raw_line, max_chars):
            _output_lines.append(part)
    if len(_output_lines) > 2000:
        _output_lines = _output_lines[-2000:]
    _scroll_offset = 0


def _load_startup() -> None:
    startup_path = os.path.join(_SIMPLELISP_DIR, "startup.scm")
    if not os.path.exists(startup_path):
        return
    _load_file(startup_path)


def _load_file(filepath: str) -> None:
    global _env
    if _env is None:
        return
    if not os.path.exists(filepath):
        _append_output(f"Error: File not found: {filepath}")
        return
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
        exprs = parse(source)
        for expr in exprs:
            lisp_eval(expr, _env)
    except (LexerError, ParseError, EvalError, OSError, UnicodeError) as e:
        _append_output(f"Error in {filepath}: {e}")


def _install_load_primitive() -> None:
    global _env

    def do_load(path: str) -> None:
        if not os.path.isabs(path):
            path = os.path.join(os.getcwd(), path)
        _load_file(path)

    set_load_function(do_load)


def _is_balanced(source: str) -> bool:
    depth = 0
    in_string = False
    escape = False
    for c in source:
        if escape:
            escape = False
            continue
        if c == "\\" and in_string:
            escape = True
            continue
        if c == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
    return depth <= 0


def _print_help() -> None:
    _append_output("SimpleLisp REPL")
    _append_output("Enter to submit. Multi-line works with unbalanced parentheses.")
    _append_output("Up/Down: history. PageUp/PageDown or wheel: scroll.")
    _append_output("Esc or (exit) to quit. (help) to show this help.")


def _maybe_quit_from_command(line: str) -> bool:
    stripped = line.strip().lower()
    if stripped in {"(exit)", "exit", "quit", "(quit)"}:
        love.event.quit()
        return True
    return False


def _maybe_help_from_command(line: str) -> bool:
    stripped = line.strip().lower()
    if stripped in {"(help)", "help"}:
        _print_help()
        return True
    return False


def _echo_multiline_source(source: str) -> None:
    lines = source.splitlines()
    for i, line in enumerate(lines):
        prefix = "> " if i == 0 else "  "
        _append_output(prefix + line)


def _evaluate_buffer() -> None:
    global _buffer, _env
    if _env is None:
        return
    try:
        _echo_multiline_source(_buffer)
        exprs = parse(_buffer)
        for expr in exprs:
            result = lisp_eval(expr, _env)
            if not is_void(result):
                _append_output(repr(result))
    except (LexerError, ParseError) as e:
        _append_output(f"Syntax error: {e}")
    except EvalError as e:
        _append_output(f"Evaluation error: {e}")
    except NameError as e:
        _append_output(f"Name error: {e}")
    except TypeError as e:
        _append_output(f"Type error: {e}")
    except ValueError as e:
        _append_output(f"Value error: {e}")
    except Exception as e:
        _append_output(f"Error: {e}")
    finally:
        _buffer = ""
        _mark_cursor_dirty()


def _submit_current_line() -> None:
    global _buffer, _current_line, _cursor_pos, _history, _history_index, _history_saved_line

    line = _current_line

    if _buffer == "":
        stripped = line.strip().lower()
        if stripped in {"(exit)", "exit", "quit", "(quit)"}:
            _append_output("> " + line)
            love.event.quit()
            return
        if stripped in {"(help)", "help"}:
            _append_output("> " + line)
            _print_help()
            _current_line = ""
            _cursor_pos = 0
            _history_index = len(_history)
            _history_saved_line = ""
            return

    if line.strip() != "":
        _history.append(line)
        if len(_history) > 200:
            _history = _history[-200:]
    _history_index = len(_history)
    _history_saved_line = ""

    _buffer += line + "\n"
    _current_line = ""
    _cursor_pos = 0
    _mark_cursor_dirty()

    if _is_balanced(_buffer):
        _evaluate_buffer()


def _history_move(delta: int) -> None:
    global _history_index, _current_line, _cursor_pos, _history_saved_line
    if not _history:
        return
    if _history_index == len(_history):
        _history_saved_line = _current_line
    _history_index = _clamp(_history_index + delta, 0, len(_history))
    if _history_index == len(_history):
        _current_line = _history_saved_line
    else:
        _current_line = _history[_history_index]
    _cursor_pos = len(_current_line)
    _mark_cursor_dirty()


def _scroll(delta_lines: int) -> None:
    global _scroll_offset
    max_off = max(0, len(_output_lines) - 1)
    _scroll_offset = _clamp(_scroll_offset + delta_lines, 0, max_off)


def love_conf(t):
    t["window"]["title"] = "SimpleLisp REPL (Python)"
    t["window"]["width"] = 960
    t["window"]["height"] = 720
    t["window"]["resizable"] = True
    t["window"]["vsync"] = True


def love_load():
    global _env, _font, _history_index, _cursor_pos

    try:
        font_path = os.path.abspath(os.path.join(_BASE_DIR, "..", "font", "ubuntu-mono.ttf"))
        if love.filesystem.exists(font_path):
            _font = love.graphics.newFont(font_path, 16)
            love.graphics.setFont(_font)
    except Exception:
        _font = None

    if _font is None:
        _font = love.graphics.getFont()
        love.graphics.setFont(_font)

    _prepare_font_advances()

    love.graphics.setBackgroundColor(0.06, 0.06, 0.08)

    _env = create_global_env()
    _install_load_primitive()
    _env.define("*command-line-args*", LispList([]))
    _load_startup()

    _append_output("SimpleLisp - Simply Scheme Interpreter")
    _append_output("Type (help) for help, (exit) to quit.")
    _history_index = 0
    _cursor_pos = 0
    _mark_cursor_dirty()


def love_update(dt):
    pass


def love_draw():
    global _font
    love.graphics.clear()

    if _font is None:
        _font = love.graphics.getFont()
        love.graphics.setFont(_font)

    w, h = love.graphics.getDimensions()
    margin = 12
    line_h = int(_font.getHeight()) + 2
    visible = max(2, (int(h) - margin * 2) // max(1, line_h))

    buffer_lines = _buffer.splitlines()
    input_lines = buffer_lines + [_current_line]
    max_input_lines = min(len(input_lines), max(1, min(10, visible - 1)))
    output_lines_visible = max(1, visible - max_input_lines)

    start = max(0, len(_output_lines) - output_lines_visible - _scroll_offset)
    end = min(len(_output_lines), start + output_lines_visible)
    y = margin

    love.graphics.setColor(0.92, 0.92, 0.92)
    for line in _output_lines[start:end]:
        love.graphics.print(line, margin, y)
        y += line_h

    input_start = max(0, len(input_lines) - max_input_lines)
    prompt_y = margin + output_lines_visible * line_h
    prompt_prefix = "> "
    for i in range(input_start, len(input_lines)):
        prompt_prefix = "> " if i == 0 else "  "
        love.graphics.setColor(0.75, 0.85, 1.0)
        love.graphics.print(prompt_prefix + input_lines[i], margin, prompt_y)
        prompt_y += line_h

    cursor_y = margin + output_lines_visible * line_h + (len(input_lines) - 1 - input_start) * line_h

    if _cursor_dirty:
        _recompute_cursor_x(prompt_prefix, margin)

    cursor_on = int(love.timer.getTime() * 2) % 2 == 0
    cursor_alpha = 1.0 if cursor_on else 0.25
    love.graphics.setColor(0.75, 0.85, 1.0, cursor_alpha)
    love.graphics.rectangle(
        "fill",
        _cursor_x_px,
        cursor_y + 2,
        2,
        max(1, int(_font.getHeight()) - 2),
    )


def love_textinput(text: str):
    global _current_line, _cursor_pos
    if not text:
        return
    if _cursor_pos == len(_current_line):
        _current_line += text
    else:
        _current_line = _current_line[:_cursor_pos] + text + _current_line[_cursor_pos:]
    _cursor_pos += len(text)
    _mark_cursor_dirty()


def love_keypressed(key, scancode, isrepeat):
    global _current_line, _cursor_pos

    k = str(key).lower().replace(" ", "").replace("_", "")

    if k == "escape":
        love.event.quit()
        return

    if k in {"return", "enter", "kpenter"}:
        _submit_current_line()
        return

    if k == "space":
        love_textinput(" ")
        return

    if k == "backspace":
        if _cursor_pos > 0:
            _current_line = _current_line[: _cursor_pos - 1] + _current_line[_cursor_pos:]
            _cursor_pos -= 1
            _mark_cursor_dirty()
        return

    if k == "delete":
        if _cursor_pos < len(_current_line):
            _current_line = _current_line[:_cursor_pos] + _current_line[_cursor_pos + 1 :]
            _mark_cursor_dirty()
        return

    if k == "left":
        _cursor_pos = max(0, _cursor_pos - 1)
        _mark_cursor_dirty()
        return

    if k == "right":
        _cursor_pos = min(len(_current_line), _cursor_pos + 1)
        _mark_cursor_dirty()
        return

    if k == "home":
        _cursor_pos = 0
        _mark_cursor_dirty()
        return

    if k == "end":
        _cursor_pos = len(_current_line)
        _mark_cursor_dirty()
        return

    if k == "up":
        _history_move(-1)
        return

    if k == "down":
        _history_move(1)
        return

    if k == "pageup":
        _scroll(10)
        return

    if k == "pagedown":
        _scroll(-10)
        return

    if k == "tab":
        love_textinput("  ")
        return


def love_wheelmoved(x, y):
    if y > 0:
        _scroll(3)
    elif y < 0:
        _scroll(-3)


def love_quit():
    pass
