/**
 * Window module bindings
 */

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <SDL.h>

#include "love2d_common.h"

namespace py = pybind11;

bool window_setMode(int width, int height, py::dict flags) {
    g_state.window_width = width;
    g_state.window_height = height;
    
    Uint32 sdl_flags = SDL_WINDOW_OPENGL | SDL_WINDOW_SHOWN;
    
    if (flags.contains("fullscreen")) {
        if (flags["fullscreen"].cast<bool>()) {
            sdl_flags |= SDL_WINDOW_FULLSCREEN;
        }
    }
    
    if (flags.contains("resizable")) {
        if (flags["resizable"].cast<bool>()) {
            sdl_flags |= SDL_WINDOW_RESIZABLE;
        }
    }
    
    if (flags.contains("borderless")) {
        if (flags["borderless"].cast<bool>()) {
            sdl_flags |= SDL_WINDOW_BORDERLESS;
        }
    }
    
    if (g_state.window) {
        SDL_SetWindowSize(g_state.window, width, height);
        SDL_SetWindowFullscreen(g_state.window, 
            (sdl_flags & SDL_WINDOW_FULLSCREEN) ? SDL_WINDOW_FULLSCREEN : 0);
    } else {
        g_state.window = SDL_CreateWindow(
            g_state.window_title.c_str(),
            SDL_WINDOWPOS_CENTERED,
            SDL_WINDOWPOS_CENTERED,
            width,
            height,
            sdl_flags
        );
        
        if (!g_state.window) {
            return false;
        }
        
        g_state.gl_context = SDL_GL_CreateContext(g_state.window);
        if (!g_state.gl_context) {
            SDL_DestroyWindow(g_state.window);
            g_state.window = nullptr;
            return false;
        }
        
        SDL_GL_MakeCurrent(g_state.window, g_state.gl_context);
    }
    
    return true;
}

py::tuple window_getMode() {
    py::dict flags;
    flags["fullscreen"] = false;
    flags["resizable"] = false;
    flags["borderless"] = false;
    flags["vsync"] = 1;
    
    return py::make_tuple(g_state.window_width, g_state.window_height, flags);
}

void window_setFullscreen(bool fullscreen) {
    if (g_state.window) {
        SDL_SetWindowFullscreen(g_state.window, 
            fullscreen ? SDL_WINDOW_FULLSCREEN : 0);
    }
}

bool window_getFullscreen() {
    if (g_state.window) {
        Uint32 flags = SDL_GetWindowFlags(g_state.window);
        return (flags & SDL_WINDOW_FULLSCREEN) != 0;
    }
    return false;
}

void window_close() {
    if (g_state.window) {
        SDL_DestroyWindow(g_state.window);
        g_state.window = nullptr;
    }
    if (g_state.gl_context) {
        SDL_GL_DeleteContext(g_state.gl_context);
        g_state.gl_context = nullptr;
    }
}

void window_setTitle(const std::string& title) {
    g_state.window_title = title;
    if (g_state.window) {
        SDL_SetWindowTitle(g_state.window, title.c_str());
    }
}

std::string window_getTitle() {
    if (g_state.window) {
        return SDL_GetWindowTitle(g_state.window);
    }
    return g_state.window_title;
}

int window_getWidth() {
    return g_state.window_width;
}

int window_getHeight() {
    return g_state.window_height;
}

py::tuple window_getDimensions() {
    return py::make_tuple(g_state.window_width, g_state.window_height);
}

void window_setVSync(int vsync) {
    SDL_GL_SetSwapInterval(vsync);
}

int window_getVSync() {
    return SDL_GL_GetSwapInterval();
}

bool window_hasFocus() {
    if (g_state.window) {
        Uint32 flags = SDL_GetWindowFlags(g_state.window);
        return (flags & SDL_WINDOW_INPUT_FOCUS) != 0;
    }
    return false;
}

bool window_hasMouseFocus() {
    if (g_state.window) {
        Uint32 flags = SDL_GetWindowFlags(g_state.window);
        return (flags & SDL_WINDOW_MOUSE_FOCUS) != 0;
    }
    return false;
}

void init_window(py::module_ &m) {
    m.doc() = "Window management functions";
    
    m.def("setMode", &window_setMode, "Set window mode/size",
          py::arg("width"), py::arg("height"), py::arg("flags") = py::dict());
    m.def("getMode", &window_getMode, "Get window mode (width, height, flags)");
    m.def("setFullscreen", &window_setFullscreen, "Set fullscreen mode",
          py::arg("fullscreen"));
    m.def("getFullscreen", &window_getFullscreen, "Get fullscreen state");
    m.def("close", &window_close, "Close the window");
    m.def("setTitle", &window_setTitle, "Set window title",
          py::arg("title"));
    m.def("getTitle", &window_getTitle, "Get window title");
    m.def("getWidth", &window_getWidth, "Get window width");
    m.def("getHeight", &window_getHeight, "Get window height");
    m.def("getDimensions", &window_getDimensions, "Get window dimensions");
    m.def("setVSync", &window_setVSync, "Set vertical sync",
          py::arg("vsync"));
    m.def("getVSync", &window_getVSync, "Get vertical sync state");
    m.def("hasFocus", &window_hasFocus, "Check if window has keyboard focus");
    m.def("hasMouseFocus", &window_hasMouseFocus, "Check if window has mouse focus");
    
}
