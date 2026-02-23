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
#include <SDL3/SDL_opengl.h>
#include <iostream>
#include <string>
#include <cstring>
#include <cstdlib>
#include <cmath>
#include <cctype>
#include <sys/stat.h>
#if defined(_WIN32)
    #include <direct.h>
    #include <windows.h>
#elif defined(__APPLE__)
    #include <dirent.h>
    #include <unistd.h>
    #include <mach-o/dyld.h>
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
    Uint64 window_flags = SDL_WINDOW_OPENGL;
    bool vsync = true;
    
    // Graphics state
    float color_r = 1.0f, color_g = 1.0f, color_b = 1.0f, color_a = 1.0f;
    float bg_r = 0.0f, bg_g = 0.0f, bg_b = 0.0f, bg_a = 1.0f;
    bool scissor_enabled = false;
    int scissor_x = 0;
    int scissor_y = 0;
    int scissor_w = 0;
    int scissor_h = 0;
    
    // Python callbacks
    PyObject* py_conf = nullptr;
    PyObject* py_load = nullptr;
    PyObject* py_update = nullptr;
    PyObject* py_draw = nullptr;
    PyObject* py_quit = nullptr;
    PyObject* py_focus = nullptr;
    PyObject* py_resize = nullptr;
    PyObject* py_textinput = nullptr;
    PyObject* py_visible = nullptr;
    PyObject* py_wheelmoved = nullptr;
    PyObject* py_directorydropped = nullptr;
    PyObject* py_filedropped = nullptr;
    PyObject* py_keypressed = nullptr;
    PyObject* py_keyreleased = nullptr;
    PyObject* py_mousepressed = nullptr;
    PyObject* py_mousereleased = nullptr;
    PyObject* py_mousemoved = nullptr;
    
    // Font state
    PyObject* current_font = nullptr;
    PyObject* default_font = nullptr;  // Cached default font
    PyObject* current_canvas = nullptr;

    double last_dt = 0.0;
    double fps = 0.0;
};

static GameState g_state;
static bool g_deprecation_output = false;

static void (*g_glGenFramebuffers)(GLsizei, GLuint*) = nullptr;
static void (*g_glDeleteFramebuffers)(GLsizei, const GLuint*) = nullptr;
static void (*g_glBindFramebuffer)(GLenum, GLuint) = nullptr;
static void (*g_glFramebufferTexture2D)(GLenum, GLenum, GLenum, GLuint, GLint) = nullptr;
static GLenum (*g_glCheckFramebufferStatus)(GLenum) = nullptr;
static void (*g_glGenerateMipmap)(GLenum) = nullptr;

#ifndef GL_FRAMEBUFFER
#define GL_FRAMEBUFFER GL_FRAMEBUFFER_EXT
#endif
#ifndef GL_COLOR_ATTACHMENT0
#define GL_COLOR_ATTACHMENT0 GL_COLOR_ATTACHMENT0_EXT
#endif
#ifndef GL_FRAMEBUFFER_COMPLETE
#define GL_FRAMEBUFFER_COMPLETE GL_FRAMEBUFFER_COMPLETE_EXT
#endif

static void updateGLViewportAndProjection() {
    glViewport(0, 0, g_state.width, g_state.height);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glOrtho(0, g_state.width, g_state.height, 0, -1, 1);
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
}

static void updateGLViewportAndProjectionForSize(int width, int height) {
    glViewport(0, 0, width, height);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glOrtho(0, width, height, 0, -1, 1);
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
}

static void loadOpenGLFunctionPointers() {
    g_glGenFramebuffers = (void (*)(GLsizei, GLuint*))SDL_GL_GetProcAddress("glGenFramebuffers");
    g_glDeleteFramebuffers = (void (*)(GLsizei, const GLuint*))SDL_GL_GetProcAddress("glDeleteFramebuffers");
    g_glBindFramebuffer = (void (*)(GLenum, GLuint))SDL_GL_GetProcAddress("glBindFramebuffer");
    g_glFramebufferTexture2D = (void (*)(GLenum, GLenum, GLenum, GLuint, GLint))SDL_GL_GetProcAddress("glFramebufferTexture2D");
    g_glCheckFramebufferStatus = (GLenum (*)(GLenum))SDL_GL_GetProcAddress("glCheckFramebufferStatus");
    g_glGenerateMipmap = (void (*)(GLenum))SDL_GL_GetProcAddress("glGenerateMipmap");

    if (!g_glGenFramebuffers) g_glGenFramebuffers = (void (*)(GLsizei, GLuint*))SDL_GL_GetProcAddress("glGenFramebuffersEXT");
    if (!g_glDeleteFramebuffers) g_glDeleteFramebuffers = (void (*)(GLsizei, const GLuint*))SDL_GL_GetProcAddress("glDeleteFramebuffersEXT");
    if (!g_glBindFramebuffer) g_glBindFramebuffer = (void (*)(GLenum, GLuint))SDL_GL_GetProcAddress("glBindFramebufferEXT");
    if (!g_glFramebufferTexture2D) g_glFramebufferTexture2D = (void (*)(GLenum, GLenum, GLenum, GLuint, GLint))SDL_GL_GetProcAddress("glFramebufferTexture2DEXT");
    if (!g_glCheckFramebufferStatus) g_glCheckFramebufferStatus = (GLenum (*)(GLenum))SDL_GL_GetProcAddress("glCheckFramebufferStatusEXT");
    if (!g_glGenerateMipmap) g_glGenerateMipmap = (void (*)(GLenum))SDL_GL_GetProcAddress("glGenerateMipmapEXT");
}

static void addToPythonSysPath(const std::string& path) {
    PyObject* sysPath = PySys_GetObject("path");
    if (!sysPath || !PyList_Check(sysPath)) {
        return;
    }

    PyObject* pyPath = PyUnicode_FromString(path.c_str());
    if (!pyPath) {
        PyErr_Clear();
        return;
    }

    if (PyList_Insert(sysPath, 0, pyPath) != 0) {
        PyErr_Clear();
    }
    Py_DECREF(pyPath);
}

static std::string getDirectoryFromPath(const std::string& path) {
    if (path.empty()) return ".";

    size_t pos = path.find_last_of("/\\");
    if (pos == std::string::npos) {
        return ".";
    }
    if (pos == 0) {
        return "/";
    }
    return path.substr(0, pos);
}

#if defined(_WIN32)
static std::wstring getExecutableDirectoryW() {
    wchar_t buffer[MAX_PATH];
    DWORD len = GetModuleFileNameW(nullptr, buffer, MAX_PATH);
    std::wstring full(buffer, len);
    size_t pos = full.find_last_of(L"\\/");
    if (pos == std::wstring::npos) return L".";
    return full.substr(0, pos);
}

static std::string wideToUtf8(const std::wstring& w) {
    if (w.empty()) return {};
    int size = WideCharToMultiByte(CP_UTF8, 0, w.c_str(), (int)w.size(), nullptr, 0, nullptr, nullptr);
    if (size <= 0) return {};
    std::string out((size_t)size, '\0');
    WideCharToMultiByte(CP_UTF8, 0, w.c_str(), (int)w.size(), out.data(), size, nullptr, nullptr);
    return out;
}

static bool pathIsDirectoryW(const std::wstring& path) {
    DWORD attr = GetFileAttributesW(path.c_str());
    return attr != INVALID_FILE_ATTRIBUTES && (attr & FILE_ATTRIBUTE_DIRECTORY);
}

static bool pathIsFileW(const std::wstring& path) {
    DWORD attr = GetFileAttributesW(path.c_str());
    return attr != INVALID_FILE_ATTRIBUTES && !(attr & FILE_ATTRIBUTE_DIRECTORY);
}

