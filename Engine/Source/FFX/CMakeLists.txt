# Skeleton module: empty until the 2.4.3 sources are ported. The INTERFACE stub keeps CMake
# configurable while there is no source yet.
file(GLOB_RECURSE PRIVATE_SOURCES CONFIGURE_DEPENDS "*.cpp")

if (PRIVATE_SOURCES)
    add_library(FFX STATIC ${PRIVATE_SOURCES})
    target_include_directories(FFX PUBLIC ${CMAKE_SOURCE_DIR})
else ()
    add_library(FFX INTERFACE)
    target_include_directories(FFX INTERFACE ${CMAKE_SOURCE_DIR})
endif ()
