/**
 * Image loading and texture management module
 * 
 * Uses stb_image for loading PNG/JPG and OpenGL for textures
 */

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#ifdef __APPLE__
#include <OpenGL/gl.h>
#else
#include <GL/gl.h>
#endif
#include <string>
#include <iostream>
#include <cstdio>

namespace py = pybind11;

#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"

// Image class to hold texture data
class Image {
public:
    std::string filename;
    int width = 0;
    int height = 0;
    int channels = 0;
    GLuint texture_id = 0;
    unsigned char* data = nullptr;
    bool loaded = false;
    
    Image(const std::string& fname) : filename(fname) {
        load();
    }
    
    ~Image() {
        if (data) {
            stbi_image_free(data);
            data = nullptr;
        }
        if (texture_id != 0) {
            glDeleteTextures(1, &texture_id);
            texture_id = 0;
        }
    }
    
    bool load() {
        // Load image using stb_image
        data = stbi_load(filename.c_str(), &width, &height, &channels, 4); // Force RGBA
        
        if (!data) {
            fprintf(stderr, "Failed to load image: %s\n", filename.c_str());
            fprintf(stderr, "Reason: %s\n", stbi_failure_reason());
            return false;
        }
        
        // Create OpenGL texture
        glGenTextures(1, &texture_id);
        glBindTexture(GL_TEXTURE_2D, texture_id);
        
        // Set texture parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);
        
        // Upload texture data
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, data);
        
        glBindTexture(GL_TEXTURE_2D, 0);
        
        loaded = true;
        printf("Image loaded: %s (%dx%d)\n", filename.c_str(), width, height);
        return true;
    }
    
    int getWidth() const { return width; }
    int getHeight() const { return height; }
    
    py::tuple getDimensions() const {
        return py::make_tuple(width, height);
    }
    
    void draw(float x, float y, float r = 0.0f, float sx = 1.0f, float sy = 1.0f, 
              float ox = 0.0f, float oy = 0.0f) const {
        if (!loaded || texture_id == 0) return;
        
        // Save current matrix
        glPushMatrix();
        
        // Apply transformations
        glTranslatef(x, y, 0.0f);
        glRotatef(r * 180.0f / 3.14159f, 0.0f, 0.0f, 1.0f);
        glScalef(sx, sy, 1.0f);
        glTranslatef(-ox, -oy, 0.0f);
        
        // Enable texturing
        glEnable(GL_TEXTURE_2D);
        glBindTexture(GL_TEXTURE_2D, texture_id);
        
        // Draw textured quad
        glBegin(GL_QUADS);
        glTexCoord2f(0.0f, 0.0f); glVertex2f(0.0f, 0.0f);
        glTexCoord2f(1.0f, 0.0f); glVertex2f((float)width, 0.0f);
        glTexCoord2f(1.0f, 1.0f); glVertex2f((float)width, (float)height);
        glTexCoord2f(0.0f, 1.0f); glVertex2f(0.0f, (float)height);
        glEnd();
        
        // Disable texturing
        glBindTexture(GL_TEXTURE_2D, 0);
        glDisable(GL_TEXTURE_2D);
        
        // Restore matrix
        glPopMatrix();
    }
};

// Global function to create new image
py::object graphics_newImage(const std::string& filename) {
    Image* img = new Image(filename);
    if (!img->loaded) {
        delete img;
        throw std::runtime_error("Failed to load image: " + filename);
    }
    return py::cast(img, py::return_value_policy::take_ownership);
}

// Global function to draw image
void graphics_draw(py::object drawable, float x, float y, float r = 0.0f, 
                   float sx = 1.0f, float sy = 1.0f, float ox = 0.0f, float oy = 0.0f,
                   float kx = 0.0f, float ky = 0.0f) {
    // Try to cast to Image
    try {
        Image* img = drawable.cast<Image*>();
        if (img) {
            img->draw(x, y, r, sx, sy, ox, oy);
        }
    } catch (...) {
        // Not an image, ignore
    }
}

void init_image(py::module_ &m) {
    m.doc() = "Image loading and texture management";
    
    // Image class
    py::class_<Image>(m, "Image")
        .def("getWidth", &Image::getWidth, "Get image width")
        .def("getHeight", &Image::getHeight, "Get image height")
        .def("getDimensions", &Image::getDimensions, "Get image dimensions (width, height)")
        .def_readonly("loaded", &Image::loaded, "Whether image was loaded successfully");
    
    // Functions
    m.def("newImage", &graphics_newImage, "Load a new image from file",
          py::arg("filename"));
    m.def("draw", &graphics_draw, "Draw a drawable object (Image, etc.)",
          py::arg("drawable"), py::arg("x"), py::arg("y"),
          py::arg("r") = 0.0f, py::arg("sx") = 1.0f, py::arg("sy") = 1.0f,
          py::arg("ox") = 0.0f, py::arg("oy") = 0.0f,
          py::arg("kx") = 0.0f, py::arg("ky") = 0.0f);
}
