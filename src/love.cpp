/**
 * LOVE2D for Python - Main Executable
 * 
 * This is the C++ entry point (like original love.exe).
 * It creates the love module using Python C API and runs the main game loop.
 * 
 * Usage: ./love game.py
 */

#include <Python.h>
#include <SDL.h>
#include <OpenGL/gl.h>
#include <iostream>
#include <string>
#include <cstring>
#include <cmath>

// Global state for the game
struct GameState {
    bool running = false;
    bool initialized = false;
    SDL_Window* window = nullptr;
    SDL_GLContext gl_context = nullptr;
    int width = 800;
    int height = 600;
    std::string title = "LOVE2D Python";
    
    // Graphics state
    float color_r = 1.0f, color_g = 1.0f, color_b = 1.0f, color_a = 1.0f;
    float bg_r = 0.0f, bg_g = 0.0f, bg_b = 0.0f, bg_a = 1.0f;
    
    // Python callbacks
    PyObject* py_load = nullptr;
    PyObject* py_update = nullptr;
    PyObject* py_draw = nullptr;
    PyObject* py_quit = nullptr;
    PyObject* py_keypressed = nullptr;
    PyObject* py_keyreleased = nullptr;
    PyObject* py_mousepressed = nullptr;
    PyObject* py_mousereleased = nullptr;
    PyObject* py_mousemoved = nullptr;
};

static GameState g_state;

// ============================================================================
// Graphics Module Functions (exposed to Python)
// ============================================================================

static PyObject* graphics_clear(PyObject* self, PyObject* args) {
    float r = 0.0f, g = 0.0f, b = 0.0f, a = 1.0f;
    PyArg_ParseTuple(args, "|ffff", &r, &g, &b, &a);
    glClearColor(r, g, b, a);
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    Py_RETURN_NONE;
}

static PyObject* graphics_setColor(PyObject* self, PyObject* args) {
    float r, g, b, a = 1.0f;
    if (!PyArg_ParseTuple(args, "fff|f", &r, &g, &b, &a))
        return nullptr;
    g_state.color_r = r;
    g_state.color_g = g;
    g_state.color_b = b;
    g_state.color_a = a;
    glColor4f(r, g, b, a);
    Py_RETURN_NONE;
}

static PyObject* graphics_getColor(PyObject* self, PyObject* args) {
    return Py_BuildValue("(ffff)", g_state.color_r, g_state.color_g, g_state.color_b, g_state.color_a);
}

static PyObject* graphics_setBackgroundColor(PyObject* self, PyObject* args) {
    float r, g, b, a = 1.0f;
    if (!PyArg_ParseTuple(args, "fff|f", &r, &g, &b, &a))
        return nullptr;
    g_state.bg_r = r;
    g_state.bg_g = g;
    g_state.bg_b = b;
    g_state.bg_a = a;
    Py_RETURN_NONE;
}

static PyObject* graphics_getBackgroundColor(PyObject* self, PyObject* args) {
    return Py_BuildValue("(ffff)", g_state.bg_r, g_state.bg_g, g_state.bg_b, g_state.bg_a);
}

static PyObject* graphics_rectangle(PyObject* self, PyObject* args) {
    const char* mode;
    float x, y, width, height;
    if (!PyArg_ParseTuple(args, "sffff", &mode, &x, &y, &width, &height))
        return nullptr;
    
    GLenum draw_mode = (strcmp(mode, "fill") == 0) ? GL_QUADS : GL_LINE_LOOP;
    
    glBegin(draw_mode);
    glVertex2f(x, y);
    glVertex2f(x + width, y);
    glVertex2f(x + width, y + height);
    glVertex2f(x, y + height);
    glEnd();
    
    Py_RETURN_NONE;
}

static PyObject* graphics_circle(PyObject* self, PyObject* args) {
    const char* mode;
    float x, y, radius;
    if (!PyArg_ParseTuple(args, "sfff", &mode, &x, &y, &radius))
        return nullptr;
    
    const int segments = 32;
    GLenum draw_mode = (strcmp(mode, "fill") == 0) ? GL_TRIANGLE_FAN : GL_LINE_LOOP;
    
    glBegin(draw_mode);
    for (int i = 0; i < segments; i++) {
        float angle = 2.0f * 3.14159f * i / segments;
        glVertex2f(x + radius * cosf(angle), y + radius * sinf(angle));
    }
    glEnd();
    
    Py_RETURN_NONE;
}