static void initializePythonFromEmbeddedRuntimeIfPresent() {
    const char* overrideHome = std::getenv("LOVE_PYTHON_HOME");
    if (overrideHome && *overrideHome) {
        int wsize = MultiByteToWideChar(CP_UTF8, 0, overrideHome, -1, nullptr, 0);
        if (wsize > 0) {
            std::wstring pythonHome((size_t)wsize - 1, L'\0');
            MultiByteToWideChar(CP_UTF8, 0, overrideHome, -1, pythonHome.data(), wsize);
            if (pathIsDirectoryW(pythonHome)) {
                PyStatus status;
                PyConfig config;
                PyConfig_InitPythonConfig(&config);
                config.isolated = 1;
                config.use_environment = 0;
                config.site_import = 0;

                status = PyConfig_SetString(&config, &config.home, pythonHome.c_str());
                if (PyStatus_Exception(status)) {
                    PyConfig_Clear(&config);
                    Py_ExitStatusException(status);
                    return;
                }

                std::wstring exeDir = getExecutableDirectoryW();
                std::wstring programName = exeDir + L"\\love.exe";
                status = PyConfig_SetString(&config, &config.program_name, programName.c_str());
                if (PyStatus_Exception(status)) {
                    PyConfig_Clear(&config);
                    Py_ExitStatusException(status);
                    return;
                }

                status = Py_InitializeFromConfig(&config);
                PyConfig_Clear(&config);
                if (PyStatus_Exception(status)) {
                    Py_ExitStatusException(status);
                    return;
                }

                addToPythonSysPath(wideToUtf8(pythonHome));
                return;
            }
        }
    }

    std::wstring exeDir = getExecutableDirectoryW();
    std::wstring pythonHome = exeDir + L"\\python";
    if (!pathIsDirectoryW(pythonHome)) {
        Py_Initialize();
        return;
    }

    PyStatus status;
    PyConfig config;
    PyConfig_InitPythonConfig(&config);
    config.isolated = 1;
    config.use_environment = 0;
    config.site_import = 0;

    status = PyConfig_SetString(&config, &config.home, pythonHome.c_str());
    if (PyStatus_Exception(status)) {
        PyConfig_Clear(&config);
        Py_ExitStatusException(status);
        return;
    }

    std::wstring programName = exeDir + L"\\love.exe";
    status = PyConfig_SetString(&config, &config.program_name, programName.c_str());
    if (PyStatus_Exception(status)) {
        PyConfig_Clear(&config);
        Py_ExitStatusException(status);
        return;
    }

    status = Py_InitializeFromConfig(&config);
    PyConfig_Clear(&config);
    if (PyStatus_Exception(status)) {
        Py_ExitStatusException(status);
        return;
    }

    addToPythonSysPath(wideToUtf8(pythonHome));
}
#elif defined(__APPLE__)
static bool pathIsDirectory(const std::string& path) {
    struct stat st;
    return stat(path.c_str(), &st) == 0 && S_ISDIR(st.st_mode);
}

static bool pathIsFile(const std::string& path) {
    struct stat st;
    return stat(path.c_str(), &st) == 0 && S_ISREG(st.st_mode);
}

static std::string getExecutableDirectoryUtf8() {
    uint32_t size = 0;
    _NSGetExecutablePath(nullptr, &size);
    std::string tmp(size + 1, '\0');
    if (_NSGetExecutablePath(tmp.data(), &size) != 0) {
        return ".";
    }
    tmp.resize(std::strlen(tmp.c_str()));

    char resolved[4096];
    if (realpath(tmp.c_str(), resolved)) {
        return getDirectoryFromPath(std::string(resolved));
    }
    return getDirectoryFromPath(tmp);
}

static std::string getBundleResourcesDirectoryUtf8() {
    return getExecutableDirectoryUtf8() + "/../Resources";
}

static std::string getDefaultPythonHomeUtf8() {
    std::string exeDir = getExecutableDirectoryUtf8();

    std::string bundlePythonHome = exeDir + "/../Resources/python";
    std::string bundlePythonHomeNested = bundlePythonHome + "/python";
    if (pathIsDirectory(bundlePythonHomeNested)) {
        return bundlePythonHomeNested;
    }
    if (pathIsDirectory(bundlePythonHome)) {
        return bundlePythonHome;
    }

    std::string adjacentPythonHome = exeDir + "/python";
    std::string adjacentPythonHomeNested = adjacentPythonHome + "/python";
    if (pathIsDirectory(adjacentPythonHomeNested)) {
        return adjacentPythonHomeNested;
    }

    return adjacentPythonHome;
}

static void initializePythonFromEmbeddedRuntimeIfPresent(const char* argv0) {
    const char* overrideHome = std::getenv("LOVE_PYTHON_HOME");
    std::string pythonHome;
    if (overrideHome && *overrideHome) {
        pythonHome = overrideHome;
    } else {
        pythonHome = getDefaultPythonHomeUtf8();
    }

    if (!pythonHome.empty() && pathIsDirectory(pythonHome)) {
        PyStatus status;
        PyConfig config;
        PyConfig_InitPythonConfig(&config);
        config.isolated = 1;
        config.use_environment = 0;
        config.site_import = 0;

        status = PyConfig_SetBytesString(&config, &config.home, pythonHome.c_str());
        if (PyStatus_Exception(status)) {
            PyConfig_Clear(&config);
            Py_ExitStatusException(status);
            return;
        }

        status = PyConfig_SetBytesString(&config, &config.program_name, argv0 ? argv0 : "love");
        if (PyStatus_Exception(status)) {
            PyConfig_Clear(&config);
            Py_ExitStatusException(status);
            return;
        }

        status = Py_InitializeFromConfig(&config);
        PyConfig_Clear(&config);
        if (PyStatus_Exception(status)) {
            Py_ExitStatusException(status);
            return;
        }

        addToPythonSysPath(pythonHome);
        std::string builtinPath = pythonHome + "/builtin";
        if (pathIsDirectory(builtinPath)) {
            addToPythonSysPath(builtinPath);
        }
        return;
    }

    Py_Initialize();
}
#endif

static bool argIsDirectory(const std::string& path) {
#if defined(_WIN32)
    DWORD attr = GetFileAttributesA(path.c_str());
    return attr != INVALID_FILE_ATTRIBUTES && (attr & FILE_ATTRIBUTE_DIRECTORY);
#else
    struct stat st;
    return stat(path.c_str(), &st) == 0 && S_ISDIR(st.st_mode);
#endif
}

static bool argIsFile(const std::string& path) {
#if defined(_WIN32)
    DWORD attr = GetFileAttributesA(path.c_str());
    return attr != INVALID_FILE_ATTRIBUTES && !(attr & FILE_ATTRIBUTE_DIRECTORY);
#else
    struct stat st;
    return stat(path.c_str(), &st) == 0 && S_ISREG(st.st_mode);
#endif
}

static bool setWorkingDirectory(const std::string& path) {
#if defined(_WIN32)
    return _chdir(path.c_str()) == 0;
#else
    return chdir(path.c_str()) == 0;
#endif
}

static std::string joinPath(const std::string& dir, const std::string& leaf) {
    if (dir.empty()) {
        return leaf;
    }
    char last = dir.back();
    if (last == '/' || last == '\\') {
        return dir + leaf;
    }
#if defined(_WIN32)
    return dir + "\\" + leaf;
#else
    return dir + "/" + leaf;
#endif
}

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
// Canvas Type Definition
// ============================================================================

typedef struct {
    PyObject_HEAD
    GLuint texture_id;
    GLuint fbo_id;
    int width;
    int height;
} CanvasObject;

static PyObject* graphics_setCanvas(PyObject* self, PyObject* args);

