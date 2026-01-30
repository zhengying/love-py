/**
 * Callback management module
 */

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <SDL.h>
#include <functional>
#include <string>

#include "love2d_common.h"

namespace py = pybind11;

void callbacks_setLoad(std::function<void()> callback) {
    g_state.load_callback = callback;
}

void callbacks_setUpdate(std::function<void(double)> callback) {
    g_state.update_callback = callback;
}

void callbacks_setDraw(std::function<void()> callback) {
    g_state.draw_callback = callback;
}

void callbacks_setQuit(std::function<bool()> callback) {
    g_state.quit_callback = callback;
}

void callbacks_setKeyPressed(std::function<void(const std::string&, int, bool)> callback) {
    g_state.keypressed_callback = callback;
}

void callbacks_setKeyReleased(std::function<void(const std::string&, int)> callback) {
    g_state.keyreleased_callback = callback;
}

void callbacks_setMousePressed(std::function<void(int, int, int, bool, int)> callback) {
    g_state.mousepressed_callback = callback;
}

void callbacks_setMouseReleased(std::function<void(int, int, int, bool, int)> callback) {
    g_state.mousereleased_callback = callback;
}

void callbacks_setMouseMoved(std::function<void(int, int, int, int, bool)> callback) {
    g_state.mousemoved_callback = callback;
}

void callbacks_run() {
    g_state.running = true;
    
    // Call load callback
    if (g_state.load_callback) {
        g_state.load_callback();
    }
    
    // Main game loop
    while (g_state.running) {
        // Process events would go here
        // For now, simplified loop
        
        // Get delta time and call update
        extern double timer_step();
        double dt = timer_step();
        
        if (g_state.update_callback) {
            g_state.update_callback(dt);
        }
        
        // Draw
        if (g_state.draw_callback) {
            g_state.draw_callback();
        }
        
        // Present
        extern void graphics_present();
        graphics_present();
        
        // Simple delay to avoid maxing CPU
        SDL_Delay(1);
    }
}

void callbacks_stop() {
    g_state.running = false;
}

void init_callbacks(py::module_ &m) {
    m.doc() = "Game loop callback management";
    
    m.def("setLoad", &callbacks_setLoad, "Set the load callback");
    m.def("setUpdate", &callbacks_setUpdate, "Set the update callback");
    m.def("setDraw", &callbacks_setDraw, "Set the draw callback");
    m.def("setQuit", &callbacks_setQuit, "Set the quit callback");
    m.def("setKeyPressed", &callbacks_setKeyPressed, "Set key pressed callback");
    m.def("setKeyReleased", &callbacks_setKeyReleased, "Set key released callback");
    m.def("setMousePressed", &callbacks_setMousePressed, "Set mouse pressed callback");
    m.def("setMouseReleased", &callbacks_setMouseReleased, "Set mouse released callback");
    m.def("setMouseMoved", &callbacks_setMouseMoved, "Set mouse moved callback");
    m.def("run", &callbacks_run, "Run the game loop");
    m.def("stop", &callbacks_stop, "Stop the game loop");
}
