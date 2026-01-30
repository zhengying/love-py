cmake_minimum_required(VERSION 3.15)
project(love2d_py VERSION 0.1.0 LANGUAGES CXX)

# C++17 required
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find Python (for embedding)
find_package(Python3 REQUIRED COMPONENTS Interpreter Development Development.Embed)

# SDL2 is required
find_package(SDL2 REQUIRED)
find_package(OpenGL REQUIRED)

# Create the main LOVE executable (like love.exe)
add_executable(love
    src/love.cpp
)

target_include_directories(love PRIVATE
    ${Python3_INCLUDE_DIRS}
    ${SDL2_INCLUDE_DIRS}
)

target_link_libraries(love PRIVATE
    ${Python3_LIBRARIES}
    SDL2::SDL2
    OpenGL::GL
)

set_target_properties(love PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/bin
)

# Install
install(TARGETS love
    RUNTIME DESTINATION bin
)
