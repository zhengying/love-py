/**
 * LOVE2D Python Bindings - Common Header
 * 
 * This header defines the shared state structure used across all modules.
 */

#ifndef LOVE2D_COMMON_H
#define LOVE2D_COMMON_H

#include <SDL.h>
#include <functional>
#include <string>

// Global state structure - shared across all modules
struct LoveState {
    bool initialized = false;
    bool running = false;
    SDL_Window* window = nullptr;
    SDL_GLContext gl_context = nullptr;
    int window_width = 800;
    int window_height = 600;
    std::string window_title = "LOVE2D Python";
    
    // Callbacks
    std::function<void()> load_callback;
    std::function<void(double)> update_callback;
    std::function<void()> draw_callback;
    std::function<bool()> quit_callback;
    std::function<void(const std::string&, int, bool)> keypressed_callback;
    std::function<void(const std::string&, int)> keyreleased_callback;
    std::function<void(int, int, int, bool, int)> mousepressed_callback;
    std::function<void(int, int, int, bool, int)> mousereleased_callback;
    std::function<void(int, int, int, int, bool)> mousemoved_callback;
};

// Global state instance - defined in love2d_bindings.cpp
extern LoveState g_state;

#endif // LOVE2D_COMMON_H