static PyObject* graphics_line(PyObject* self, PyObject* args) {
    float x1, y1, x2, y2;
    if (!PyArg_ParseTuple(args, "ffff", &x1, &y1, &x2, &y2))
        return nullptr;
    
    glBegin(GL_LINES);
    glVertex2f(x1, y1);
    glVertex2f(x2, y2);
    glEnd();
    
    Py_RETURN_NONE;
}

static PyObject* graphics_push(PyObject* self, PyObject* args) {
    glPushMatrix();
    Py_RETURN_NONE;
}

static PyObject* graphics_pop(PyObject* self, PyObject* args) {
    glPopMatrix();
    Py_RETURN_NONE;
}

static PyObject* graphics_origin(PyObject* self, PyObject* args) {
    glLoadIdentity();
    Py_RETURN_NONE;
}

static PyObject* graphics_translate(PyObject* self, PyObject* args) {
    float dx, dy;
    if (!PyArg_ParseTuple(args, "ff", &dx, &dy))
        return nullptr;
    glTranslatef(dx, dy, 0.0f);
    Py_RETURN_NONE;
}

static PyObject* graphics_rotate(PyObject* self, PyObject* args) {
    float angle;
    if (!PyArg_ParseTuple(args, "f", &angle))
        return nullptr;
    glRotatef(angle * 180.0f / 3.14159f, 0.0f, 0.0f, 1.0f);
    Py_RETURN_NONE;
}

static PyObject* graphics_scale(PyObject* self, PyObject* args) {
    float sx, sy;
    if (!PyArg_ParseTuple(args, "ff", &sx, &sy))
        return nullptr;
    glScalef(sx, sy, 1.0f);
    Py_RETURN_NONE;
}

static PyObject* graphics_getWidth(PyObject* self, PyObject* args) {
    return PyLong_FromLong(g_state.width);
}

static PyObject* graphics_getHeight(PyObject* self, PyObject* args) {
    return PyLong_FromLong(g_state.height);
}

static PyObject* graphics_getDimensions(PyObject* self, PyObject* args) {
    return Py_BuildValue("(ii)", g_state.width, g_state.height);
}

// Graphics module method table
static PyMethodDef GraphicsMethods[] = {
    {"clear", graphics_clear, METH_VARARGS, "Clear the screen (r, g, b, a)"},
    {"setColor", graphics_setColor, METH_VARARGS, "Set drawing color (r, g, b, a)"},
    {"getColor", graphics_getColor, METH_NOARGS, "Get current drawing color"},
    {"setBackgroundColor", graphics_setBackgroundColor, METH_VARARGS, "Set background color (r, g, b, a)"},
    {"getBackgroundColor", graphics_getBackgroundColor, METH_NOARGS, "Get background color"},
    {"rectangle", graphics_rectangle, METH_VARARGS, "Draw rectangle (mode, x, y, width, height)"},
    {"circle", graphics_circle, METH_VARARGS, "Draw circle (mode, x, y, radius)"},
    {"line", graphics_line, METH_VARARGS, "Draw line (x1, y1, x2, y2)"},
    {"push", graphics_push, METH_NOARGS, "Save transformation state"},
    {"pop", graphics_pop, METH_NOARGS, "Restore transformation state"},
    {"origin", graphics_origin, METH_NOARGS, "Reset transformation"},
    {"translate", graphics_translate, METH_VARARGS, "Translate (dx, dy)"},
    {"rotate", graphics_rotate, METH_VARARGS, "Rotate (angle in radians)"},
    {"scale", graphics_scale, METH_VARARGS, "Scale (sx, sy)"},
    {"getWidth", graphics_getWidth, METH_NOARGS, "Get screen width"},
    {"getHeight", graphics_getHeight, METH_NOARGS, "Get screen height"},
    {"getDimensions", graphics_getDimensions, METH_NOARGS, "Get screen dimensions"},
    {nullptr, nullptr, 0, nullptr}
};

// ============================================================================
// Window Module Functions
// ============================================================================

static PyObject* window_setMode(PyObject* self, PyObject* args) {
    int width, height;
    PyObject* flags = nullptr;
    if (!PyArg_ParseTuple(args, "ii|O", &width, &height, &flags))
        return nullptr;
    
    g_state.width = width;
    g_state.height = height;
    
    if (g_state.window) {
        SDL_SetWindowSize(g_state.window, width, height);
    }
    
    Py_RETURN_NONE;
}

