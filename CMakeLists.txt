cmake_minimum_required(VERSION 3.15)
project(love2d_py VERSION 0.1.0 LANGUAGES CXX)

# C++17 required
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

if(APPLE)
    set(LOVE_EMBEDDED_PYTHON_STAGE_DIR ${CMAKE_BINARY_DIR}/embedded-python)
    if(CMAKE_SYSTEM_PROCESSOR MATCHES "arm64")
        set(LOVE_EMBEDDED_PYTHON_ARCHIVE ${CMAKE_CURRENT_SOURCE_DIR}/external/deps/python/macos-arm64/python-standalone.tar.zst)
    else()
        set(LOVE_EMBEDDED_PYTHON_ARCHIVE ${CMAKE_CURRENT_SOURCE_DIR}/external/deps/python/macos-x86_64/python-standalone.tar.zst)
    endif()

    if(NOT EXISTS ${LOVE_EMBEDDED_PYTHON_STAGE_DIR}/python/include)
        if(NOT EXISTS ${LOVE_EMBEDDED_PYTHON_ARCHIVE})
            message(FATAL_ERROR "Missing embedded Python archive: ${LOVE_EMBEDDED_PYTHON_ARCHIVE}")
        endif()
        file(MAKE_DIRECTORY ${LOVE_EMBEDDED_PYTHON_STAGE_DIR})
        execute_process(
            COMMAND ${CMAKE_COMMAND} -E tar xf ${LOVE_EMBEDDED_PYTHON_ARCHIVE}
            WORKING_DIRECTORY ${LOVE_EMBEDDED_PYTHON_STAGE_DIR}
            RESULT_VARIABLE LOVE_EMBEDDED_PYTHON_EXTRACT_RESULT
        )
        if(NOT LOVE_EMBEDDED_PYTHON_EXTRACT_RESULT EQUAL 0)
            message(FATAL_ERROR "Failed to extract embedded Python archive: ${LOVE_EMBEDDED_PYTHON_ARCHIVE}")
        endif()
    endif()

    file(GLOB LOVE_EMBEDDED_PYTHON_DYLIBS ${LOVE_EMBEDDED_PYTHON_STAGE_DIR}/python/lib/libpython*.dylib)
    list(LENGTH LOVE_EMBEDDED_PYTHON_DYLIBS LOVE_EMBEDDED_PYTHON_DYLIB_COUNT)
    if(LOVE_EMBEDDED_PYTHON_DYLIB_COUNT LESS 1)
        message(FATAL_ERROR "Embedded Python dylib not found under: ${LOVE_EMBEDDED_PYTHON_STAGE_DIR}/python/lib")
    endif()
    list(GET LOVE_EMBEDDED_PYTHON_DYLIBS 0 LOVE_EMBEDDED_PYTHON_DYLIB_PATH)
    get_filename_component(LOVE_EMBEDDED_PYTHON_DYLIB_NAME ${LOVE_EMBEDDED_PYTHON_DYLIB_PATH} NAME)

    file(GLOB LOVE_EMBEDDED_PYTHON_INCLUDE_DIRS LIST_DIRECTORIES true ${LOVE_EMBEDDED_PYTHON_STAGE_DIR}/python/include/python*)
    list(LENGTH LOVE_EMBEDDED_PYTHON_INCLUDE_DIRS LOVE_EMBEDDED_PYTHON_INCLUDE_DIR_COUNT)
    if(LOVE_EMBEDDED_PYTHON_INCLUDE_DIR_COUNT LESS 1)
        message(FATAL_ERROR "Embedded Python include directory not found under: ${LOVE_EMBEDDED_PYTHON_STAGE_DIR}/python/include")
    endif()
    list(GET LOVE_EMBEDDED_PYTHON_INCLUDE_DIRS 0 LOVE_EMBEDDED_PYTHON_INCLUDE_DIR)
endif()

