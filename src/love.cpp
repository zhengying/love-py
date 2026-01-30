/**
 * LOVE2D for Python - Main Executable
 * 
 * This is the C++ entry point (like original love.exe).
 * It creates the love module using Python C API and runs the main game loop.
 * 
 * Usage: ./love game.py
 */

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <SDL3/SDL.h>
#include <OpenGL/gl.h>
#include <iostream>
#include <string>
#include <cstring>
#include <cmath>
#include <sys/stat.h>
#if defined(_WIN32)
    #include <direct.h>
    #include <windows.h>
#else
    #include <dirent.h>
    #include <unistd.h>
#endif

#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"

#include <ft2build.h>
#include FT_FREETYPE_H

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
    
    // Font state
    PyObject* current_font = nullptr;
    PyObject* default_font = nullptr;  // Cached default font
};

static GameState g_state;

// ============================================================================
// Image Type Definition
// ============================================================================

typedef struct {
    PyObject_HEAD
    GLuint texture_id;
    int width;
    int height;
} ImageObject;

static void image_dealloc(PyObject* self) {
    ImageObject* img = (ImageObject*)self;
    if (img->texture_id != 0) {
        glDeleteTextures(1, &img->texture_id);
    }
    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject* image_getWidth(PyObject* self, PyObject* args) {
    ImageObject* img = (ImageObject*)self;
    return PyLong_FromLong(img->width);
}

static PyObject* image_getHeight(PyObject* self, PyObject* args) {
    ImageObject* img = (ImageObject*)self;
    return PyLong_FromLong(img->height);
}

static PyMethodDef ImageMethods[] = {
    {"getWidth", (PyCFunction)image_getWidth, METH_NOARGS, "Get image width"},
    {"getHeight", (PyCFunction)image_getHeight, METH_NOARGS, "Get image height"},
    {nullptr, nullptr, 0, nullptr}
};

static PyTypeObject ImageType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "love.Image",
    .tp_basicsize = sizeof(ImageObject),
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_doc = "Image object",
    .tp_dealloc = image_dealloc,
    .tp_methods = ImageMethods,
};

// ============================================================================
// Font Type Definition
// ============================================================================

static FT_Library ft_library = nullptr;

struct Character {
    GLuint texture_id;
    int width;
    int height;
    int bearing_x;
    int bearing_y;
    long advance;
};

typedef struct {
    PyObject_HEAD
    FT_Face face;
    int size;
    Character characters[128];
    GLint filter_min;
    GLint filter_mag;
} FontObject;

static void font_dealloc(PyObject* self) {
    FontObject* font = (FontObject*)self;
    
    // Only cleanup if FreeType library is still valid
    if (ft_library && font->face) {
        FT_Done_Face(font->face);
        font->face = nullptr;
    }
    
    // Note: We can't delete OpenGL textures here during Python shutdown
    // as the GL context may already be destroyed
    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject* font_getHeight(PyObject* self, PyObject* args) {
    FontObject* font = (FontObject*)self;
    if (font->face) {
        return PyLong_FromLong(font->face->size->metrics.height >> 6);
    }
    return PyLong_FromLong(0);
}

static PyObject* font_getWidth(PyObject* self, PyObject* args) {
    FontObject* font = (FontObject*)self;
    const char* text;
    if (!PyArg_ParseTuple(args, "s", &text))
        return nullptr;
    
    float width = 0;
    for (const char* p = text; *p; p++) {
        if (*p < 128 && font->characters[*p].texture_id != 0) {
            width += (font->characters[*p].advance >> 6);
        }
    }
    return PyFloat_FromDouble(width);
}

static PyObject* font_setFilter(PyObject* self, PyObject* args) {
    FontObject* font = (FontObject*)self;
    const char* min_filter;
    const char* mag_filter;
    
    if (!PyArg_ParseTuple(args, "ss", &min_filter, &mag_filter))
        return nullptr;
    
    // Parse minification filter
    if (strcmp(min_filter, "linear") == 0) {
        font->filter_min = GL_LINEAR;
    } else if (strcmp(min_filter, "nearest") == 0) {
        font->filter_min = GL_NEAREST;
    } else {
        PyErr_SetString(PyExc_ValueError, "Invalid minification filter. Use 'linear' or 'nearest'.");
        return nullptr;
    }
    
    // Parse magnification filter
    if (strcmp(mag_filter, "linear") == 0) {
        font->filter_mag = GL_LINEAR;
    } else if (strcmp(mag_filter, "nearest") == 0) {
        font->filter_mag = GL_NEAREST;
    } else {
        PyErr_SetString(PyExc_ValueError, "Invalid magnification filter. Use 'linear' or 'nearest'.");
        return nullptr;
    }
    
    // Update existing textures
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1);
    for (int c = 0; c < 128; c++) {
        if (font->characters[c].texture_id != 0) {
            glBindTexture(GL_TEXTURE_2D, font->characters[c].texture_id);
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, font->filter_min);
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, font->filter_mag);
        }
    }
    glBindTexture(GL_TEXTURE_2D, 0);
    
    Py_RETURN_NONE;
}