static PyObject* window_setTitle(PyObject* self, PyObject* args) {
    const char* title;
    if (!PyArg_ParseTuple(args, "s", &title))
        return nullptr;
    
    g_state.title = title;
    if (g_state.window) {
        SDL_SetWindowTitle(g_state.window, title);
    }
    
    Py_RETURN_NONE;
}

static PyObject* window_getWidth(PyObject* self, PyObject* args) {
    return PyLong_FromLong(g_state.width);
}

static PyObject* window_getHeight(PyObject* self, PyObject* args) {
    return PyLong_FromLong(g_state.height);
}

static PyObject* window_getDimensions(PyObject* self, PyObject* args) {
    return Py_BuildValue("(ii)", g_state.width, g_state.height);
}

static PyMethodDef WindowMethods[] = {
    {"setMode", window_setMode, METH_VARARGS, "Set window mode (width, height, flags)"},
    {"setTitle", window_setTitle, METH_VARARGS, "Set window title"},
    {"getWidth", window_getWidth, METH_NOARGS, "Get window width"},
    {"getHeight", window_getHeight, METH_NOARGS, "Get window height"},
    {"getDimensions", window_getDimensions, METH_NOARGS, "Get window dimensions"},
    {nullptr, nullptr, 0, nullptr}
};

// ============================================================================
// Timer Module Functions
// ============================================================================

static PyObject* timer_getTime(PyObject* self, PyObject* args) {
    return PyFloat_FromDouble(SDL_GetTicks() / 1000.0);
}

static PyObject* timer_getDelta(PyObject* self, PyObject* args) {
    // Return a placeholder - real delta time is calculated in the main loop
    return PyFloat_FromDouble(1.0 / 60.0);
}

static PyObject* timer_getFPS(PyObject* self, PyObject* args) {
    return PyFloat_FromDouble(60.0);
}

static PyObject* timer_sleep(PyObject* self, PyObject* args) {
    float seconds;
    if (!PyArg_ParseTuple(args, "f", &seconds))
        return nullptr;
    SDL_Delay((int)(seconds * 1000));
    Py_RETURN_NONE;
}

static PyMethodDef TimerMethods[] = {
    {"getTime", timer_getTime, METH_NOARGS, "Get elapsed time in seconds"},
    {"getDelta", timer_getDelta, METH_NOARGS, "Get delta time"},
    {"getFPS", timer_getFPS, METH_NOARGS, "Get current FPS"},
    {"sleep", timer_sleep, METH_VARARGS, "Sleep for seconds"},
    {nullptr, nullptr, 0, nullptr}
};

// ============================================================================
// Keyboard Module Functions
// ============================================================================

static PyObject* keyboard_isDown(PyObject* self, PyObject* args) {
    // Check if any of the provided keys are down
    Py_ssize_t n = PyTuple_Size(args);
    const Uint8* state = SDL_GetKeyboardState(nullptr);
    
    for (Py_ssize_t i = 0; i < n; i++) {
        PyObject* item = PyTuple_GetItem(args, i);
        if (!PyUnicode_Check(item)) continue;
        
        const char* key = PyUnicode_AsUTF8(item);
        SDL_Scancode scancode = SDL_GetScancodeFromName(key);
        if (scancode != SDL_SCANCODE_UNKNOWN && state[scancode]) {
            Py_RETURN_TRUE;
        }
    }
    
    Py_RETURN_FALSE;
}

static PyMethodDef KeyboardMethods[] = {
    {"isDown", keyboard_isDown, METH_VARARGS, "Check if key(s) are down"},
    {nullptr, nullptr, 0, nullptr}
};

// ============================================================================
// Mouse Module Functions
// ============================================================================

static PyObject* mouse_getPosition(PyObject* self, PyObject* args) {
    int x, y;
    SDL_GetMouseState(&x, &y);
    return Py_BuildValue("(ii)", x, y);
}

static PyObject* mouse_getX(PyObject* self, PyObject* args) {
    int x, y;
    SDL_GetMouseState(&x, &y);
    return PyLong_FromLong(x);
}

static PyObject* mouse_getY(PyObject* self, PyObject* args) {
    int x, y;
    SDL_GetMouseState(&x, &y);
    return PyLong_FromLong(y);
}

static PyObject* mouse_isDown(PyObject* self, PyObject* args) {
    int button;
    if (!PyArg_ParseTuple(args, "i", &button))
        return nullptr;
    
    Uint32 state = SDL_GetMouseState(nullptr, nullptr);
    if (state & SDL_BUTTON(button)) {
        Py_RETURN_TRUE;
    }
    Py_RETURN_FALSE;
}

