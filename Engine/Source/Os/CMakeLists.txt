# Skeleton module: empty until the 2.4.3 sources are ported. The INTERFACE stub keeps CMake
# configurable while there is no source yet.
file(GLOB_RECURSE PRIVATE_SOURCES CONFIGURE_DEPENDS "*.cpp")

if (PRIVATE_SOURCES)
    add_library(Os STATIC ${PRIVATE_SOURCES})
    target_include_directories(Os PUBLIC ${CMAKE_SOURCE_DIR})
    target_link_libraries(Os PUBLIC imm32 wininet ws2_32 dinput8 dxguid version)
else ()
    add_library(Os INTERFACE)
    target_include_directories(Os INTERFACE ${CMAKE_SOURCE_DIR})
    target_link_libraries(Os INTERFACE imm32 wininet ws2_32 dinput8 dxguid version)
endif ()