static PyMethodDef FontMethods[] = {
    {"getHeight", (PyCFunction)font_getHeight, METH_NOARGS, "Get font height"},
    {"getWidth", (PyCFunction)font_getWidth, METH_VARARGS, "Get text width"},
    {"setFilter", (PyCFunction)font_setFilter, METH_VARARGS, "Set texture filter (min_filter, mag_filter) - 'linear' or 'nearest'"},
    {nullptr, nullptr, 0, nullptr}
};

static PyTypeObject FontType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "love.Font",
    .tp_basicsize = sizeof(FontObject),
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_doc = "Font object",
    .tp_dealloc = font_dealloc,
    .tp_methods = FontMethods,
};

static PyObject* font_newFont(PyObject* self, PyObject* args) {
    const char* filename;
    int size = 12;
    if (!PyArg_ParseTuple(args, "s|i", &filename, &size))
        return nullptr;

    if (!ft_library) {
        if (FT_Init_FreeType(&ft_library)) {
            PyErr_SetString(PyExc_RuntimeError, "Failed to initialize FreeType");
            return nullptr;
        }
    }

    FontObject* font = PyObject_New(FontObject, &FontType);
    if (!font) {
        return nullptr;
    }

    font->face = nullptr;
    font->size = size;
    memset(font->characters, 0, sizeof(font->characters));
    font->filter_min = GL_LINEAR;  // Default: linear filtering
    font->filter_mag = GL_LINEAR;

    if (FT_New_Face(ft_library, filename, 0, &font->face)) {
        Py_DECREF(font);
        PyErr_SetString(PyExc_IOError, "Failed to load font");
        return nullptr;
    }

    FT_Set_Pixel_Sizes(font->face, 0, size);

    glPixelStorei(GL_UNPACK_ALIGNMENT, 1);

    for (unsigned char c = 0; c < 128; c++) {
        // Load character with better hinting
        if (FT_Load_Char(font->face, c, FT_LOAD_RENDER | FT_LOAD_FORCE_AUTOHINT)) {
            continue;
        }

        GLuint texture = 0;
        int width = font->face->glyph->bitmap.width;
        int height = font->face->glyph->bitmap.rows;
        
        // Only create texture if there's actual bitmap data
        if (width > 0 && height > 0 && font->face->glyph->bitmap.buffer) {
            // Get FreeType bitmap info
            FT_Bitmap* bitmap = &font->face->glyph->bitmap;
            int pitch = bitmap->pitch;
            
            // Allocate buffer for tightly-packed texture data (no padding)
            unsigned char* tex_data = new unsigned char[width * height];
            memset(tex_data, 0, width * height);
            
            // Handle different pixel modes from FreeType
            if (bitmap->pixel_mode == FT_PIXEL_MODE_GRAY) {
                // 8-bit grayscale - copy row by row accounting for pitch
                for (int y = 0; y < height; y++) {
                    for (int x = 0; x < width; x++) {
                        tex_data[y * width + x] = bitmap->buffer[y * pitch + x];
                    }
                }
            } else if (bitmap->pixel_mode == FT_PIXEL_MODE_MONO) {
                // 1-bit monochrome - expand to 8-bit
                for (int y = 0; y < height; y++) {
                    for (int x = 0; x < width; x++) {
                        // Extract bit and convert to 0 or 255
                        unsigned char byte = bitmap->buffer[y * pitch + (x / 8)];
                        unsigned char bit = (byte >> (7 - (x % 8))) & 1;
                        tex_data[y * width + x] = bit ? 255 : 0;
                    }
                }
            } else {
                // Unknown pixel mode - skip this character
                delete[] tex_data;
                continue;
            }
            
            glGenTextures(1, &texture);
            glBindTexture(GL_TEXTURE_2D, texture);
            
            // Upload tightly-packed glyph bitmap as alpha texture
            glPixelStorei(GL_UNPACK_ALIGNMENT, 1);
            glTexImage2D(
                GL_TEXTURE_2D,
                0,
                GL_ALPHA,
                width,
                height,
                0,
                GL_ALPHA,
                GL_UNSIGNED_BYTE,
                tex_data
            );
            
            // Clean up temp buffer
            delete[] tex_data;
            
            // Use font's filter settings (defaults to linear, can be changed with setFilter)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE);
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, font->filter_min);
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, font->filter_mag);
        }

        font->characters[c].texture_id = texture;
        font->characters[c].width = width;
        font->characters[c].height = height;
        font->characters[c].bearing_x = font->face->glyph->bitmap_left;
        font->characters[c].bearing_y = font->face->glyph->bitmap_top;
        font->characters[c].advance = font->face->glyph->advance.x;
    }

    glBindTexture(GL_TEXTURE_2D, 0);

    return (PyObject*)font;
}

