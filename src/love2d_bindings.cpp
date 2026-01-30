/**
 * LOVE2D Python Bindings - Main Module
 * 
 * This file creates the core _love2d_core module using pybind11.
 * It provides the bridge between LOVE2D C++ and Python.
 */

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>
#include <pybind11/numpy.h>

#include <SDL.h>
#include <memory>
#include <string>
#include <vector>
#include <functional>
#include <map>

#include "love2d_common.h"

namespace py = pybind11;

// Forward declarations for module bindings
void init_graphics(py::module_ &m);
void init_window(py::module_ &m);
void init_event(py::module_ &m);
void init_timer(py::module_ &m);
void init_keyboard(py::module_ &m);
void init_mouse(py::module_ &m);
void init_callbacks(py::module_ &m);
void init_audio(py::module_ &m);
void init_filesystem(py::module_ &m);
void init_image(py::module_ &m);

// Core initialization
bool love_init() {
    if (g_state.initialized) {
        return true;
    }
    
    if (SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO | SDL_INIT_TIMER) < 0) {
        return false;
    }
    
    // Set OpenGL attributes
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_MAJOR_VERSION, 2);
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_MINOR_VERSION, 1);
    SDL_GL_SetAttribute(SDL_GL_DOUBLEBUFFER, 1);
    SDL_GL_SetAttribute(SDL_GL_DEPTH_SIZE, 24);
    
    g_state.initialized = true;
    return true;
}

void love_quit() {
    if (g_state.window) {
        SDL_DestroyWindow(g_state.window);
        g_state.window = nullptr;
    }
    if (g_state.gl_context) {
        SDL_GL_DeleteContext(g_state.gl_context);
        g_state.gl_context = nullptr;
    }
    SDL_Quit();
    g_state.initialized = false;
}

// Version
py::tuple love_getVersion() {
    return py::make_tuple(11, 5, 0, "Mysterious Mysteries");
}

// Define the global state
LoveState g_state;

PYBIND11_MODULE(_love2d_core, m) {
    m.doc() = "LOVE2D Python bindings core module";
    
    // Version
    m.def("getVersion", &love_getVersion, "Get LOVE version (major, minor, revision, codename)");
    m.def("init", &love_init, "Initialize LOVE2D");
    m.def("quit", &love_quit, "Shutdown LOVE2D");
    
    // Bind the LoveState struct and expose instance
    py::class_<LoveState>(m, "_LoveState")
        .def_readwrite("initialized", &LoveState::initialized)
        .def_readwrite("running", &LoveState::running)
        .def_readwrite("window_width", &LoveState::window_width)
        .def_readwrite("window_height", &LoveState::window_height);
    m.attr("_state") = py::cast(&g_state, py::return_value_policy::reference);
    
    // Initialize submodules
    py::module_ graphics = m.def_submodule("graphics", "Graphics module");
    init_graphics(graphics);
    
    py::module_ window = m.def_submodule("window", "Window module");
    init_window(window);
    
    py::module_ event = m.def_submodule("event", "Event module");
    init_event(event);
    
    py::module_ timer = m.def_submodule("timer", "Timer module");
    init_timer(timer);
    
    py::module_ keyboard = m.def_submodule("keyboard", "Keyboard module");
    init_keyboard(keyboard);
    
    py::module_ mouse = m.def_submodule("mouse", "Mouse module");
    init_mouse(mouse);
    
    py::module_ callbacks = m.def_submodule("callbacks", "Callback management");
    init_callbacks(callbacks);
    
    py::module_ audio = m.def_submodule("audio", "Audio module");
    init_audio(audio);
    
    py::module_ filesystem = m.def_submodule("filesystem", "Filesystem module");
    init_filesystem(filesystem);
    
    py::module_ image = m.def_submodule("image", "Image loading and texture management");
    init_image(image);
}
