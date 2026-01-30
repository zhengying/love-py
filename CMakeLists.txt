cmake_minimum_required(VERSION 3.15)
project(love2d_py VERSION 0.1.0 LANGUAGES CXX)

# C++17 required for pybind11
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find Python
find_package(Python3 REQUIRED COMPONENTS Interpreter Development)

# Find pybind11
execute_process(
    COMMAND ${Python3_EXECUTABLE} -m pybind11 --cmakedir
    OUTPUT_VARIABLE PYBIND11_CMAKEDIR
    OUTPUT_STRIP_TRAILING_WHITESPACE
)
list(APPEND CMAKE_PREFIX_PATH ${PYBIND11_CMAKEDIR})
find_package(pybind11 REQUIRED)

# Find LOVE2D headers and libraries
# Assumes LOVE2D is installed or in love2d-orignal/src
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/../love2d-orignal/src")
    set(LOVE2D_INCLUDE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/../love2d-orignal/src")
else()
    # Try to find system LOVE2D
    find_path(LOVE2D_INCLUDE_DIR NAMES love/love.h PATHS /usr/include /usr/local/include)
endif()

# SDL2 is required for LOVE2D
find_package(SDL2 REQUIRED)
find_package(OpenGL REQUIRED)

# Create the binding module
pybind11_add_module(_love2d_core
    src/love2d_bindings.cpp
    src/graphics_module.cpp
    src/window_module.cpp
    src/event_module.cpp
    src/timer_module.cpp
    src/keyboard_module.cpp
    src/mouse_module.cpp
    src/audio_module.cpp
    src/filesystem_module.cpp
    src/callback_manager.cpp
)

target_include_directories(_love2d_core PRIVATE
    ${LOVE2D_INCLUDE_DIR}
    ${SDL2_INCLUDE_DIRS}
)

target_link_libraries(_love2d_core PRIVATE
    SDL2::SDL2
    OpenGL::GL
)

# If LOVE2D library exists, link it
if(EXISTS "${LOVE2D_LIBRARY}")
    target_link_libraries(_love2d_core PRIVATE ${LOVE2D_LIBRARY})
endif()

# Set properties
set_target_properties(_love2d_core PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/love
)

# Install
install(TARGETS _love2d_core
    LIBRARY DESTINATION love
)