static PyMethodDef FontModuleMethods[] = {
    {"newFont", font_newFont, METH_VARARGS, "Create new font from file (filename, size=12)"},
    {nullptr, nullptr, 0, nullptr}
};

static PyObject* image_newImage(PyObject* self, PyObject* args) {
    const char* filename;
    if (!PyArg_ParseTuple(args, "s", &filename))
        return nullptr;

    int width, height, channels;
    unsigned char* data = stbi_load(filename, &width, &height, &channels, 4);
    if (!data) {
        PyErr_SetString(PyExc_IOError, "Failed to load image");
        return nullptr;
    }

    ImageObject* img = PyObject_New(ImageObject, &ImageType);
    if (!img) {
        stbi_image_free(data);
        return nullptr;
    }

    img->width = width;
    img->height = height;

    glGenTextures(1, &img->texture_id);
    glBindTexture(GL_TEXTURE_2D, img->texture_id);

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, data);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

    glBindTexture(GL_TEXTURE_2D, 0);
    stbi_image_free(data);

    return (PyObject*)img;
}

static PyMethodDef ImageModuleMethods[] = {
    {"newImage", image_newImage, METH_VARARGS, "Load an image file (filename) -> Image"},
    {nullptr, nullptr, 0, nullptr}
};

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

static PyObject* graphics_drawImage(PyObject* self, PyObject* args, PyObject* kwargs) {
    PyObject* image_obj;
    float x = 0.0f, y = 0.0f;
    float r = 0.0f, sx = 1.0f, sy = 1.0f;
    float ox = 0.0f, oy = 0.0f;

    static const char* kwlist[] = {"image", "x", "y", "r", "sx", "sy", "ox", "oy", nullptr};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O|ffffff", (char**)kwlist,
                                     &image_obj, &x, &y, &r, &sx, &sy, &ox, &oy))
        return nullptr;

    if (!PyObject_TypeCheck(image_obj, &ImageType)) {
        PyErr_SetString(PyExc_TypeError, "Expected Image object");
        return nullptr;
    }

    ImageObject* img = (ImageObject*)image_obj;

    glEnable(GL_TEXTURE_2D);
    glBindTexture(GL_TEXTURE_2D, img->texture_id);

    glPushMatrix();
    glTranslatef(x, y, 0.0f);
    glRotatef(r * 180.0f / 3.14159f, 0.0f, 0.0f, 1.0f);
    glScalef(sx, sy, 1.0f);
    glTranslatef(-ox, -oy, 0.0f);

    float w = (float)img->width;
    float h = (float)img->height;

    glBegin(GL_QUADS);
    glTexCoord2f(0.0f, 0.0f); glVertex2f(0.0f, 0.0f);
    glTexCoord2f(1.0f, 0.0f); glVertex2f(w, 0.0f);
    glTexCoord2f(1.0f, 1.0f); glVertex2f(w, h);
    glTexCoord2f(0.0f, 1.0f); glVertex2f(0.0f, h);
    glEnd();

    glPopMatrix();
    glBindTexture(GL_TEXTURE_2D, 0);
    glDisable(GL_TEXTURE_2D);

    Py_RETURN_NONE;
}

