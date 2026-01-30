/**
 * Keyboard module bindings
 */

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <SDL.h>
#include <map>
#include <string>

#include "love2d_common.h"

namespace py = pybind11;

// Key constant mapping
static std::map<std::string, SDL_Keycode> key_map = {
    {"a", SDLK_a}, {"b", SDLK_b}, {"c", SDLK_c}, {"d", SDLK_d},
    {"e", SDLK_e}, {"f", SDLK_f}, {"g", SDLK_g}, {"h", SDLK_h},
    {"i", SDLK_i}, {"j", SDLK_j}, {"k", SDLK_k}, {"l", SDLK_l},
    {"m", SDLK_m}, {"n", SDLK_n}, {"o", SDLK_o}, {"p", SDLK_p},
    {"q", SDLK_q}, {"r", SDLK_r}, {"s", SDLK_s}, {"t", SDLK_t},
    {"u", SDLK_u}, {"v", SDLK_v}, {"w", SDLK_w}, {"x", SDLK_x},
    {"y", SDLK_y}, {"z", SDLK_z},
    {"0", SDLK_0}, {"1", SDLK_1}, {"2", SDLK_2}, {"3", SDLK_3},
    {"4", SDLK_4}, {"5", SDLK_5}, {"6", SDLK_6}, {"7", SDLK_7},
    {"8", SDLK_8}, {"9", SDLK_9},
    {"return", SDLK_RETURN}, {"escape", SDLK_ESCAPE}, {"backspace", SDLK_BACKSPACE},
    {"tab", SDLK_TAB}, {"space", SDLK_SPACE}, {"-", SDLK_MINUS},
    {"equals", SDLK_EQUALS}, {"[", SDLK_LEFTBRACKET}, {"]", SDLK_RIGHTBRACKET},
    {"\\", SDLK_BACKSLASH}, {";", SDLK_SEMICOLON}, {"'", SDLK_QUOTE},
    {",", SDLK_COMMA}, {".", SDLK_PERIOD}, {"/", SDLK_SLASH},
    {"f1", SDLK_F1}, {"f2", SDLK_F2}, {"f3", SDLK_F3}, {"f4", SDLK_F4},
    {"f5", SDLK_F5}, {"f6", SDLK_F6}, {"f7", SDLK_F7}, {"f8", SDLK_F8},
    {"f9", SDLK_F9}, {"f10", SDLK_F10}, {"f11", SDLK_F11}, {"f12", SDLK_F12},
    {"pause", SDLK_PAUSE}, {"insert", SDLK_INSERT}, {"home", SDLK_HOME},
    {"pageup", SDLK_PAGEUP}, {"delete", SDLK_DELETE}, {"end", SDLK_END},
    {"pagedown", SDLK_PAGEDOWN}, {"right", SDLK_RIGHT}, {"left", SDLK_LEFT},
    {"down", SDLK_DOWN}, {"up", SDLK_UP},
    {"lctrl", SDLK_LCTRL}, {"rctrl", SDLK_RCTRL},
    {"lshift", SDLK_LSHIFT}, {"rshift", SDLK_RSHIFT},
    {"lalt", SDLK_LALT}, {"ralt", SDLK_RALT},
    {"lgui", SDLK_LGUI}, {"rgui", SDLK_RGUI},
};

bool keyboard_isDown(py::args keys) {
    const Uint8* state = SDL_GetKeyboardState(nullptr);
    
    for (auto key : keys) {
        std::string key_str = key.cast<std::string>();
        auto it = key_map.find(key_str);
        if (it != key_map.end()) {
            SDL_Scancode scancode = SDL_GetScancodeFromKey(it->second);
            if (state[scancode]) {
                return true;
            }
        }
    }
    
    return false;
}

bool keyboard_isScancodeDown(const std::string& scancode) {
    const Uint8* state = SDL_GetKeyboardState(nullptr);
    SDL_Scancode code = SDL_GetScancodeFromName(scancode.c_str());
    if (code != SDL_SCANCODE_UNKNOWN) {
        return state[code];
    }
    return false;
}

void keyboard_setKeyRepeat(bool enable) {
    // SDL 2.0 doesn't support key repeat enable/disable per se
    // Key repeat is always on in SDL2
}

bool keyboard_hasKeyRepeat() {
    // SDL doesn't provide a direct way to check this
    return true;
}

void keyboard_setTextInput(bool enable) {
    if (enable) {
        SDL_StartTextInput();
    } else {
        SDL_StopTextInput();
    }
}

bool keyboard_hasTextInput() {
    return SDL_IsTextInputActive() == SDL_TRUE;
}

bool keyboard_hasScreenKeyboard() {
    return SDL_HasScreenKeyboardSupport() == SDL_TRUE;
}

void init_keyboard(py::module_ &m) {
    m.doc() = "Keyboard input functions";
    
    m.def("isDown", &keyboard_isDown, "Check if key(s) are pressed");
    m.def("isScancodeDown", &keyboard_isScancodeDown, "Check if scancode is pressed",
          py::arg("scancode"));
    m.def("setKeyRepeat", &keyboard_setKeyRepeat, "Enable/disable key repeat",
          py::arg("enable"));
    m.def("hasKeyRepeat", &keyboard_hasKeyRepeat, "Check if key repeat is enabled");
    m.def("setTextInput", &keyboard_setTextInput, "Enable/disable text input",
          py::arg("enable"));
    m.def("hasTextInput", &keyboard_hasTextInput, "Check if text input is active");
    m.def("hasScreenKeyboard", &keyboard_hasScreenKeyboard, "Check if screen keyboard is available");
    
}