static void canvas_dealloc(PyObject* self) {
    CanvasObject* canvas = (CanvasObject*)self;
    if (canvas->fbo_id != 0 && g_glDeleteFramebuffers) {
        g_glDeleteFramebuffers(1, &canvas->fbo_id);
        canvas->fbo_id = 0;
    }
    if (canvas->texture_id != 0) {
        glDeleteTextures(1, &canvas->texture_id);
        canvas->texture_id = 0;
    }
    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject* canvas_getWidth(PyObject* self, PyObject* args) {
    CanvasObject* canvas = (CanvasObject*)self;
    return PyLong_FromLong(canvas->width);
}

static PyObject* canvas_getHeight(PyObject* self, PyObject* args) {
    CanvasObject* canvas = (CanvasObject*)self;
    return PyLong_FromLong(canvas->height);
}

static PyObject* canvas_getDimensions(PyObject* self, PyObject* args) {
    CanvasObject* canvas = (CanvasObject*)self;
    return Py_BuildValue("(ii)", canvas->width, canvas->height);
}

static PyObject* canvas_generateMipmaps(PyObject* self, PyObject* args) {
    CanvasObject* canvas = (CanvasObject*)self;
    if (!g_glGenerateMipmap) {
        Py_RETURN_NONE;
    }
    glBindTexture(GL_TEXTURE_2D, canvas->texture_id);
    g_glGenerateMipmap(GL_TEXTURE_2D);
    glBindTexture(GL_TEXTURE_2D, 0);
    Py_RETURN_NONE;
}

static PyObject* canvas_getImageData(PyObject* self, PyObject* args) {
    CanvasObject* canvas = (CanvasObject*)self;
    if (!g_glBindFramebuffer) {
        PyErr_SetString(PyExc_RuntimeError, "Framebuffer functions are not available");
        return nullptr;
    }

    const size_t size = (size_t)canvas->width * (size_t)canvas->height * 4;
    std::string buffer(size, '\0');

    PyObject* prev = g_state.current_canvas ? g_state.current_canvas : Py_None;
    Py_INCREF(prev);

    g_glBindFramebuffer(GL_FRAMEBUFFER, canvas->fbo_id);
    glPixelStorei(GL_PACK_ALIGNMENT, 1);
    glReadPixels(0, 0, canvas->width, canvas->height, GL_RGBA, GL_UNSIGNED_BYTE, buffer.data());

    PyObject* restoreArgs = PyTuple_Pack(1, prev);
    Py_DECREF(prev);
    if (!restoreArgs) {
        return nullptr;
    }
    PyObject* restoreRes = graphics_setCanvas(nullptr, restoreArgs);
    Py_DECREF(restoreArgs);
    if (!restoreRes) {
        return nullptr;
    }
    Py_DECREF(restoreRes);

    PyObject* data = PyBytes_FromStringAndSize(buffer.data(), (Py_ssize_t)buffer.size());
    if (!data) return nullptr;
    PyObject* result = Py_BuildValue("(Oii)", data, canvas->width, canvas->height);
    Py_DECREF(data);
    return result;
}

static PyObject* canvas_renderTo(PyObject* self, PyObject* args) {
    PyObject* func = nullptr;
    if (!PyArg_ParseTuple(args, "O", &func)) {
        return nullptr;
    }
    if (!PyCallable_Check(func)) {
        PyErr_SetString(PyExc_TypeError, "Expected a callable");
        return nullptr;
    }

    PyObject* prev = g_state.current_canvas ? g_state.current_canvas : Py_None;
    Py_INCREF(prev);

    PyObject* setArgs = PyTuple_Pack(1, self);
    if (!setArgs) {
        Py_DECREF(prev);
        return nullptr;
    }
    PyObject* setRes = graphics_setCanvas(nullptr, setArgs);
    Py_DECREF(setArgs);
    if (!setRes) {
        Py_DECREF(prev);
        return nullptr;
    }
    Py_DECREF(setRes);

    PyObject* callRes = PyObject_CallObject(func, nullptr);
    if (!callRes) {
        PyObject* restoreArgs = PyTuple_Pack(1, prev);
        Py_DECREF(prev);
        if (restoreArgs) {
            PyObject* restoreRes = graphics_setCanvas(nullptr, restoreArgs);
            Py_DECREF(restoreArgs);
            Py_XDECREF(restoreRes);
        } else {
            PyErr_Clear();
        }
        return nullptr;
    }
    Py_DECREF(callRes);

    PyObject* restoreArgs = PyTuple_Pack(1, prev);
    Py_DECREF(prev);
    if (!restoreArgs) {
        return nullptr;
    }
    PyObject* restoreRes = graphics_setCanvas(nullptr, restoreArgs);
    Py_DECREF(restoreArgs);
    if (!restoreRes) {
        return nullptr;
    }
    Py_DECREF(restoreRes);
    Py_RETURN_NONE;
}

static PyMethodDef CanvasMethods[] = {
    {"getWidth", (PyCFunction)canvas_getWidth, METH_NOARGS, "Get canvas width"},
    {"getHeight", (PyCFunction)canvas_getHeight, METH_NOARGS, "Get canvas height"},
    {"getDimensions", (PyCFunction)canvas_getDimensions, METH_NOARGS, "Get canvas dimensions"},
    {"renderTo", (PyCFunction)canvas_renderTo, METH_VARARGS, "Render to canvas with a function"},
    {"generateMipmaps", (PyCFunction)canvas_generateMipmaps, METH_NOARGS, "Generate mipmaps"},
    {"getImageData", (PyCFunction)canvas_getImageData, METH_NOARGS, "Read back canvas pixels (bytes, width, height)"},
    {nullptr, nullptr, 0, nullptr}
};

static PyTypeObject CanvasType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "love.Canvas",
    .tp_basicsize = sizeof(CanvasObject),
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_doc = "Canvas object",
    .tp_dealloc = canvas_dealloc,
    .tp_methods = CanvasMethods,
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
    int max_bearing_y;
    int max_bearing_bottom;
    int has_glyph_extents;
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
    if (font->has_glyph_extents) {
        return PyLong_FromLong(font->max_bearing_y + font->max_bearing_bottom);
    }
    if (font->face) {
        double h = (double)font->face->size->metrics.height / 64.0;
        return PyLong_FromLong((long)ceil(h));
    }
    return PyLong_FromLong(0);
}

static PyObject* font_getAscent(PyObject* self, PyObject* args) {
    FontObject* font = (FontObject*)self;
    if (font->has_glyph_extents) {
        return PyLong_FromLong(font->max_bearing_y);
    }
    if (font->face) {
        double a = (double)font->face->size->metrics.ascender / 64.0;
        return PyLong_FromLong((long)ceil(a));
    }
    return PyLong_FromLong(0);
}

static PyObject* font_getDescent(PyObject* self, PyObject* args) {
    FontObject* font = (FontObject*)self;
    if (font->has_glyph_extents) {
        return PyLong_FromLong(-font->max_bearing_bottom);
    }
    if (font->face) {
        double d = (double)font->face->size->metrics.descender / 64.0;
        return PyLong_FromLong((long)floor(d));
    }
    return PyLong_FromLong(0);
}