static PyObject* graphics_print(PyObject* self, PyObject* args) {
    const char* text;
    float x, y;
    float r = 0.0f;
    float sx = 1.0f, sy = 1.0f;
    
    if (!PyArg_ParseTuple(args, "sff|fff", &text, &x, &y, &r, &sx, &sy))
        return nullptr;
    
    if (!g_state.current_font || !PyObject_IsInstance(g_state.current_font, (PyObject*)&FontType)) {
        Py_RETURN_NONE;
    }
    
    FontObject* font = (FontObject*)g_state.current_font;
    
    // Get baseline from font metrics
    float baseline = 0.0f;
    if (font->face && font->face->size) {
        baseline = (font->face->size->metrics.ascender >> 6);
    }
    
    glEnable(GL_TEXTURE_2D);
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    
    // Simple texture environment - just modulate
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE);
    
    // Use the current color for text (white = use texture alpha with full color)
    glColor4f(g_state.color_r, g_state.color_g, g_state.color_b, g_state.color_a);
    
    glPushMatrix();
    glTranslatef(x, y, 0.0f);
    glRotatef(r * 180.0f / 3.14159f, 0.0f, 0.0f, 1.0f);
    glScalef(sx, sy, 1.0f);
    
    float cursor_x = 0.0f;
    
    for (const char* p = text; *p; p++) {
        unsigned char c = (unsigned char)*p;
        if (c >= 128 || font->characters[c].texture_id == 0) {
            // Handle space specially
            if (c == ' ' && font->face) {
                cursor_x += (font->characters['a'].advance >> 6) * 0.5f;
            }
            continue;
        }
        
        Character* ch = &font->characters[c];
        
        // Calculate position
        // Note: OpenGL y=0 is at top (inverted from FreeTYpe), so we flip y
        // bearing_y is distance from baseline to top of glyph (positive upward in FreeType)
        // In OpenGL Y-down, we need: baseline - bearing_y to position glyph correctly
        float xpos = cursor_x + ch->bearing_x;
        float ypos = baseline - ch->bearing_y;  // Correct: distance down from baseline to glyph top
        float w = (float)ch->width;
        float h = (float)ch->height;
        
        // Draw textured quad
        // FreeType bitmap origin is at top-left, so we need to flip V coordinates
        glBindTexture(GL_TEXTURE_2D, ch->texture_id);
        glBegin(GL_QUADS);
        glTexCoord2f(0.0f, 0.0f); glVertex2f(xpos, ypos);         // Top-left vertex uses top-left texcoord
        glTexCoord2f(1.0f, 0.0f); glVertex2f(xpos + w, ypos);     // Top-right vertex uses top-right texcoord
        glTexCoord2f(1.0f, 1.0f); glVertex2f(xpos + w, ypos + h); // Bottom-right vertex uses bottom-right texcoord
        glTexCoord2f(0.0f, 1.0f); glVertex2f(xpos, ypos + h);     // Bottom-left vertex uses bottom-left texcoord
        glEnd();
        
        // Advance cursor (advance is in 26.6 fixed point format)
        cursor_x += (ch->advance >> 6);
    }
    
    glPopMatrix();
    glBindTexture(GL_TEXTURE_2D, 0);
    glDisable(GL_TEXTURE_2D);
    glDisable(GL_BLEND);
    
    Py_RETURN_NONE;
}