static PyMethodDef MouseMethods[] = {
    {"getPosition", mouse_getPosition, METH_NOARGS, "Get mouse position (x, y)"},
    {"getX", mouse_getX, METH_NOARGS, "Get mouse X coordinate"},
    {"getY", mouse_getY, METH_NOARGS, "Get mouse Y coordinate"},
    {"isDown", mouse_isDown, METH_VARARGS, "Check if mouse button is down (1=left, 2=middle, 3=right)"},
    {nullptr, nullptr, 0, nullptr}
};

// ============================================================================
// Event Module Functions
// ============================================================================

static PyObject* event_quit(PyObject* self, PyObject* args) {
    SDL_Event event;
    event.type = SDL_QUIT;
    SDL_PushEvent(&event);
    Py_RETURN_NONE;
}

static PyMethodDef EventMethods[] = {
    {"quit", event_quit, METH_NOARGS, "Push quit event"},
    {nullptr, nullptr, 0, nullptr}
};

// ============================================================================
// Create LOVE Module
// ============================================================================

static PyModuleDef GraphicsModule = {
    PyModuleDef_HEAD_INIT, "love.graphics", nullptr, -1, GraphicsMethods
};

static PyModuleDef WindowModule = {
    PyModuleDef_HEAD_INIT, "love.window", nullptr, -1, WindowMethods
};

static PyModuleDef TimerModule = {
    PyModuleDef_HEAD_INIT, "love.timer", nullptr, -1, TimerMethods
};

static PyModuleDef KeyboardModule = {
    PyModuleDef_HEAD_INIT, "love.keyboard", nullptr, -1, KeyboardMethods
};

static PyModuleDef MouseModule = {
    PyModuleDef_HEAD_INIT, "love.mouse", nullptr, -1, MouseMethods
};

static PyModuleDef EventModule = {
    PyModuleDef_HEAD_INIT, "love.event", nullptr, -1, EventMethods
};

// Submodules as PyObject*
static PyObject* createLoveModule() {
    // Create main love module
    static PyModuleDef LoveModule = {
        PyModuleDef_HEAD_INIT, "love", "LOVE2D Python API", -1, nullptr
    };
    
    PyObject* love = PyModule_Create(&LoveModule);
    if (!love) return nullptr;
    
    // Add submodules
    PyObject* graphics = PyModule_Create(&GraphicsModule);
    PyObject* window = PyModule_Create(&WindowModule);
    PyObject* timer = PyModule_Create(&TimerModule);
    PyObject* keyboard = PyModule_Create(&KeyboardModule);
    PyObject* mouse = PyModule_Create(&MouseModule);
    PyObject* event = PyModule_Create(&EventModule);
    
    if (graphics) PyModule_AddObject(love, "graphics", graphics);
    if (window) PyModule_AddObject(love, "window", window);
    if (timer) PyModule_AddObject(love, "timer", timer);
    if (keyboard) PyModule_AddObject(love, "keyboard", keyboard);
    if (mouse) PyModule_AddObject(love, "mouse", mouse);
    if (event) PyModule_AddObject(love, "event", event);
    
    // Add version
    PyModule_AddStringConstant(love, "__version__", "11.5.0");
    
    return love;
}

// ============================================================================
// SDL and Game Loop
// ============================================================================

bool initSDL() {
    if (SDL_Init(SDL_INIT_VIDEO | SDL_INIT_TIMER) < 0) {
        std::cerr << "SDL_Init failed: " << SDL_GetError() << std::endl;
        return false;
    }
    
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_MAJOR_VERSION, 2);
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_MINOR_VERSION, 1);
    SDL_GL_SetAttribute(SDL_GL_DOUBLEBUFFER, 1);
    SDL_GL_SetAttribute(SDL_GL_DEPTH_SIZE, 24);
    
    g_state.window = SDL_CreateWindow(
        g_state.title.c_str(),
        SDL_WINDOWPOS_CENTERED,
        SDL_WINDOWPOS_CENTERED,
        g_state.width,
        g_state.height,
        SDL_WINDOW_OPENGL | SDL_WINDOW_SHOWN
    );
    
    if (!g_state.window) {
        std::cerr << "SDL_CreateWindow failed: " << SDL_GetError() << std::endl;
        return false;
    }
    
    g_state.gl_context = SDL_GL_CreateContext(g_state.window);
    if (!g_state.gl_context) {
        std::cerr << "SDL_GL_CreateContext failed: " << SDL_GetError() << std::endl;
        return false;
    }
    
    SDL_GL_MakeCurrent(g_state.window, g_state.gl_context);
    SDL_GL_SetSwapInterval(1);
    
    glViewport(0, 0, g_state.width, g_state.height);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glOrtho(0, g_state.width, g_state.height, 0, -1, 1);
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    
    g_state.initialized = true;
    return true;
}