# Find Python (for embedding)
#
# On macOS, the build uses the vendored embedded Python archive under external/deps/python,
# so a system Python installation is not required.
if(NOT APPLE)
    find_package(Python3 REQUIRED COMPONENTS Interpreter Development Development.Embed)
endif()

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
    find_package(Freetype REQUIRED)
endif()

# Find OpenGL
find_package(OpenGL REQUIRED)

# Create the main LOVE executable (like love.exe)
add_executable(love
    src/love.cpp
)

target_include_directories(love PRIVATE
    $<$<NOT:$<PLATFORM_ID:Darwin>>:${Python3_INCLUDE_DIRS}>
)

if(APPLE)
    target_include_directories(love PRIVATE
        ${FREETYPE_FRAMEWORK_PATH}/Headers
        ${LOVE_EMBEDDED_PYTHON_INCLUDE_DIR}
    )
endif()

target_link_libraries(love PRIVATE
    $<$<NOT:$<PLATFORM_ID:Darwin>>:${Python3_LIBRARIES}>
    $<$<PLATFORM_ID:Darwin>:${LOVE_EMBEDDED_PYTHON_DYLIB_PATH}>
    SDL3::SDL3
    OpenGL::GL
)

if(APPLE)
    target_link_libraries(love PRIVATE
        ${FREETYPE_FRAMEWORK_PATH}/Versions/Current/freetype
    )
else()
    if(TARGET Freetype::Freetype)
        target_link_libraries(love PRIVATE Freetype::Freetype)
    else()
        target_include_directories(love PRIVATE ${FREETYPE_INCLUDE_DIRS})
        target_link_libraries(love PRIVATE ${FREETYPE_LIBRARIES})
    endif()
endif()

set_target_properties(love PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/bin
)

