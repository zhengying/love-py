cmake_minimum_required(VERSION 3.15)
project(love2d_py VERSION 0.1.0 LANGUAGES CXX)

# C++17 required
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find Python (for embedding)
find_package(Python3 REQUIRED COMPONENTS Interpreter Development Development.Embed)

# Find SDL3 from local xcframework (macOS)
if(APPLE)
    # Use local SDL3.xcframework from shared/Frameworks
    set(SDL3_XCFRAMEWORK_PATH ${CMAKE_CURRENT_SOURCE_DIR}/src/shared/Frameworks/SDL3.xcframework)
    
    # Determine architecture
    if(CMAKE_SYSTEM_PROCESSOR MATCHES "arm64")
        set(SDL3_FRAMEWORK_PATH ${SDL3_XCFRAMEWORK_PATH}/macos-arm64_x86_64/SDL3.framework)
    else()
        set(SDL3_FRAMEWORK_PATH ${SDL3_XCFRAMEWORK_PATH}/macos-arm64_x86_64/SDL3.framework)
    endif()
    
    # Find SDL3 using the framework's CMake config
    find_package(SDL3 3.1.3 REQUIRED CONFIG PATHS ${SDL3_FRAMEWORK_PATH}/Versions/Current/Resources/CMake)
    
    # FreeType framework
    set(FREETYPE_FRAMEWORK_PATH ${CMAKE_CURRENT_SOURCE_DIR}/src/platform/apple/macOS/Frameworks/freetype.framework)
else()
    # For non-Apple platforms, use system SDL3
    find_package(SDL3 3.1.3 REQUIRED CONFIG)
endif()

# Find OpenGL
find_package(OpenGL REQUIRED)

# Create the main LOVE executable (like love.exe)
add_executable(love
    src/love.cpp
)

target_include_directories(love PRIVATE
    ${Python3_INCLUDE_DIRS}
)

if(APPLE)
    target_include_directories(love PRIVATE
        ${FREETYPE_FRAMEWORK_PATH}/Headers
    )
endif()

target_link_libraries(love PRIVATE
    ${Python3_LIBRARIES}
    SDL3::SDL3
    OpenGL::GL
)

if(APPLE)
    target_link_libraries(love PRIVATE
        ${FREETYPE_FRAMEWORK_PATH}/Versions/Current/freetype
    )
endif()

set_target_properties(love PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/bin
)

# Install
install(TARGETS love
    RUNTIME DESTINATION bin
)
