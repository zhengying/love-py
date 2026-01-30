/**
 * Filesystem module bindings (placeholder)
 */

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <fstream>
#include <sstream>
#include <filesystem>

#include "love2d_common.h"

namespace py = pybind11;
namespace fs = std::filesystem;

std::string filesystem_read(const std::string& filename, int64_t bytes = -1) {
    std::ifstream file(filename, std::ios::binary);
    if (!file) {
        throw std::runtime_error("Could not open file: " + filename);
    }
    
    std::ostringstream buffer;
    if (bytes > 0) {
        std::vector<char> data(bytes);
        file.read(data.data(), bytes);
        buffer.write(data.data(), file.gcount());
    } else {
        buffer << file.rdbuf();
    }
    
    return buffer.str();
}

int64_t filesystem_write(const std::string& filename, const std::string& data) {
    std::ofstream file(filename, std::ios::binary);
    if (!file) {
        throw std::runtime_error("Could not open file for writing: " + filename);
    }
    
    file.write(data.data(), data.size());
    return data.size();
}

bool filesystem_exists(const std::string& path) {
    return fs::exists(path);
}

bool filesystem_isFile(const std::string& path) {
    return fs::is_regular_file(path);
}

bool filesystem_isDirectory(const std::string& path) {
    return fs::is_directory(path);
}

py::list filesystem_getDirectoryItems(const std::string& dir) {
    py::list items;
    if (fs::is_directory(dir)) {
        for (const auto& entry : fs::directory_iterator(dir)) {
            items.append(entry.path().filename().string());
        }
    }
    return items;
}

bool filesystem_createDirectory(const std::string& name) {
    return fs::create_directory(name);
}

py::object filesystem_getInfo(const std::string& path, const std::string& filtertype = "") {
    if (!fs::exists(path)) {
        return py::none();
    }
    
    py::dict info;
    info["type"] = fs::is_directory(path) ? "directory" : "file";
    info["size"] = fs::is_regular_file(path) ? fs::file_size(path) : 0;
    info["modtime"] = 0;  // Placeholder
    
    return info;
}

std::string filesystem_getSaveDirectory() {
    // Placeholder - should return platform-specific save directory
    return "./save";
}

std::string filesystem_getWorkingDirectory() {
    return fs::current_path().string();
}

void init_filesystem(py::module_ &m) {
    m.doc() = "File I/O functions";
    
    m.def("read", &filesystem_read, "Read file contents",
          py::arg("filename"), py::arg("bytes") = -1);
    m.def("write", &filesystem_write, "Write to file",
          py::arg("filename"), py::arg("data"));
    m.def("exists", &filesystem_exists, "Check if path exists",
          py::arg("path"));
    m.def("isFile", &filesystem_isFile, "Check if path is file",
          py::arg("path"));
    m.def("isDirectory", &filesystem_isDirectory, "Check if path is directory",
          py::arg("path"));
    m.def("getDirectoryItems", &filesystem_getDirectoryItems, "List directory contents",
          py::arg("dir"));
    m.def("createDirectory", &filesystem_createDirectory, "Create directory",
          py::arg("name"));
    m.def("getInfo", &filesystem_getInfo, "Get file/directory info",
          py::arg("path"), py::arg("filtertype") = "");
    m.def("getSaveDirectory", &filesystem_getSaveDirectory, "Get save directory");
    m.def("getWorkingDirectory", &filesystem_getWorkingDirectory, "Get working directory");
}
