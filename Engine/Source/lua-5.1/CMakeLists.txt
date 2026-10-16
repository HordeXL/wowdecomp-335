# Skeleton module: empty until the 2.4.3 sources are ported. The INTERFACE stub keeps CMake
# configurable while there is no source yet.
file(GLOB PRIVATE_SOURCES CONFIGURE_DEPENDS "src/*.c" "src/*.cpp")

if (PRIVATE_SOURCES)
    set_source_files_properties(${PRIVATE_SOURCES} PROPERTIES LANGUAGE CXX)
    add_library(lua STATIC ${PRIVATE_SOURCES})
    target_include_directories(lua PUBLIC ${CMAKE_SOURCE_DIR} ${CMAKE_CURRENT_SOURCE_DIR}/src)
else ()
    add_library(lua INTERFACE)
    target_include_directories(lua INTERFACE ${CMAKE_SOURCE_DIR} ${CMAKE_CURRENT_SOURCE_DIR}/src)
endif ()