void quitSDL() {
    if (g_state.gl_context) {
        SDL_GL_DeleteContext(g_state.gl_context);
        g_state.gl_context = nullptr;
    }
    if (g_state.window) {
        SDL_DestroyWindow(g_state.window);
        g_state.window = nullptr;
    }
    SDL_Quit();
    g_state.initialized = false;
}

bool callPythonCallback(PyObject* callback) {
    if (!callback || callback == Py_None) return true;
    
    PyObject* result = PyObject_CallObject(callback, nullptr);
    if (!result) {
        PyErr_Print();
        return false;
    }
    
    bool shouldContinue = true;
    if (PyBool_Check(result)) {
        shouldContinue = (result == Py_True);
    }
    
    Py_DECREF(result);
    return shouldContinue;
}

bool callPythonUpdate(double dt) {
    if (!g_state.py_update || g_state.py_update == Py_None) return true;
    
    PyObject* args = Py_BuildValue("(d)", dt);
    PyObject* result = PyObject_CallObject(g_state.py_update, args);
    Py_DECREF(args);
    
    if (!result) {
        PyErr_Print();
        return false;
    }
    
    Py_DECREF(result);
    return true;
}

bool callPythonKeyCallback(PyObject* callback, const char* key, int scancode, bool isrepeat) {
    if (!callback || callback == Py_None) return true;
    
    PyObject* args = Py_BuildValue("(sii)", key, scancode, isrepeat ? 1 : 0);
    PyObject* result = PyObject_CallObject(callback, args);
    Py_DECREF(args);
    
    if (!result) {
        PyErr_Print();
        return false;
    }
    
    Py_DECREF(result);
    return true;
}

bool callPythonMouseCallback(PyObject* callback, int x, int y, int button, bool istouch, int presses) {
    if (!callback || callback == Py_None) return true;
    
    PyObject* args = Py_BuildValue("(iiiii)", x, y, button, istouch ? 1 : 0, presses);
    PyObject* result = PyObject_CallObject(callback, args);
    Py_DECREF(args);
    
    if (!result) {
        PyErr_Print();
        return false;
    }
    
    Py_DECREF(result);
    return true;
}

bool loadGameScript(const char* filename) {
    FILE* fp = fopen(filename, "r");
    if (!fp) {
        std::cerr << "Cannot open game file: " << filename << std::endl;
        return false;
    }
    
    PyObject* main_module = PyImport_AddModule("__main__");
    PyObject* global_dict = PyModule_GetDict(main_module);
    
    int result = PyRun_SimpleFile(fp, filename);
    if (result != 0) {
        std::cerr << "Failed to load game script: " << filename << std::endl;
        PyErr_Print();
        fclose(fp);
        return false;
    }
    fclose(fp);
    
    g_state.py_load = PyDict_GetItemString(global_dict, "love_load");
    g_state.py_update = PyDict_GetItemString(global_dict, "love_update");
    g_state.py_draw = PyDict_GetItemString(global_dict, "love_draw");
    g_state.py_quit = PyDict_GetItemString(global_dict, "love_quit");
    g_state.py_keypressed = PyDict_GetItemString(global_dict, "love_keypressed");
    g_state.py_keyreleased = PyDict_GetItemString(global_dict, "love_keyreleased");
    g_state.py_mousepressed = PyDict_GetItemString(global_dict, "love_mousepressed");
    g_state.py_mousereleased = PyDict_GetItemString(global_dict, "love_mousereleased");
    g_state.py_mousemoved = PyDict_GetItemString(global_dict, "love_mousemoved");
    
    Py_XINCREF(g_state.py_load);
    Py_XINCREF(g_state.py_update);
    Py_XINCREF(g_state.py_draw);
    Py_XINCREF(g_state.py_quit);
    Py_XINCREF(g_state.py_keypressed);
    Py_XINCREF(g_state.py_keyreleased);
    Py_XINCREF(g_state.py_mousepressed);
    Py_XINCREF(g_state.py_mousereleased);
    Py_XINCREF(g_state.py_mousemoved);
    
    std::cout << "Game script loaded: " << filename << std::endl;
    return true;
}