static PyObject* graphics_setFont(PyObject* self, PyObject* args) {
    PyObject* font_obj;
    if (!PyArg_ParseTuple(args, "O", &font_obj))
        return nullptr;
    
    if (!PyObject_IsInstance(font_obj, (PyObject*)&FontType)) {
        PyErr_SetString(PyExc_TypeError, "Expected Font object");
        return nullptr;
    }
    
    Py_XDECREF(g_state.current_font);
    g_state.current_font = font_obj;
    Py_INCREF(font_obj);
    
    Py_RETURN_NONE;
}

static PyObject* createDefaultFont(int size = 13);

static PyObject* graphics_getFont(PyObject* self, PyObject* args) {
    // If we already have a current font, return it
    if (g_state.current_font) {
        Py_INCREF(g_state.current_font);
        return g_state.current_font;
    }
    
    // Create default font if we don't have one cached (use larger size for better quality)
    if (!g_state.default_font) {
        g_state.default_font = createDefaultFont(16);
        if (!g_state.default_font) {
            // Failed to create default font
            PyErr_Clear();  // Clear the error so we can return None
            Py_RETURN_NONE;
        }
    }
    
    // Use the cached default font as current font
    Py_INCREF(g_state.default_font);
    g_state.current_font = g_state.default_font;
    
    Py_INCREF(g_state.current_font);
    return g_state.current_font;
}

// Create default font from embedded resources
static PyObject* createDefaultFont(int size) {
    // Try multiple possible paths for the default font
    const char* possible_paths[] = {
        "resources/font.ttf",
        "../resources/font.ttf",
        "../../resources/font.ttf",
        "./resources/font.ttf",
        nullptr
    };
    
    for (int i = 0; possible_paths[i] != nullptr; i++) {
        struct stat buffer;
        if (stat(possible_paths[i], &buffer) == 0) {
            // File exists, try to load it
            PyObject* args = Py_BuildValue("(si)", possible_paths[i], size);
            if (!args) continue;
            
            PyObject* font = font_newFont(nullptr, args);
            Py_DECREF(args);
            
            if (font) {
                return font;
            }
            PyErr_Clear();  // Clear error and try next path
        }
    }
    
    // Could not find default font
    PyErr_SetString(PyExc_RuntimeError, "Could not load default font from resources/font.ttf");
    return nullptr;
}

static PyObject* graphics_newFont(PyObject* self, PyObject* args) {
    return font_newFont(self, args);
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
    {"drawImage", (PyCFunction)graphics_drawImage, METH_VARARGS | METH_KEYWORDS, "Draw image (image, x=0, y=0, r=0, sx=1, sy=1, ox=0, oy=0)"},
    {"print", graphics_print, METH_VARARGS, "Print text (text, x, y, r=0, sx=1, sy=1)"},
    {"setFont", graphics_setFont, METH_VARARGS, "Set current font"},
    {"getFont", graphics_getFont, METH_NOARGS, "Get current font"},
    {"newFont", graphics_newFont, METH_VARARGS, "Create new font (filename, size=12)"},
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
    const bool* state = SDL_GetKeyboardState(nullptr);
    
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
    float x, y;
    SDL_GetMouseState(&x, &y);
    return Py_BuildValue("(ii)", (int)x, (int)y);
}

