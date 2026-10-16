# Skeleton module: empty until the 2.4.3 sources are ported. The INTERFACE stub keeps CMake
# configurable while there is no source yet.
#
# The 3.3.5a tree also vendored FMOD Ex under fmodex/ and assembled its .s/.nasm sources with NASM
# on Win32. That vendored payload has to be restored here when SoundEngine is ported.
file(GLOB_RECURSE PRIVATE_SOURCES CONFIGURE_DEPENDS "*.cpp")

if (PRIVATE_SOURCES)
    add_library(SoundEngine STATIC ${PRIVATE_SOURCES})
    target_include_directories(SoundEngine PUBLIC ${CMAKE_SOURCE_DIR})
else ()
    add_library(SoundEngine INTERFACE)
    target_include_directories(SoundEngine INTERFACE ${CMAKE_SOURCE_DIR})
endif ()