int runGame() {
    if (!initSDL()) {
        return 1;
    }
    
    g_state.running = true;
    
    if (g_state.py_load) {
        callPythonCallback(g_state.py_load);
    }
    
    Uint32 last_time = SDL_GetTicks();
    
    while (g_state.running) {
        Uint32 current_time = SDL_GetTicks();
        double dt = (current_time - last_time) / 1000.0;
        last_time = current_time;
        
        SDL_Event event;
        while (SDL_PollEvent(&event)) {
            switch (event.type) {
                case SDL_QUIT:
                    g_state.running = false;
                    break;
                    
                case SDL_KEYDOWN:
                    if (event.key.keysym.sym == SDLK_ESCAPE) {
                        g_state.running = false;
                    }
                    if (g_state.py_keypressed) {
                        const char* key = SDL_GetKeyName(event.key.keysym.sym);
                        callPythonKeyCallback(g_state.py_keypressed, key, 
                                            event.key.keysym.scancode, 
                                            event.key.repeat != 0);
                    }
                    break;
                    
                case SDL_KEYUP:
                    if (g_state.py_keyreleased) {
                        const char* key = SDL_GetKeyName(event.key.keysym.sym);
                        callPythonKeyCallback(g_state.py_keyreleased, key,
                                            event.key.keysym.scancode, false);
                    }
                    break;
                    
                case SDL_MOUSEBUTTONDOWN:
                    if (g_state.py_mousepressed) {
                        int x, y;
                        SDL_GetMouseState(&x, &y);
                        callPythonMouseCallback(g_state.py_mousepressed, x, y,
                                              event.button.button,
                                              event.button.which == SDL_TOUCH_MOUSEID,
                                              event.button.clicks);
                    }
                    break;
                    
                case SDL_MOUSEBUTTONUP:
                    if (g_state.py_mousereleased) {
                        int x, y;
                        SDL_GetMouseState(&x, &y);
                        callPythonMouseCallback(g_state.py_mousereleased, x, y,
                                              event.button.button,
                                              event.button.which == SDL_TOUCH_MOUSEID,
                                              event.button.clicks);
                    }
                    break;
                    
                case SDL_MOUSEMOTION:
                    if (g_state.py_mousemoved) {
                        callPythonMouseCallback(g_state.py_mousemoved, 
                                              event.motion.x, event.motion.y,
                                              event.motion.xrel, event.motion.yrel,
                                              event.motion.which == SDL_TOUCH_MOUSEID);
                    }
                    break;
            }
        }
        
        if (g_state.py_update) {
            if (!callPythonUpdate(dt)) {
                g_state.running = false;
            }
        }
        
        glClear(GL_COLOR_BUFFER_BIT);
        glLoadIdentity();
        
        if (g_state.py_draw) {
            if (!callPythonCallback(g_state.py_draw)) {
                g_state.running = false;
            }
        }
        
        SDL_GL_SwapWindow(g_state.window);
        SDL_Delay(1);
    }
    
    if (g_state.py_quit) {
        callPythonCallback(g_state.py_quit);
    }
    
    Py_XDECREF(g_state.py_load);
    Py_XDECREF(g_state.py_update);
    Py_XDECREF(g_state.py_draw);
    Py_XDECREF(g_state.py_quit);
    Py_XDECREF(g_state.py_keypressed);
    Py_XDECREF(g_state.py_keyreleased);
    Py_XDECREF(g_state.py_mousepressed);
    Py_XDECREF(g_state.py_mousereleased);
    Py_XDECREF(g_state.py_mousemoved);
    
    quitSDL();
    return 0;
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <game.py>" << std::endl;
        std::cerr << "Example: " << argv[0] << " examples/basic_game.py" << std::endl;
        return 1;
    }
    
    Py_Initialize();
    
    // Add current directory to path
    PyRun_SimpleString(
        "import sys\n"
        "sys.path.insert(0, '.')\n"
    );
    
    // Create and register the love module
    PyObject* love = createLoveModule();
    if (!love) {
        std::cerr << "Failed to create love module" << std::endl;
        Py_Finalize();
        return 1;
    }
    PyObject* sys_modules = PyImport_GetModuleDict();
    PyDict_SetItemString(sys_modules, "love", love);
    
    if (!loadGameScript(argv[1])) {
        Py_Finalize();
        return 1;
    }
    
    int result = runGame();
    
    Py_Finalize();
    return result;
}
