/**
 * Graphics module bindings
 */

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <SDL.h>
#ifdef __APPLE__
#include <OpenGL/gl.h>
#else
#include <GL/gl.h>
#endif

#include "love2d_common.h"

namespace py = pybind11;

// Graphics state
struct GraphicsState {
    float color_r = 1.0f, color_g = 1.0f, color_b = 1.0f, color_a = 1.0f;
    float bg_r = 0.0f, bg_g = 0.0f, bg_b = 0.0f, bg_a = 1.0f;
    int current_width = 800;
    int current_height = 600;
};

static GraphicsState g_graphics_state;

// Basic drawing functions
void graphics_clear(float r, float g, float b, float a) {
    glClearColor(r, g, b, a);
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
}

void graphics_setColor(float r, float g, float b, float a) {
    g_graphics_state.color_r = r;
    g_graphics_state.color_g = g;
    g_graphics_state.color_b = b;
    g_graphics_state.color_a = a;
    glColor4f(r, g, b, a);
}

py::tuple graphics_getColor() {
    return py::make_tuple(
        g_graphics_state.color_r,
        g_graphics_state.color_g,
        g_graphics_state.color_b,
        g_graphics_state.color_a
    );
}

void graphics_setBackgroundColor(float r, float g, float b, float a) {
    g_graphics_state.bg_r = r;
    g_graphics_state.bg_g = g;
    g_graphics_state.bg_b = b;
    g_graphics_state.bg_a = a;
}

py::tuple graphics_getBackgroundColor() {
    return py::make_tuple(
        g_graphics_state.bg_r,
        g_graphics_state.bg_g,
        g_graphics_state.bg_b,
        g_graphics_state.bg_a
    );
}

// Rectangle drawing
void graphics_rectangle(const std::string& mode, float x, float y, float width, float height) {
    GLenum draw_mode = (mode == "fill") ? GL_QUADS : GL_LINE_LOOP;
    
    glBegin(draw_mode);
    glVertex2f(x, y);
    glVertex2f(x + width, y);
    glVertex2f(x + width, y + height);
    glVertex2f(x, y + height);
    glEnd();
}

// Circle drawing (simplified)
void graphics_circle(const std::string& mode, float x, float y, float radius) {
    const int segments = 32;
    GLenum draw_mode = (mode == "fill") ? GL_TRIANGLE_FAN : GL_LINE_LOOP;
    
    glBegin(draw_mode);
    for (int i = 0; i < segments; i++) {
        float angle = 2.0f * 3.14159f * i / segments;
        glVertex2f(x + radius * cosf(angle), y + radius * sinf(angle));
    }
    glEnd();
}

// Line drawing
void graphics_line(float x1, float y1, float x2, float y2) {
    glBegin(GL_LINES);
    glVertex2f(x1, y1);
    glVertex2f(x2, y2);
    glEnd();
}

// Transformations
void graphics_push() {
    glPushMatrix();
}

void graphics_pop() {
    glPopMatrix();
}

void graphics_origin() {
    glLoadIdentity();
}

void graphics_translate(float x, float y) {
    glTranslatef(x, y, 0.0f);
}

void graphics_rotate(float angle) {
    glRotatef(angle * 180.0f / 3.14159f, 0.0f, 0.0f, 1.0f);
}

void graphics_scale(float sx, float sy) {
    glScalef(sx, sy, 1.0f);
}

// Present (swap buffers)
void graphics_present() {
    SDL_GL_SwapWindow(SDL_GL_GetCurrentWindow());
}

// Get dimensions
int graphics_getWidth() {
    return g_graphics_state.current_width;
}

int graphics_getHeight() {
    return g_graphics_state.current_height;
}

py::tuple graphics_getDimensions() {
    return py::make_tuple(
        g_graphics_state.current_width,
        g_graphics_state.current_height
    );
}

void init_graphics(py::module_ &m) {
    m.doc() = "Graphics drawing functions";
    
    // State functions
    m.def("clear", &graphics_clear, "Clear the screen",
          py::arg("r") = 0.0f, py::arg("g") = 0.0f, py::arg("b") = 0.0f, py::arg("a") = 1.0f);
    m.def("present", &graphics_present, "Present the rendered frame");
    m.def("setColor", &graphics_setColor, "Set drawing color (0-1 range)",
          py::arg("r"), py::arg("g"), py::arg("b"), py::arg("a") = 1.0f);
    m.def("getColor", &graphics_getColor, "Get current drawing color");
    m.def("setBackgroundColor", &graphics_setBackgroundColor, "Set background color",
          py::arg("r"), py::arg("g"), py::arg("b"), py::arg("a") = 1.0f);
    m.def("getBackgroundColor", &graphics_getBackgroundColor, "Get background color");
    
    // Drawing functions
    m.def("rectangle", &graphics_rectangle, "Draw a rectangle",
          py::arg("mode"), py::arg("x"), py::arg("y"), py::arg("width"), py::arg("height"));
    m.def("circle", &graphics_circle, "Draw a circle",
          py::arg("mode"), py::arg("x"), py::arg("y"), py::arg("radius"));
    m.def("line", &graphics_line, "Draw a line",
          py::arg("x1"), py::arg("y1"), py::arg("x2"), py::arg("y2"));
    
    // Transformations
    m.def("push", &graphics_push, "Save transformation state");
    m.def("pop", &graphics_pop, "Restore transformation state");
    m.def("origin", &graphics_origin, "Reset transformation");
    m.def("translate", &graphics_translate, "Translate coordinate system",
          py::arg("dx"), py::arg("dy"));
    m.def("rotate", &graphics_rotate, "Rotate coordinate system",
          py::arg("angle"));
    m.def("scale", &graphics_scale, "Scale coordinate system",
          py::arg("sx"), py::arg("sy"));
    
    // Dimensions
    m.def("getWidth", &graphics_getWidth, "Get screen width");
    m.def("getHeight", &graphics_getHeight, "Get screen height");
    m.def("getDimensions", &graphics_getDimensions, "Get screen dimensions (width, height)");
    
}