static PyObject* font_getBaseline(PyObject* self, PyObject* args) {
    FontObject* font = (FontObject*)self;
    if (font->has_glyph_extents) {
        return PyLong_FromLong(font->max_bearing_y);
    }
    if (font->face) {
        double a = (double)font->face->size->metrics.ascender / 64.0;
        return PyLong_FromLong((long)ceil(a));
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
        unsigned char c = (unsigned char)*p;
        if (c < 128) {
            int adv = (int)(font->characters[c].advance >> 6);
            if (c == ' ' && font->characters['a'].advance != 0) {
                int half_a = (int)((font->characters['a'].advance >> 6) * 0.5f);
                if (half_a > adv) {
                    adv = half_a;
                }
            }
            width += (float)adv;
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
    {"getAscent", (PyCFunction)font_getAscent, METH_NOARGS, "Get font ascent"},
    {"getDescent", (PyCFunction)font_getDescent, METH_NOARGS, "Get font descent"},
    {"getBaseline", (PyCFunction)font_getBaseline, METH_NOARGS, "Get font baseline"},
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
    font->max_bearing_y = 0;
    font->max_bearing_bottom = 0;
    font->has_glyph_extents = 0;

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

        if (width > 0 && height > 0 && texture != 0) {
            int top = font->characters[c].bearing_y;
            if (top < 0) top = 0;
            int bottom = height - font->characters[c].bearing_y;
            if (bottom < 0) bottom = 0;
            if (top > font->max_bearing_y) font->max_bearing_y = top;
            if (bottom > font->max_bearing_bottom) font->max_bearing_bottom = bottom;
            font->has_glyph_extents = 1;
        }
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

static int getCurrentTargetHeight() {
    if (g_state.current_canvas && g_state.current_canvas != Py_None && PyObject_TypeCheck(g_state.current_canvas, &CanvasType)) {
        CanvasObject* canvas = (CanvasObject*)g_state.current_canvas;
        return canvas->height;
    }
    return g_state.height;
}

static PyObject* graphics_setScissor(PyObject* self, PyObject* args) {
    Py_ssize_t n = PyTuple_Size(args);
    if (n == 0) {
        glDisable(GL_SCISSOR_TEST);
        g_state.scissor_enabled = false;
        g_state.scissor_x = 0;
        g_state.scissor_y = 0;
        g_state.scissor_w = 0;
        g_state.scissor_h = 0;
        Py_RETURN_NONE;
    }

    int x = 0;
    int y = 0;
    int w = 0;
    int h = 0;
    if (!PyArg_ParseTuple(args, "iiii", &x, &y, &w, &h)) {
        return nullptr;
    }
    if (w < 0 || h < 0) {
        PyErr_SetString(PyExc_ValueError, "Scissor width/height must be non-negative");
        return nullptr;
    }

    const int target_h = getCurrentTargetHeight();
    glEnable(GL_SCISSOR_TEST);
    glScissor(x, target_h - y - h, w, h);
    g_state.scissor_enabled = true;
    g_state.scissor_x = x;
    g_state.scissor_y = y;
    g_state.scissor_w = w;
    g_state.scissor_h = h;
    Py_RETURN_NONE;
}

static PyObject* graphics_getScissor(PyObject* self, PyObject* args) {
    if (!g_state.scissor_enabled) {
        Py_RETURN_NONE;
    }
    return Py_BuildValue("(iiii)", g_state.scissor_x, g_state.scissor_y, g_state.scissor_w, g_state.scissor_h);
}

static PyObject* graphics_intersectScissor(PyObject* self, PyObject* args) {
    int x = 0;
    int y = 0;
    int w = 0;
    int h = 0;
    if (!PyArg_ParseTuple(args, "iiii", &x, &y, &w, &h)) {
        return nullptr;
    }
    if (w < 0 || h < 0) {
        PyErr_SetString(PyExc_ValueError, "Scissor width/height must be non-negative");
        return nullptr;
    }

    if (!g_state.scissor_enabled) {
        PyObject* t = Py_BuildValue("(iiii)", x, y, w, h);
        if (!t) return nullptr;
        PyObject* r = graphics_setScissor(self, t);
        Py_DECREF(t);
        return r;
    }

    const int left = (g_state.scissor_x > x) ? g_state.scissor_x : x;
    const int top = (g_state.scissor_y > y) ? g_state.scissor_y : y;
    const int right = ((g_state.scissor_x + g_state.scissor_w) < (x + w)) ? (g_state.scissor_x + g_state.scissor_w) : (x + w);
    const int bottom = ((g_state.scissor_y + g_state.scissor_h) < (y + h)) ? (g_state.scissor_y + g_state.scissor_h) : (y + h);

    const int iw = (right > left) ? (right - left) : 0;
    const int ih = (bottom > top) ? (bottom - top) : 0;

    PyObject* t = Py_BuildValue("(iiii)", left, top, iw, ih);
    if (!t) return nullptr;
    PyObject* r = graphics_setScissor(self, t);
    Py_DECREF(t);
    return r;
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

    GLuint texture_id = 0;
    int drawable_width = 0;
    int drawable_height = 0;
    if (PyObject_TypeCheck(image_obj, &ImageType)) {
        ImageObject* img = (ImageObject*)image_obj;
        texture_id = img->texture_id;
        drawable_width = img->width;
        drawable_height = img->height;
    } else if (PyObject_TypeCheck(image_obj, &CanvasType)) {
        CanvasObject* canvas = (CanvasObject*)image_obj;
        texture_id = canvas->texture_id;
        drawable_width = canvas->width;
        drawable_height = canvas->height;
    } else {
        PyErr_SetString(PyExc_TypeError, "Expected Image or Canvas object");
        return nullptr;
    }

    glEnable(GL_TEXTURE_2D);
    glBindTexture(GL_TEXTURE_2D, texture_id);

    glPushMatrix();
    glTranslatef(x, y, 0.0f);
    glRotatef(r * 180.0f / 3.14159f, 0.0f, 0.0f, 1.0f);
    glScalef(sx, sy, 1.0f);
    glTranslatef(-ox, -oy, 0.0f);

    float w = (float)drawable_width;
    float h = (float)drawable_height;

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

static PyObject* graphics_drawImageRegion(PyObject* self, PyObject* args, PyObject* kwargs) {
    PyObject* image_obj;
    float src_x = 0.0f;
    float src_y = 0.0f;
    float src_w = 0.0f;
    float src_h = 0.0f;
    float x = 0.0f;
    float y = 0.0f;
    float r = 0.0f;
    float scale_x = 1.0f;
    float scale_y = 1.0f;
    float ox = 0.0f;
    float oy = 0.0f;

    static const char* kwlist[] = {
        "image",
        "sx",
        "sy",
        "sw",
        "sh",
        "x",
        "y",
        "r",
        "scale_x",
        "scale_y",
        "ox",
        "oy",
        nullptr
    };

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "Offff|fffffff", (char**)kwlist,
                                     &image_obj, &src_x, &src_y, &src_w, &src_h,
                                     &x, &y, &r, &scale_x, &scale_y, &ox, &oy)) {
        return nullptr;
    }

    if (src_w <= 0.0f || src_h <= 0.0f) {
        PyErr_SetString(PyExc_ValueError, "Source width and height must be positive");
        return nullptr;
    }

    GLuint texture_id = 0;
    int drawable_width = 0;
    int drawable_height = 0;
    if (PyObject_TypeCheck(image_obj, &ImageType)) {
        ImageObject* img = (ImageObject*)image_obj;
        texture_id = img->texture_id;
        drawable_width = img->width;
        drawable_height = img->height;
    } else if (PyObject_TypeCheck(image_obj, &CanvasType)) {
        CanvasObject* canvas = (CanvasObject*)image_obj;
        texture_id = canvas->texture_id;
        drawable_width = canvas->width;
        drawable_height = canvas->height;
    } else {
        PyErr_SetString(PyExc_TypeError, "Expected Image or Canvas object");
        return nullptr;
    }

    if (drawable_width <= 0 || drawable_height <= 0) {
        PyErr_SetString(PyExc_RuntimeError, "Drawable has invalid dimensions");
        return nullptr;
    }

    float u0 = src_x / (float)drawable_width;
    float v0 = src_y / (float)drawable_height;
    float u1 = (src_x + src_w) / (float)drawable_width;
    float v1 = (src_y + src_h) / (float)drawable_height;

    glEnable(GL_TEXTURE_2D);
    glBindTexture(GL_TEXTURE_2D, texture_id);

    glPushMatrix();
    glTranslatef(x, y, 0.0f);
    glRotatef(r * 180.0f / 3.14159f, 0.0f, 0.0f, 1.0f);
    glScalef(scale_x, scale_y, 1.0f);
    glTranslatef(-ox, -oy, 0.0f);

    float w = src_w;
    float h = src_h;

    glBegin(GL_QUADS);
    glTexCoord2f(u0, v0); glVertex2f(0.0f, 0.0f);
    glTexCoord2f(u1, v0); glVertex2f(w, 0.0f);
    glTexCoord2f(u1, v1); glVertex2f(w, h);
    glTexCoord2f(u0, v1); glVertex2f(0.0f, h);
    glEnd();

    glPopMatrix();
    glBindTexture(GL_TEXTURE_2D, 0);
    glDisable(GL_TEXTURE_2D);

    Py_RETURN_NONE;
}

static PyObject* graphics_newCanvas(PyObject* self, PyObject* args) {
    int width = 0;
    int height = 0;
    if (!PyArg_ParseTuple(args, "ii", &width, &height)) {
        return nullptr;
    }
    if (width <= 0 || height <= 0) {
        PyErr_SetString(PyExc_ValueError, "Canvas size must be positive");
        return nullptr;
    }
    if (!g_glGenFramebuffers || !g_glBindFramebuffer || !g_glFramebufferTexture2D || !g_glCheckFramebufferStatus) {
        PyErr_SetString(PyExc_RuntimeError, "Framebuffer functions are not available");
        return nullptr;
    }

    CanvasObject* canvas = PyObject_New(CanvasObject, &CanvasType);
    if (!canvas) {
        return nullptr;
    }
    canvas->texture_id = 0;
    canvas->fbo_id = 0;
    canvas->width = width;
    canvas->height = height;

    glGenTextures(1, &canvas->texture_id);
    glBindTexture(GL_TEXTURE_2D, canvas->texture_id);
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, nullptr);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);
    glBindTexture(GL_TEXTURE_2D, 0);

    g_glGenFramebuffers(1, &canvas->fbo_id);
    g_glBindFramebuffer(GL_FRAMEBUFFER, canvas->fbo_id);
    g_glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, canvas->texture_id, 0);
    GLenum status = g_glCheckFramebufferStatus(GL_FRAMEBUFFER);
    g_glBindFramebuffer(GL_FRAMEBUFFER, 0);
    updateGLViewportAndProjection();

    if (status != GL_FRAMEBUFFER_COMPLETE) {
        Py_DECREF(canvas);
        PyErr_SetString(PyExc_RuntimeError, "Failed to create framebuffer for canvas");
        return nullptr;
    }

    return (PyObject*)canvas;
}