if(APPLE)
    add_custom_command(TARGET love POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E make_directory ${CMAKE_CURRENT_SOURCE_DIR}/bin/python
        COMMAND ${CMAKE_COMMAND} -E copy_directory ${LOVE_EMBEDDED_PYTHON_STAGE_DIR}/python ${CMAKE_CURRENT_SOURCE_DIR}/bin/python
        COMMAND ${CMAKE_COMMAND} -E copy_directory ${CMAKE_CURRENT_SOURCE_DIR}/python_builtin ${CMAKE_CURRENT_SOURCE_DIR}/bin/python/builtin
        COMMAND /bin/sh -c "install_name_tool -add_rpath '@executable_path/python/lib' '${CMAKE_CURRENT_SOURCE_DIR}/bin/love' 2>/dev/null || true"
        COMMAND /bin/sh -c "install_name_tool -change '${LOVE_EMBEDDED_PYTHON_DYLIB_PATH}' '@rpath/${LOVE_EMBEDDED_PYTHON_DYLIB_NAME}' '${CMAKE_CURRENT_SOURCE_DIR}/bin/love' 2>/dev/null || true"
        COMMAND /bin/sh -c "install_name_tool -change '/install/lib/${LOVE_EMBEDDED_PYTHON_DYLIB_NAME}' '@rpath/${LOVE_EMBEDDED_PYTHON_DYLIB_NAME}' '${CMAKE_CURRENT_SOURCE_DIR}/bin/love' 2>/dev/null || true"
        COMMAND /bin/sh -c "install_name_tool -id '@rpath/${LOVE_EMBEDDED_PYTHON_DYLIB_NAME}' '${CMAKE_CURRENT_SOURCE_DIR}/bin/python/lib/${LOVE_EMBEDDED_PYTHON_DYLIB_NAME}' 2>/dev/null || true"
        VERBATIM
    )

    add_executable(love_app MACOSX_BUNDLE
        src/love.cpp
    )

    target_include_directories(love_app PRIVATE
        ${LOVE_EMBEDDED_PYTHON_INCLUDE_DIR}
        ${FREETYPE_FRAMEWORK_PATH}/Headers
    )

    target_link_libraries(love_app PRIVATE
        ${LOVE_EMBEDDED_PYTHON_DYLIB_PATH}
        SDL3::SDL3
        OpenGL::GL
        ${FREETYPE_FRAMEWORK_PATH}/Versions/Current/freetype
    )

    set_target_properties(love_app PROPERTIES
        OUTPUT_NAME love
        BUNDLE_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/bin
    )

    add_custom_command(TARGET love_app POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E make_directory $<TARGET_BUNDLE_CONTENT_DIR:love_app>/Frameworks
        COMMAND ${CMAKE_COMMAND} -E make_directory $<TARGET_BUNDLE_CONTENT_DIR:love_app>/Resources
        COMMAND ${CMAKE_COMMAND} -E copy_directory ${SDL3_FRAMEWORK_PATH} $<TARGET_BUNDLE_CONTENT_DIR:love_app>/Frameworks/SDL3.framework
        COMMAND ${CMAKE_COMMAND} -E copy_directory ${FREETYPE_FRAMEWORK_PATH} $<TARGET_BUNDLE_CONTENT_DIR:love_app>/Frameworks/freetype.framework
        COMMAND ${CMAKE_COMMAND} -E copy_directory ${LOVE_EMBEDDED_PYTHON_STAGE_DIR}/python $<TARGET_BUNDLE_CONTENT_DIR:love_app>/Resources/python
        COMMAND ${CMAKE_COMMAND} -E copy_directory ${CMAKE_CURRENT_SOURCE_DIR}/python_builtin $<TARGET_BUNDLE_CONTENT_DIR:love_app>/Resources/python/builtin
        COMMAND ${CMAKE_COMMAND} -E copy_directory ${CMAKE_CURRENT_SOURCE_DIR}/resources $<TARGET_BUNDLE_CONTENT_DIR:love_app>/Resources/resources
        COMMAND /bin/sh -c "install_name_tool -delete_rpath '${SDL3_XCFRAMEWORK_PATH}/macos-arm64_x86_64' '$<TARGET_FILE:love_app>' 2>/dev/null || true"
        COMMAND /bin/sh -c "install_name_tool -delete_rpath '${CMAKE_CURRENT_SOURCE_DIR}/src/platform/apple/macOS/Frameworks' '$<TARGET_FILE:love_app>' 2>/dev/null || true"
        COMMAND /bin/sh -c "install_name_tool -add_rpath '@executable_path/../Frameworks' '$<TARGET_FILE:love_app>' 2>/dev/null || true"
        COMMAND /bin/sh -c "install_name_tool -add_rpath '@executable_path/../Resources/python/lib' '$<TARGET_FILE:love_app>' 2>/dev/null || true"
        COMMAND /bin/sh -c "install_name_tool -change '${LOVE_EMBEDDED_PYTHON_DYLIB_PATH}' '@rpath/${LOVE_EMBEDDED_PYTHON_DYLIB_NAME}' '$<TARGET_FILE:love_app>' 2>/dev/null || true"
        COMMAND /bin/sh -c "install_name_tool -change '/install/lib/${LOVE_EMBEDDED_PYTHON_DYLIB_NAME}' '@rpath/${LOVE_EMBEDDED_PYTHON_DYLIB_NAME}' '$<TARGET_FILE:love_app>' 2>/dev/null || true"
        COMMAND /bin/sh -c "install_name_tool -id '@rpath/${LOVE_EMBEDDED_PYTHON_DYLIB_NAME}' '$<TARGET_BUNDLE_CONTENT_DIR:love_app>/Resources/python/lib/${LOVE_EMBEDDED_PYTHON_DYLIB_NAME}'"
        COMMAND ${CMAKE_COMMAND} -E rm -rf ${CMAKE_CURRENT_SOURCE_DIR}/bin/love.app
        COMMAND ${CMAKE_COMMAND} -E copy_directory $<TARGET_BUNDLE_DIR:love_app> ${CMAKE_CURRENT_SOURCE_DIR}/bin/love.app
        VERBATIM
    )
endif()

# Install
install(TARGETS love
    RUNTIME DESTINATION bin
)