static PyObject* mouse_getX(PyObject* self, PyObject* args) {
    float x, y;
    SDL_GetMouseState(&x, &y);
    return PyLong_FromLong((int)x);
}

static PyObject* mouse_getY(PyObject* self, PyObject* args) {
    float x, y;
    SDL_GetMouseState(&x, &y);
    return PyLong_FromLong((int)y);
}

static PyObject* mouse_isDown(PyObject* self, PyObject* args) {
    int button;
    if (!PyArg_ParseTuple(args, "i", &button))
        return nullptr;
    
    SDL_MouseButtonFlags state = SDL_GetMouseState(nullptr, nullptr);
    if (state & SDL_BUTTON_MASK(button)) {
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
    event.type = SDL_EVENT_QUIT;
    SDL_PushEvent(&event);
    Py_RETURN_NONE;
}

static PyMethodDef EventMethods[] = {
    {"quit", event_quit, METH_NOARGS, "Push quit event"},
    {nullptr, nullptr, 0, nullptr}
};

// ============================================================================
// Filesystem Module Functions (C++17)
// ============================================================================

#include <fstream>
#include <sstream>

static PyObject* filesystem_read(PyObject* self, PyObject* args) {
    const char* filename;
    if (!PyArg_ParseTuple(args, "s", &filename))
        return nullptr;
    
    std::ifstream file(filename, std::ios::binary);
    if (!file.is_open()) {
        PyErr_SetString(PyExc_FileNotFoundError, "Could not open file");
        return nullptr;
    }
    
    std::stringstream buffer;
    buffer << file.rdbuf();
    std::string content = buffer.str();
    
    return PyUnicode_FromStringAndSize(content.c_str(), content.size());
}

static PyObject* filesystem_write(PyObject* self, PyObject* args) {
    const char* filename;
    const char* data;
    Py_ssize_t data_len;
    if (!PyArg_ParseTuple(args, "ss#", &filename, &data, &data_len))
        return nullptr;
    
    std::ofstream file(filename, std::ios::binary);
    if (!file.is_open()) {
        PyErr_SetString(PyExc_IOError, "Could not open file for writing");
        return nullptr;
    }
    
    file.write(data, data_len);
    file.close();
    
    Py_RETURN_TRUE;
}

static PyObject* filesystem_exists(PyObject* self, PyObject* args) {
    const char* path;
    if (!PyArg_ParseTuple(args, "s", &path))
        return nullptr;
    
    struct stat buffer;
    if (stat(path, &buffer) == 0) {
        Py_RETURN_TRUE;
    }
    Py_RETURN_FALSE;
}

static PyObject* filesystem_isFile(PyObject* self, PyObject* args) {
    const char* path;
    if (!PyArg_ParseTuple(args, "s", &path))
        return nullptr;
    
    struct stat buffer;
    if (stat(path, &buffer) == 0) {
        if (S_ISREG(buffer.st_mode)) {
            Py_RETURN_TRUE;
        }
    }
    Py_RETURN_FALSE;
}

static PyObject* filesystem_isDirectory(PyObject* self, PyObject* args) {
    const char* path;
    if (!PyArg_ParseTuple(args, "s", &path))
        return nullptr;
    
    struct stat buffer;
    if (stat(path, &buffer) == 0) {
        if (S_ISDIR(buffer.st_mode)) {
            Py_RETURN_TRUE;
        }
    }
    Py_RETURN_FALSE;
}

static PyObject* filesystem_createDirectory(PyObject* self, PyObject* args) {
    const char* name;
    if (!PyArg_ParseTuple(args, "s", &name))
        return nullptr;
    
    #if defined(_WIN32)
        int result = mkdir(name);
    #else
        int result = mkdir(name, 0755);
    #endif
    
    if (result == 0) {
        Py_RETURN_TRUE;
    } else {
        PyErr_SetString(PyExc_IOError, "Failed to create directory");
        return nullptr;
    }
}

static PyObject* filesystem_getWorkingDirectory(PyObject* self, PyObject* args) {
    char cwd[4096];
    if (getcwd(cwd, sizeof(cwd)) != nullptr) {
        return PyUnicode_FromString(cwd);
    } else {
        PyErr_SetString(PyExc_IOError, "Failed to get working directory");
        return nullptr;
    }
}

static PyObject* filesystem_getDirectoryItems(PyObject* self, PyObject* args) {
    const char* dir;
    if (!PyArg_ParseTuple(args, "s", &dir))
        return nullptr;
    
    PyObject* list = PyList_New(0);
    if (!list) return nullptr;
    
    #if defined(_WIN32)
        WIN32_FIND_DATA findData;
        char searchPath[4096];
        snprintf(searchPath, sizeof(searchPath), "%s/*", dir);
        HANDLE hFind = FindFirstFile(searchPath, &findData);
        
        if (hFind != INVALID_HANDLE_VALUE) {
            do {
                PyObject* name = PyUnicode_FromString(findData.cFileName);
                if (name) {
                    PyList_Append(list, name);
                    Py_DECREF(name);
                }
            } while (FindNextFile(hFind, &findData));
            FindClose(hFind);
        }
    #else
        DIR* d = opendir(dir);
        if (d) {
            struct dirent* entry;
            while ((entry = readdir(d)) != nullptr) {
                PyObject* name = PyUnicode_FromString(entry->d_name);
                if (name) {
                    PyList_Append(list, name);
                    Py_DECREF(name);
                }
            }
            closedir(d);
        }
    #endif
    
    return list;
}

static PyMethodDef FilesystemMethods[] = {
    {"read", filesystem_read, METH_VARARGS, "Read file contents"},
    {"write", filesystem_write, METH_VARARGS, "Write data to file"},
    {"exists", filesystem_exists, METH_VARARGS, "Check if path exists"},
    {"isFile", filesystem_isFile, METH_VARARGS, "Check if path is a file"},
    {"isDirectory", filesystem_isDirectory, METH_VARARGS, "Check if path is a directory"},
    {"createDirectory", filesystem_createDirectory, METH_VARARGS, "Create a directory"},
    {"getWorkingDirectory", filesystem_getWorkingDirectory, METH_NOARGS, "Get current working directory"},
    {"getDirectoryItems", filesystem_getDirectoryItems, METH_VARARGS, "List files in directory"},
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

static PyModuleDef FilesystemModule = {
    PyModuleDef_HEAD_INIT, "love.filesystem", nullptr, -1, FilesystemMethods
};

static PyModuleDef ImageModule = {
    PyModuleDef_HEAD_INIT, "love.image", nullptr, -1, ImageModuleMethods
};

static PyModuleDef FontModule = {
    PyModuleDef_HEAD_INIT, "love.font", nullptr, -1, FontModuleMethods
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
    PyObject* filesystem = PyModule_Create(&FilesystemModule);
    PyObject* image = PyModule_Create(&ImageModule);
    PyObject* font = PyModule_Create(&FontModule);
    
    if (graphics) PyModule_AddObject(love, "graphics", graphics);
    if (window) PyModule_AddObject(love, "window", window);
    if (timer) PyModule_AddObject(love, "timer", timer);
    if (keyboard) PyModule_AddObject(love, "keyboard", keyboard);
    if (mouse) PyModule_AddObject(love, "mouse", mouse);
    if (event) PyModule_AddObject(love, "event", event);
    if (filesystem) PyModule_AddObject(love, "filesystem", filesystem);
    if (image) PyModule_AddObject(love, "image", image);
    if (font) PyModule_AddObject(love, "font", font);
    
    // Initialize Image type
    if (PyType_Ready(&ImageType) < 0) {
        return nullptr;
    }
    Py_INCREF(&ImageType);
    PyModule_AddObject(image, "Image", (PyObject*)&ImageType);
    
    // Initialize Font type
    if (PyType_Ready(&FontType) < 0) {
        return nullptr;
    }
    Py_INCREF(&FontType);
    PyModule_AddObject(font, "Font", (PyObject*)&FontType);
    
    // Add version
    PyModule_AddStringConstant(love, "__version__", "11.5.0");
    
    return love;
}

// ============================================================================
// SDL and Game Loop
// ============================================================================

bool initSDL() {
    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        std::cerr << "SDL_Init failed: " << SDL_GetError() << std::endl;
        return false;
    }
    
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_MAJOR_VERSION, 2);
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_MINOR_VERSION, 1);
    SDL_GL_SetAttribute(SDL_GL_DOUBLEBUFFER, 1);
    SDL_GL_SetAttribute(SDL_GL_DEPTH_SIZE, 24);
    
    g_state.window = SDL_CreateWindow(
        g_state.title.c_str(),
        g_state.width,
        g_state.height,
        SDL_WINDOW_OPENGL
    );
    
    if (g_state.window) {
        SDL_SetWindowPosition(g_state.window, SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED);
    }
    
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
    // Cleanup fonts (must be done before FreeType cleanup)
    Py_XDECREF(g_state.current_font);
    g_state.current_font = nullptr;
    
    Py_XDECREF(g_state.default_font);
    g_state.default_font = nullptr;
    
    if (ft_library) {
        FT_Done_FreeType(ft_library);
        ft_library = nullptr;
    }
    
    if (g_state.gl_context) {
        SDL_GL_DestroyContext(g_state.gl_context);
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
    
    Uint64 last_time = SDL_GetTicks();
    
    while (g_state.running) {
        Uint64 current_time = SDL_GetTicks();
        double dt = (current_time - last_time) / 1000.0;
        last_time = current_time;
        
        SDL_Event event;
        while (SDL_PollEvent(&event)) {
            switch (event.type) {
                case SDL_EVENT_QUIT:
                    g_state.running = false;
                    break;
                    
                case SDL_EVENT_KEY_DOWN:
                    if (event.key.key == SDLK_ESCAPE) {
                        g_state.running = false;
                    }
                    if (g_state.py_keypressed) {
                        const char* key = SDL_GetKeyName(event.key.key);
                        callPythonKeyCallback(g_state.py_keypressed, key, 
                                            event.key.scancode, 
                                            event.key.repeat != 0);
                    }
                    break;
                    
                case SDL_EVENT_KEY_UP:
                    if (g_state.py_keyreleased) {
                        const char* key = SDL_GetKeyName(event.key.key);
                        callPythonKeyCallback(g_state.py_keyreleased, key,
                                            event.key.scancode, false);
                    }
                    break;
                    
                case SDL_EVENT_MOUSE_BUTTON_DOWN:
                    if (g_state.py_mousepressed) {
                        float x, y;
                        SDL_GetMouseState(&x, &y);
                        callPythonMouseCallback(g_state.py_mousepressed, (int)x, (int)y,
                                              event.button.button,
                                              false,  // SDL3 doesn't have which field the same way
                                              event.button.clicks);
                    }
                    break;
                    
                case SDL_EVENT_MOUSE_BUTTON_UP:
                    if (g_state.py_mousereleased) {
                        float x, y;
                        SDL_GetMouseState(&x, &y);
                        callPythonMouseCallback(g_state.py_mousereleased, (int)x, (int)y,
                                              event.button.button,
                                              false,  // SDL3 doesn't have which field the same way
                                              event.button.clicks);
                    }
                    break;
                    
                case SDL_EVENT_MOUSE_MOTION:
                    if (g_state.py_mousemoved) {
                        callPythonMouseCallback(g_state.py_mousemoved, 
                                              (int)event.motion.x, (int)event.motion.y,
                                              (int)event.motion.xrel, (int)event.motion.yrel,
                                              false);  // SDL3 doesn't have which field the same way
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