static PyObject* graphics_getCanvas(PyObject* self, PyObject* args) {
    if (!g_state.current_canvas || g_state.current_canvas == Py_None) {
        Py_RETURN_NONE;
    }
    Py_INCREF(g_state.current_canvas);
    return g_state.current_canvas;
}

static PyObject* graphics_setCanvas(PyObject* self, PyObject* args) {
    Py_ssize_t n = PyTuple_Size(args);
    PyObject* canvas_obj = nullptr;
    if (n >= 1) {
        canvas_obj = PyTuple_GetItem(args, 0);
    }

    if (!g_glBindFramebuffer) {
        PyErr_SetString(PyExc_RuntimeError, "Framebuffer functions are not available");
        return nullptr;
    }

    if (n == 0 || !canvas_obj || canvas_obj == Py_None) {
        g_glBindFramebuffer(GL_FRAMEBUFFER, 0);
        updateGLViewportAndProjection();
        Py_XDECREF(g_state.current_canvas);
        g_state.current_canvas = nullptr;
        Py_RETURN_NONE;
    }

    if (!PyObject_TypeCheck(canvas_obj, &CanvasType)) {
        PyErr_SetString(PyExc_TypeError, "Expected Canvas or None");
        return nullptr;
    }

    CanvasObject* canvas = (CanvasObject*)canvas_obj;
    g_glBindFramebuffer(GL_FRAMEBUFFER, canvas->fbo_id);
    updateGLViewportAndProjectionForSize(canvas->width, canvas->height);

    Py_XDECREF(g_state.current_canvas);
    g_state.current_canvas = canvas_obj;
    Py_INCREF(canvas_obj);

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
    
    float baseline = 0.0f;
    if (font->has_glyph_extents) {
        baseline = (float)font->max_bearing_y;
    } else if (font->face && font->face->size) {
        baseline = (float)ceil((double)font->face->size->metrics.ascender / 64.0);
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
        if (c >= 128) {
            continue;
        }
        
        Character* ch = &font->characters[c];

        if (ch->texture_id != 0 && ch->width > 0 && ch->height > 0) {
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
        }
        
        // Advance cursor (advance is in 26.6 fixed point format)
        int adv = (int)(ch->advance >> 6);
        if (c == ' ' && font->characters['a'].advance != 0) {
            int half_a = (int)((font->characters['a'].advance >> 6) * 0.5f);
            if (half_a > adv) {
                adv = half_a;
            }
        }
        cursor_x += (float)adv;
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
    {"setScissor", graphics_setScissor, METH_VARARGS, "Set scissor rectangle (x, y, w, h) or clear ()"},
    {"getScissor", graphics_getScissor, METH_NOARGS, "Get scissor rectangle or None"},
    {"intersectScissor", graphics_intersectScissor, METH_VARARGS, "Intersect current scissor with (x, y, w, h)"},
    {"getWidth", graphics_getWidth, METH_NOARGS, "Get screen width"},
    {"getHeight", graphics_getHeight, METH_NOARGS, "Get screen height"},
    {"getDimensions", graphics_getDimensions, METH_NOARGS, "Get screen dimensions"},
    {"drawImage", (PyCFunction)graphics_drawImage, METH_VARARGS | METH_KEYWORDS, "Draw image (image, x=0, y=0, r=0, sx=1, sy=1, ox=0, oy=0)"},
    {"drawImageRegion", (PyCFunction)graphics_drawImageRegion, METH_VARARGS | METH_KEYWORDS, "Draw image region (image, sx, sy, sw, sh, x=0, y=0, r=0, scale_x=1, scale_y=1, ox=0, oy=0)"},
    {"print", graphics_print, METH_VARARGS, "Print text (text, x, y, r=0, sx=1, sy=1)"},
    {"setFont", graphics_setFont, METH_VARARGS, "Set current font"},
    {"getFont", graphics_getFont, METH_NOARGS, "Get current font"},
    {"newFont", graphics_newFont, METH_VARARGS, "Create new font (filename, size=12)"},
    {"newCanvas", graphics_newCanvas, METH_VARARGS, "Create new canvas (width, height)"},
    {"setCanvas", graphics_setCanvas, METH_VARARGS, "Set active canvas (canvas or None)"},
    {"getCanvas", graphics_getCanvas, METH_NOARGS, "Get active canvas"},
    {nullptr, nullptr, 0, nullptr}
};

// ============================================================================
// Window Module Functions
// ============================================================================

static void applyWindowFlagsFromDict(PyObject* flags) {
    if (!flags || flags == Py_None) {
        return;
    }

    if (!PyDict_Check(flags)) {
        PyErr_SetString(PyExc_TypeError, "flags must be a dict");
        return;
    }

    PyObject* fullscreen = PyDict_GetItemString(flags, "fullscreen");
    if (fullscreen) {
        int enabled = PyObject_IsTrue(fullscreen);
        if (enabled == 1) {
            g_state.window_flags |= SDL_WINDOW_FULLSCREEN;
        } else if (enabled == 0) {
            g_state.window_flags &= ~SDL_WINDOW_FULLSCREEN;
        }
    }

    PyObject* resizable = PyDict_GetItemString(flags, "resizable");
    if (resizable) {
        int enabled = PyObject_IsTrue(resizable);
        if (enabled == 1) {
            g_state.window_flags |= SDL_WINDOW_RESIZABLE;
        } else if (enabled == 0) {
            g_state.window_flags &= ~SDL_WINDOW_RESIZABLE;
        }
    }

    PyObject* vsync = PyDict_GetItemString(flags, "vsync");
    if (vsync) {
        int enabled = PyObject_IsTrue(vsync);
        if (enabled == 1) {
            g_state.vsync = true;
        } else if (enabled == 0) {
            g_state.vsync = false;
        }
    }
}

static PyObject* window_setMode(PyObject* self, PyObject* args) {
    int width, height;
    PyObject* flags = nullptr;
    if (!PyArg_ParseTuple(args, "ii|O", &width, &height, &flags))
        return nullptr;
    
    g_state.width = width;
    g_state.height = height;

    applyWindowFlagsFromDict(flags);
    if (PyErr_Occurred()) {
        return nullptr;
    }
    
    if (g_state.window) {
        SDL_SetWindowSize(g_state.window, width, height);
        SDL_GL_MakeCurrent(g_state.window, g_state.gl_context);
        updateGLViewportAndProjection();

        SDL_SetWindowResizable(g_state.window, (g_state.window_flags & SDL_WINDOW_RESIZABLE) != 0);
        SDL_SetWindowFullscreen(g_state.window, (g_state.window_flags & SDL_WINDOW_FULLSCREEN) != 0);
        SDL_GL_SetSwapInterval(g_state.vsync ? 1 : 0);
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

static PyObject* window_getMode(PyObject* self, PyObject* args) {
    PyObject* flags = PyDict_New();
    if (!flags) return nullptr;

    PyObject* fullscreen = (g_state.window_flags & SDL_WINDOW_FULLSCREEN) ? Py_True : Py_False;
    PyObject* resizable = (g_state.window_flags & SDL_WINDOW_RESIZABLE) ? Py_True : Py_False;
    PyObject* vsync = g_state.vsync ? Py_True : Py_False;

    Py_INCREF(fullscreen);
    Py_INCREF(resizable);
    Py_INCREF(vsync);

    PyDict_SetItemString(flags, "fullscreen", fullscreen);
    PyDict_SetItemString(flags, "resizable", resizable);
    PyDict_SetItemString(flags, "vsync", vsync);

    Py_DECREF(fullscreen);
    Py_DECREF(resizable);
    Py_DECREF(vsync);

    PyObject* result = Py_BuildValue("(iiO)", g_state.width, g_state.height, flags);
    Py_DECREF(flags);
    return result;
}

static PyObject* window_close(PyObject* self, PyObject* args) {
    SDL_Event event;
    event.type = SDL_EVENT_QUIT;
    SDL_PushEvent(&event);
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
    {"getMode", window_getMode, METH_NOARGS, "Get window mode (width, height, flags)"},
    {"setTitle", window_setTitle, METH_VARARGS, "Set window title"},
    {"close", window_close, METH_NOARGS, "Close the window"},
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
    return PyFloat_FromDouble(g_state.last_dt);
}

static PyObject* timer_getFPS(PyObject* self, PyObject* args) {
    return PyFloat_FromDouble(g_state.fps);
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
// Love Global Functions
// ============================================================================

static PyObject* love_getVersion(PyObject* self, PyObject* args) {
    return Py_BuildValue("(iiis)", 11, 5, 0, "Mysterious Mysteries");
}

static PyObject* love_setDeprecationOutput(PyObject* self, PyObject* args) {
    int enabled = 0;
    if (!PyArg_ParseTuple(args, "p", &enabled)) {
        return nullptr;
    }
    g_deprecation_output = enabled != 0;
    Py_RETURN_NONE;
}

static PyObject* love_hasDeprecationOutput(PyObject* self, PyObject* args) {
    if (g_deprecation_output) {
        Py_RETURN_TRUE;
    }
    Py_RETURN_FALSE;
}

static bool parseVersionString(const char* versionStr, int& major, int& minor, int& revision) {
    major = 0;
    minor = 0;
    revision = 0;

    if (!versionStr) return false;

    std::string s(versionStr);
    size_t p1 = s.find('.');
    if (p1 == std::string::npos) {
        return false;
    }
    size_t p2 = s.find('.', p1 + 1);

    try {
        major = std::stoi(s.substr(0, p1));
        if (p2 == std::string::npos) {
            minor = std::stoi(s.substr(p1 + 1));
            revision = 0;
            return true;
        }
        minor = std::stoi(s.substr(p1 + 1, p2 - (p1 + 1)));
        revision = std::stoi(s.substr(p2 + 1));
        return true;
    } catch (...) {
        return false;
    }
}

static PyObject* love_isVersionCompatible(PyObject* self, PyObject* args) {
    const char* versionStr = nullptr;
    if (!PyArg_ParseTuple(args, "s", &versionStr)) {
        return nullptr;
    }

    int major = 0, minor = 0, revision = 0;
    if (!parseVersionString(versionStr, major, minor, revision)) {
        PyErr_SetString(PyExc_ValueError, "Invalid version string");
        return nullptr;
    }

    const int currentMajor = 11;
    const int currentMinor = 5;
    const int currentRevision = 0;

    bool compatible = (major == currentMajor) &&
                      ((minor < currentMinor) ||
                       (minor == currentMinor && revision <= currentRevision));

    if (compatible) {
        Py_RETURN_TRUE;
    }
    Py_RETURN_FALSE;
}

static PyMethodDef LoveMethods[] = {
    {"getVersion", love_getVersion, METH_NOARGS, "Get LOVE version (major, minor, revision, codename)"},
    {"setDeprecationOutput", love_setDeprecationOutput, METH_VARARGS, "Enable/disable deprecation output"},
    {"hasDeprecationOutput", love_hasDeprecationOutput, METH_NOARGS, "Check if deprecation output is enabled"},
    {"isVersionCompatible", love_isVersionCompatible, METH_VARARGS, "Check if version string is compatible"},
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
        PyModuleDef_HEAD_INIT, "love", "LOVE2D Python API", -1, LoveMethods
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

    if (PyType_Ready(&CanvasType) < 0) {
        return nullptr;
    }
    Py_INCREF(&CanvasType);
    if (graphics) {
        PyModule_AddObject(graphics, "Canvas", (PyObject*)&CanvasType);
    }
    
    // Add version
    PyModule_AddStringConstant(love, "__version__", "11.5.0");
    
    return love;
}

// ============================================================================
// SDL and Game Loop
// ============================================================================

bool initSDL() {
    if (!SDL_Init(SDL_INIT_VIDEO)) {
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
        g_state.window_flags
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
    loadOpenGLFunctionPointers();
    SDL_GL_SetSwapInterval(g_state.vsync ? 1 : 0);

    updateGLViewportAndProjection();

    SDL_StartTextInput(g_state.window);
    
    g_state.initialized = true;
    return true;
}

void quitSDL() {
    // Cleanup fonts (must be done before FreeType cleanup)
    Py_XDECREF(g_state.current_font);
    g_state.current_font = nullptr;
    
    Py_XDECREF(g_state.default_font);
    g_state.default_font = nullptr;

    Py_XDECREF(g_state.current_canvas);
    g_state.current_canvas = nullptr;
    
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

static const char* normalizeKeyName(SDL_Keycode keycode) {
    switch (keycode) {
        case SDLK_BACKSPACE: return "backspace";
        case SDLK_DELETE: return "delete";
        case SDLK_LEFT: return "left";
        case SDLK_RIGHT: return "right";
        case SDLK_UP: return "up";
        case SDLK_DOWN: return "down";
        case SDLK_HOME: return "home";
        case SDLK_END: return "end";
        case SDLK_RETURN: return "return";
        case SDLK_ESCAPE: return "escape";
        case SDLK_TAB: return "tab";
        case SDLK_SPACE: return "space";
        case SDLK_LSHIFT: return "lshift";
        case SDLK_RSHIFT: return "rshift";
        case SDLK_LCTRL: return "lctrl";
        case SDLK_RCTRL: return "rctrl";
        case SDLK_LALT: return "lalt";
        case SDLK_RALT: return "ralt";
        case SDLK_LGUI: return "lgui";
        case SDLK_RGUI: return "rgui";
        default: break;
    }

    const char* name = SDL_GetKeyName(keycode);
    if (!name) return "";

    static thread_local std::string normalized;
    normalized.clear();

    for (const unsigned char* p = (const unsigned char*)name; *p; ++p) {
        if (*p == ' ')
            continue;
        normalized.push_back((char)std::tolower(*p));
    }
    return normalized.c_str();
}

static bool callPythonKeyReleasedCallback(PyObject* callback, const char* key, int scancode) {
    if (!callback || callback == Py_None) return true;

    PyObject* args2 = Py_BuildValue("(si)", key, scancode);
    PyObject* result2 = PyObject_CallObject(callback, args2);
    Py_DECREF(args2);

    if (result2) {
        Py_DECREF(result2);
        return true;
    }

    if (PyErr_ExceptionMatches(PyExc_TypeError)) {
        PyErr_Clear();
        PyObject* args3 = Py_BuildValue("(sii)", key, scancode, 0);
        PyObject* result3 = PyObject_CallObject(callback, args3);
        Py_DECREF(args3);
        if (!result3) {
            PyErr_Print();
            return false;
        }
        Py_DECREF(result3);
        return true;
    }

    PyErr_Print();
    return false;
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

bool callPythonMouseMoveCallback(PyObject* callback, int x, int y, int dx, int dy, bool istouch) {
    if (!callback || callback == Py_None) return true;

    PyObject* args = Py_BuildValue("(iiiii)", x, y, dx, dy, istouch ? 1 : 0);
    PyObject* result = PyObject_CallObject(callback, args);
    Py_DECREF(args);

    if (!result) {
        PyErr_Print();
        return false;
    }

    Py_DECREF(result);
    return true;
}

static bool callPythonResizeCallback(int w, int h) {
    if (!g_state.py_resize || g_state.py_resize == Py_None) return true;
    PyObject* args = Py_BuildValue("(ii)", w, h);
    PyObject* result = PyObject_CallObject(g_state.py_resize, args);
    Py_DECREF(args);
    if (!result) {
        PyErr_Print();
        return false;
    }
    Py_DECREF(result);
    return true;
}

static bool callPythonBoolCallback(PyObject* callback, bool value) {
    if (!callback || callback == Py_None) return true;
    PyObject* args = Py_BuildValue("(i)", value ? 1 : 0);
    PyObject* result = PyObject_CallObject(callback, args);
    Py_DECREF(args);
    if (!result) {
        PyErr_Print();
        return false;
    }
    Py_DECREF(result);
    return true;
}

static bool callPythonTextCallback(PyObject* callback, const char* text) {
    if (!callback || callback == Py_None) return true;
    PyObject* args = Py_BuildValue("(s)", text ? text : "");
    PyObject* result = PyObject_CallObject(callback, args);
    Py_DECREF(args);
    if (!result) {
        PyErr_Print();
        return false;
    }
    Py_DECREF(result);
    return true;
}

static bool callPythonWheelCallback(float x, float y) {
    if (!g_state.py_wheelmoved || g_state.py_wheelmoved == Py_None) return true;
    PyObject* args = Py_BuildValue("(ff)", x, y);
    PyObject* result = PyObject_CallObject(g_state.py_wheelmoved, args);
    Py_DECREF(args);
    if (!result) {
        PyErr_Print();
        return false;
    }
    Py_DECREF(result);
    return true;
}

static bool callPythonDropCallback(PyObject* callback, const char* path) {
    if (!callback || callback == Py_None) return true;
    PyObject* args = Py_BuildValue("(s)", path ? path : "");
    PyObject* result = PyObject_CallObject(callback, args);
    Py_DECREF(args);
    if (!result) {
        PyErr_Print();
        return false;
    }
    Py_DECREF(result);
    return true;
}

static void applyConfTable(PyObject* t) {
    if (!t || !PyDict_Check(t)) {
        return;
    }

    PyObject* window = PyDict_GetItemString(t, "window");
    if (!window || !PyDict_Check(window)) {
        return;
    }

    PyObject* width = PyDict_GetItemString(window, "width");
    if (width && PyLong_Check(width)) {
        g_state.width = (int)PyLong_AsLong(width);
    }

    PyObject* height = PyDict_GetItemString(window, "height");
    if (height && PyLong_Check(height)) {
        g_state.height = (int)PyLong_AsLong(height);
    }

    PyObject* title = PyDict_GetItemString(window, "title");
    if (title && PyUnicode_Check(title)) {
        const char* s = PyUnicode_AsUTF8(title);
        if (s) {
            g_state.title = s;
        }
    }

    applyWindowFlagsFromDict(window);
    PyErr_Clear();
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

    g_state.py_conf = PyDict_GetItemString(global_dict, "love_conf");
    g_state.py_load = PyDict_GetItemString(global_dict, "love_load");
    g_state.py_update = PyDict_GetItemString(global_dict, "love_update");
    g_state.py_draw = PyDict_GetItemString(global_dict, "love_draw");
    g_state.py_quit = PyDict_GetItemString(global_dict, "love_quit");
    g_state.py_focus = PyDict_GetItemString(global_dict, "love_focus");
    g_state.py_resize = PyDict_GetItemString(global_dict, "love_resize");
    g_state.py_textinput = PyDict_GetItemString(global_dict, "love_textinput");
    g_state.py_visible = PyDict_GetItemString(global_dict, "love_visible");
    g_state.py_wheelmoved = PyDict_GetItemString(global_dict, "love_wheelmoved");
    g_state.py_directorydropped = PyDict_GetItemString(global_dict, "love_directorydropped");
    g_state.py_filedropped = PyDict_GetItemString(global_dict, "love_filedropped");
    g_state.py_keypressed = PyDict_GetItemString(global_dict, "love_keypressed");
    g_state.py_keyreleased = PyDict_GetItemString(global_dict, "love_keyreleased");
    g_state.py_mousepressed = PyDict_GetItemString(global_dict, "love_mousepressed");
    g_state.py_mousereleased = PyDict_GetItemString(global_dict, "love_mousereleased");
    g_state.py_mousemoved = PyDict_GetItemString(global_dict, "love_mousemoved");
    
    Py_XINCREF(g_state.py_conf);
    Py_XINCREF(g_state.py_load);
    Py_XINCREF(g_state.py_update);
    Py_XINCREF(g_state.py_draw);
    Py_XINCREF(g_state.py_quit);
    Py_XINCREF(g_state.py_focus);
    Py_XINCREF(g_state.py_resize);
    Py_XINCREF(g_state.py_textinput);
    Py_XINCREF(g_state.py_visible);
    Py_XINCREF(g_state.py_wheelmoved);
    Py_XINCREF(g_state.py_directorydropped);
    Py_XINCREF(g_state.py_filedropped);
    Py_XINCREF(g_state.py_keypressed);
    Py_XINCREF(g_state.py_keyreleased);
    Py_XINCREF(g_state.py_mousepressed);
    Py_XINCREF(g_state.py_mousereleased);
    Py_XINCREF(g_state.py_mousemoved);

    if (g_state.py_conf && g_state.py_conf != Py_None && PyCallable_Check(g_state.py_conf)) {
        PyObject* t = PyDict_New();
        PyObject* window = PyDict_New();
        if (t && window) {
            PyObject* width = PyLong_FromLong(g_state.width);
            PyObject* height = PyLong_FromLong(g_state.height);
            PyObject* title = PyUnicode_FromString(g_state.title.c_str());
            PyObject* fullscreen = (g_state.window_flags & SDL_WINDOW_FULLSCREEN) ? Py_True : Py_False;
            PyObject* resizable = (g_state.window_flags & SDL_WINDOW_RESIZABLE) ? Py_True : Py_False;
            PyObject* vsync = g_state.vsync ? Py_True : Py_False;

            Py_INCREF(fullscreen);
            Py_INCREF(resizable);
            Py_INCREF(vsync);

            if (width) PyDict_SetItemString(window, "width", width);
            if (height) PyDict_SetItemString(window, "height", height);
            if (title) PyDict_SetItemString(window, "title", title);
            PyDict_SetItemString(window, "fullscreen", fullscreen);
            PyDict_SetItemString(window, "resizable", resizable);
            PyDict_SetItemString(window, "vsync", vsync);
            PyDict_SetItemString(t, "window", window);

            Py_XDECREF(width);
            Py_XDECREF(height);
            Py_XDECREF(title);
            Py_DECREF(fullscreen);
            Py_DECREF(resizable);
            Py_DECREF(vsync);

            PyObject* confArgs = Py_BuildValue("(O)", t);
            PyObject* confResult = PyObject_CallObject(g_state.py_conf, confArgs);
            Py_XDECREF(confArgs);
            if (!confResult) {
                PyErr_Print();
            } else {
                Py_DECREF(confResult);
            }
            applyConfTable(t);
        }
        Py_XDECREF(window);
        Py_XDECREF(t);
    }
    
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
    Uint64 fps_last_time = last_time;
    int fps_frames = 0;
    
    while (g_state.running) {
        Uint64 current_time = SDL_GetTicks();
        double dt = (current_time - last_time) / 1000.0;
        last_time = current_time;
        g_state.last_dt = dt;

        fps_frames += 1;
        Uint64 fps_elapsed = current_time - fps_last_time;
        if (fps_elapsed >= 1000) {
            g_state.fps = (double)fps_frames * 1000.0 / (double)fps_elapsed;
            fps_frames = 0;
            fps_last_time = current_time;
        }
        
        SDL_Event event;
        while (SDL_PollEvent(&event)) {
            switch (event.type) {
                case SDL_EVENT_QUIT:
                    g_state.running = false;
                    break;

                case SDL_EVENT_WINDOW_RESIZED: {
                    int w = (int)event.window.data1;
                    int h = (int)event.window.data2;
                    if (w > 0 && h > 0) {
                        g_state.width = w;
                        g_state.height = h;
                        SDL_GL_MakeCurrent(g_state.window, g_state.gl_context);
                        updateGLViewportAndProjection();
                        if (!callPythonResizeCallback(w, h)) {
                            g_state.running = false;
                        }
                    }
                    break;
                }

                case SDL_EVENT_WINDOW_FOCUS_GAINED:
                    if (!callPythonBoolCallback(g_state.py_focus, true)) {
                        g_state.running = false;
                    }
                    break;

                case SDL_EVENT_WINDOW_FOCUS_LOST:
                    if (!callPythonBoolCallback(g_state.py_focus, false)) {
                        g_state.running = false;
                    }
                    break;

                case SDL_EVENT_WINDOW_SHOWN:
                    if (!callPythonBoolCallback(g_state.py_visible, true)) {
                        g_state.running = false;
                    }
                    break;

                case SDL_EVENT_WINDOW_HIDDEN:
                    if (!callPythonBoolCallback(g_state.py_visible, false)) {
                        g_state.running = false;
                    }
                    break;
                    
                case SDL_EVENT_KEY_DOWN:
                    if (event.key.key == SDLK_ESCAPE) {
                        g_state.running = false;
                    }
                    if (g_state.py_keypressed) {
                        const char* key = normalizeKeyName(event.key.key);
                        callPythonKeyCallback(g_state.py_keypressed, key, 
                                            event.key.scancode, 
                                            event.key.repeat != 0);
                    }
                    break;
                    
                case SDL_EVENT_KEY_UP:
                    if (g_state.py_keyreleased) {
                        const char* key = normalizeKeyName(event.key.key);
                        callPythonKeyReleasedCallback(g_state.py_keyreleased, key, event.key.scancode);
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
                        callPythonMouseMoveCallback(g_state.py_mousemoved,
                                                  (int)event.motion.x, (int)event.motion.y,
                                                  (int)event.motion.xrel, (int)event.motion.yrel,
                                                  false);
                    }
                    break;

                case SDL_EVENT_MOUSE_WHEEL:
                    if (!callPythonWheelCallback(event.wheel.x, event.wheel.y)) {
                        g_state.running = false;
                    }
                    break;

                case SDL_EVENT_TEXT_INPUT:
                    if (!callPythonTextCallback(g_state.py_textinput, event.text.text)) {
                        g_state.running = false;
                    }
                    break;

                case SDL_EVENT_DROP_FILE: {
                    const char* path = event.drop.data;
                    struct stat buffer;
                    bool isDir = false;
                    if (path && stat(path, &buffer) == 0) {
                        isDir = S_ISDIR(buffer.st_mode);
                    }
                    if (isDir) {
                        if (!callPythonDropCallback(g_state.py_directorydropped, path)) {
                            g_state.running = false;
                        }
                    } else {
                        if (!callPythonDropCallback(g_state.py_filedropped, path)) {
                            g_state.running = false;
                        }
                    }
                    break;
                }
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
    
    Py_XDECREF(g_state.py_conf);
    Py_XDECREF(g_state.py_load);
    Py_XDECREF(g_state.py_update);
    Py_XDECREF(g_state.py_draw);
    Py_XDECREF(g_state.py_quit);
    Py_XDECREF(g_state.py_focus);
    Py_XDECREF(g_state.py_resize);
    Py_XDECREF(g_state.py_textinput);
    Py_XDECREF(g_state.py_visible);
    Py_XDECREF(g_state.py_wheelmoved);
    Py_XDECREF(g_state.py_directorydropped);
    Py_XDECREF(g_state.py_filedropped);
    Py_XDECREF(g_state.py_keypressed);
    Py_XDECREF(g_state.py_keyreleased);
    Py_XDECREF(g_state.py_mousepressed);
    Py_XDECREF(g_state.py_mousereleased);
    Py_XDECREF(g_state.py_mousemoved);
    
    quitSDL();
    return 0;
}

int main(int argc, char* argv[]) {
#if defined(_WIN32)
    initializePythonFromEmbeddedRuntimeIfPresent();
#elif defined(__APPLE__)
    initializePythonFromEmbeddedRuntimeIfPresent(argv[0]);
#else
    Py_Initialize();
#endif
    
    std::string gamePath;
    std::string launchArg;
    if (argc >= 2) {
        launchArg = argv[1];
    }

#if defined(__APPLE__)
    if (launchArg.empty()) {
        std::string resourcesDir = getBundleResourcesDirectoryUtf8();
        std::string defaultGame = resourcesDir + "/resources/no_game.py";
        if (!pathIsFile(defaultGame)) {
            std::cerr << "Usage: " << argv[0] << " <game.py|game_dir>" << std::endl;
            std::cerr << "Example: " << argv[0] << " examples/basic_game.py" << std::endl;
            return 1;
        }
        if (pathIsDirectory(resourcesDir)) {
            chdir(resourcesDir.c_str());
        }
        launchArg = defaultGame;
    }
#endif

    if (launchArg.empty()) {
        std::cerr << "Usage: " << argv[0] << " <game.py|game_dir>" << std::endl;
        std::cerr << "Example: " << argv[0] << " examples/basic_game.py" << std::endl;
        return 1;
    }

    if (argIsDirectory(launchArg)) {
        std::string candidate = joinPath(launchArg, "main.py");
        if (!argIsFile(candidate)) {
            std::cerr << "Cannot find main.py in directory: " << launchArg << std::endl;
            std::cerr << "Usage: " << argv[0] << " <game.py|game_dir>" << std::endl;
            std::cerr << "Example: " << argv[0] << " examples/basic_game.py" << std::endl;
            return 1;
        }
        if (setWorkingDirectory(launchArg)) {
            gamePath = "main.py";
        } else {
            gamePath = candidate;
        }
    } else {
        gamePath = launchArg;
    }

    addToPythonSysPath(getDirectoryFromPath(gamePath));
    addToPythonSysPath(".");
    
    // Create and register the love module
    PyObject* love = createLoveModule();
    if (!love) {
        std::cerr << "Failed to create love module" << std::endl;
        Py_Finalize();
        return 1;
    }
    PyObject* sys_modules = PyImport_GetModuleDict();
    PyDict_SetItemString(sys_modules, "love", love);
    
    if (!loadGameScript(gamePath.c_str())) {
        Py_Finalize();
        return 1;
    }
    
    int result = runGame();
    
    Py_Finalize();
    return result;
}
