/**
 * Timer module bindings
 */

#include <pybind11/pybind11.h>
#include <SDL.h>

#include "love2d_common.h"

namespace py = pybind11;

static Uint64 g_start_time = 0;
static Uint64 g_last_frame_time = 0;
static double g_delta_time = 0.0;
static double g_fps = 0.0;
static int g_frame_count = 0;
static Uint64 g_fps_last_time = 0;

double timer_getTime() {
    return (double)(SDL_GetTicks()) / 1000.0;
}

double timer_getDelta() {
    return g_delta_time;
}

int timer_getFPS() {
    return (int)g_fps;
}

double timer_step() {
    Uint64 current_time = SDL_GetTicks();
    
    if (g_last_frame_time == 0) {
        g_last_frame_time = current_time;
        g_start_time = current_time;
        g_fps_last_time = current_time;
    }
    
    // Calculate delta time
    g_delta_time = (double)(current_time - g_last_frame_time) / 1000.0;
    g_last_frame_time = current_time;
    
    // Update FPS counter
    g_frame_count++;
    if (current_time - g_fps_last_time >= 1000) {
        g_fps = (double)g_frame_count * 1000.0 / (double)(current_time - g_fps_last_time);
        g_frame_count = 0;
        g_fps_last_time = current_time;
    }
    
    return g_delta_time;
}

void timer_sleep(double seconds) {
    SDL_Delay((Uint32)(seconds * 1000));
}

void init_timer(py::module_ &m) {
    m.doc() = "Time and frame rate functions";
    
    m.def("getTime", &timer_getTime, "Get time since application start (seconds)");
    m.def("getDelta", &timer_getDelta, "Get delta time (seconds since last frame)");
    m.def("getFPS", &timer_getFPS, "Get current FPS");
    m.def("step", &timer_step, "Advance the timer and get delta time");
    m.def("sleep", &timer_sleep, "Sleep for specified seconds",
          py::arg("s"));
}
