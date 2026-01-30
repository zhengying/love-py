/**
 * Mouse module bindings
 */

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <SDL.h>

#include "love2d_common.h"

namespace py = pybind11;

py::tuple mouse_getPosition() {
    int x, y;
    SDL_GetMouseState(&x, &y);
    return py::make_tuple(x, y);
}

int mouse_getX() {
    int x, y;
    SDL_GetMouseState(&x, &y);
    return x;
}

int mouse_getY() {
    int x, y;
    SDL_GetMouseState(&x, &y);
    return y;
}

void mouse_setPosition(int x, int y) {
    SDL_WarpMouseInWindow(g_state.window, x, y);
}

bool mouse_isDown(py::args buttons) {
    Uint32 state = SDL_GetMouseState(nullptr, nullptr);
    
    for (auto btn : buttons) {
        int button = btn.cast<int>();
        Uint32 mask = 0;
        switch (button) {
            case 1: mask = SDL_BUTTON_LMASK; break;
            case 2: mask = SDL_BUTTON_MMASK; break;
            case 3: mask = SDL_BUTTON_RMASK; break;
            case 4: mask = SDL_BUTTON_X1MASK; break;
            case 5: mask = SDL_BUTTON_X2MASK; break;
        }
        if (state & mask) {
            return true;
        }
    }
    
    return false;
}

bool mouse_isVisible() {
    return SDL_ShowCursor(SDL_QUERY) == SDL_ENABLE;
}

void mouse_setVisible(bool visible) {
    SDL_ShowCursor(visible ? SDL_ENABLE : SDL_DISABLE);
}

bool mouse_isGrabbed() {
    return SDL_GetWindowGrab(g_state.window) == SDL_TRUE;
}

void mouse_setGrabbed(bool grabbed) {
    SDL_SetWindowGrab(g_state.window, grabbed ? SDL_TRUE : SDL_FALSE);
}

void init_mouse(py::module_ &m) {
    m.doc() = "Mouse input functions";
    
    m.def("getPosition", &mouse_getPosition, "Get mouse position (x, y)");
    m.def("getX", &mouse_getX, "Get mouse X position");
    m.def("getY", &mouse_getY, "Get mouse Y position");
    m.def("setPosition", &mouse_setPosition, "Set mouse position",
          py::arg("x"), py::arg("y"));
    m.def("isDown", &mouse_isDown, "Check if mouse button(s) are pressed");
    m.def("isVisible", &mouse_isVisible, "Check if cursor is visible");
    m.def("setVisible", &mouse_setVisible, "Show/hide cursor",
          py::arg("visible"));
    m.def("isGrabbed", &mouse_isGrabbed, "Check if cursor is grabbed");
    m.def("setGrabbed", &mouse_setGrabbed, "Grab/release cursor",
          py::arg("grabbed"));
}
