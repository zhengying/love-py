/**
 * LOVE2D for Python - Main Executable
 * 
 * This is the C++ entry point (like original love.exe).
 * It runs the main game loop and calls Python callbacks.
 * 
 * Usage: ./love game.py
 */

#include <Python.h>
#include <SDL.h>
#include <OpenGL/gl.h>
#include <iostream>
#include <string>
#include <cstring>

// Global state for the game
struct GameState {
    bool running = false;
    bool initialized = false;
    SDL_Window* window = nullptr;
    SDL_GLContext gl_context = nullptr;
    int width = 800;
    int height = 600;
    std::string title = "LOVE2D Python";
    
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

// Initialize SDL and create window
bool initSDL() {
    if (SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO | SDL_INIT_TIMER) < 0) {
        std::cerr << "SDL_Init failed: " << SDL_GetError() << std::endl;
        return false;
    }
    
    // Set OpenGL attributes
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_MAJOR_VERSION, 2);
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_MINOR_VERSION, 1);
    SDL_GL_SetAttribute(SDL_GL_DOUBLEBUFFER, 1);
    SDL_GL_SetAttribute(SDL_GL_DEPTH_SIZE, 24);
    
    // Create window
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
    
    // Create OpenGL context
    g_state.gl_context = SDL_GL_CreateContext(g_state.window);
    if (!g_state.gl_context) {
        std::cerr << "SDL_GL_CreateContext failed: " << SDL_GetError() << std::endl;
        return false;
    }
    
    SDL_GL_MakeCurrent(g_state.window, g_state.gl_context);
    
    // Enable vsync by default
    SDL_GL_SetSwapInterval(1);
    
    // Initialize OpenGL state
    glViewport(0, 0, g_state.width, g_state.height);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glOrtho(0, g_state.width, g_state.height, 0, -1, 1);
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    
    g_state.initialized = true;
    return true;
}

// Shutdown SDL
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

// Call a Python callback (if it exists)
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

// Call update with dt parameter
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

// Call key callback with parameters
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

// Call mouse callback with parameters
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

// Load Python game script and extract callbacks
bool loadGameScript(const char* filename) {
    FILE* fp = fopen(filename, "r");
    if (!fp) {
        std::cerr << "Cannot open game file: " << filename << std::endl;
        return false;
    }
    fclose(fp);
    
    // Run the Python script
    PyObject* main_module = PyImport_AddModule("__main__");
    PyObject* global_dict = PyModule_GetDict(main_module);
    
    int result = PyRun_SimpleFile(fp, filename);
    if (result != 0) {
        std::cerr << "Failed to load game script: " << filename << std::endl;
        PyErr_Print();
        return false;
    }
    
    // Extract callbacks from the global namespace
    g_state.py_load = PyDict_GetItemString(global_dict, "love_load");
    g_state.py_update = PyDict_GetItemString(global_dict, "love_update");
    g_state.py_draw = PyDict_GetItemString(global_dict, "love_draw");
    g_state.py_quit = PyDict_GetItemString(global_dict, "love_quit");
    g_state.py_keypressed = PyDict_GetItemString(global_dict, "love_keypressed");
    g_state.py_keyreleased = PyDict_GetItemString(global_dict, "love_keyreleased");
    g_state.py_mousepressed = PyDict_GetItemString(global_dict, "love_mousepressed");
    g_state.py_mousereleased = PyDict_GetItemString(global_dict, "love_mousereleased");
    g_state.py_mousemoved = PyDict_GetItemString(global_dict, "love_mousemoved");
    
    // Increment reference counts for callbacks we keep
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

// Main game loop
int runGame() {
    if (!initSDL()) {
        return 1;
    }
    
    g_state.running = true;
    
    // Call load callback
    if (g_state.py_load) {
        callPythonCallback(g_state.py_load);
    }
    
    // Main loop
    Uint32 last_time = SDL_GetTicks();
    
    while (g_state.running) {
        // Calculate delta time
        Uint32 current_time = SDL_GetTicks();
        double dt = (current_time - last_time) / 1000.0;
        last_time = current_time;
        
        // Process events
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
        
        // Call update
        if (g_state.py_update) {
            if (!callPythonUpdate(dt)) {
                g_state.running = false;
            }
        }
        
        // Clear screen
        glClear(GL_COLOR_BUFFER_BIT);
        glLoadIdentity();
        
        // Call draw
        if (g_state.py_draw) {
            if (!callPythonCallback(g_state.py_draw)) {
                g_state.running = false;
            }
        }
        
        // Present frame
        SDL_GL_SwapWindow(g_state.window);
        
        // Small delay to prevent maxing CPU
        SDL_Delay(1);
    }
    
    // Call quit callback
    if (g_state.py_quit) {
        callPythonCallback(g_state.py_quit);
    }
    
    // Cleanup Python callbacks
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
    
    // Initialize Python
    Py_Initialize();
    
    // Add current directory to Python path
    PyRun_SimpleString("import sys; sys.path.insert(0, '.')");
    
    // Load the game script
    if (!loadGameScript(argv[1])) {
        Py_Finalize();
        return 1;
    }
    
    // Run the game
    int result = runGame();
    
    // Finalize Python
    Py_Finalize();
    
    return result;
}
