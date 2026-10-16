# Skeleton module: empty until the 2.4.3 sources are ported. The INTERFACE stub keeps CMake
# configurable while there is no source yet.
file(GLOB_RECURSE PRIVATE_SOURCES CONFIGURE_DEPENDS "*.cpp")

if (PRIVATE_SOURCES)
    add_library(ConsoleBase STATIC ${PRIVATE_SOURCES})
    target_include_directories(ConsoleBase PUBLIC ${CMAKE_SOURCE_DIR})
else ()
    add_library(ConsoleBase INTERFACE)
    target_include_directories(ConsoleBase INTERFACE ${CMAKE_SOURCE_DIR})
endif ()
