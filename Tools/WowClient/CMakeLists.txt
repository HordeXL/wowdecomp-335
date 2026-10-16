# The client executable with the crash logger. Skipped while there is no source yet, so the
# skeleton still configures.
file(GLOB CLIENT_SOURCES CONFIGURE_DEPENDS "${CMAKE_SOURCE_DIR}/WoW/Source/*.cpp")

if (NOT CLIENT_SOURCES)
    message(STATUS "WowClient: no sources yet, skipping the executable")
    return()
endif ()

if (WOWDECOMP_ARCH_64)
    file(GLOB CLIENT_PLATFORM_SOURCES CONFIGURE_DEPENDS "${CMAKE_SOURCE_DIR}/WoW/Source/Win64/*.cpp")
    set(WOWCLIENT_OUTPUT_NAME WowClient64)
else ()
    file(GLOB CLIENT_PLATFORM_SOURCES CONFIGURE_DEPENDS "${CMAKE_SOURCE_DIR}/WoW/Source/Win32/*.cpp")
    set(WOWCLIENT_OUTPUT_NAME WowClient32)
endif ()

set(WOWCLIENT_OUTPUT_OVERRIDE "" CACHE STRING "WowClient executable name instead of WowClient64/WowClient32")
if (WOWCLIENT_OUTPUT_OVERRIDE)
    set(WOWCLIENT_OUTPUT_NAME ${WOWCLIENT_OUTPUT_OVERRIDE})
endif ()

option(WOWCLIENT_CRASH_LOG "Crash logger with console window and WowClient_crash.log" ON)
set(CLIENT_TOOL_SOURCES "")
if (WOWCLIENT_CRASH_LOG)
    list(APPEND CLIENT_TOOL_SOURCES crash_log.cpp)
endif ()

add_executable(WowClient WIN32 ${CLIENT_SOURCES} ${CLIENT_PLATFORM_SOURCES} ${CLIENT_TOOL_SOURCES})

set_target_properties(WowClient PROPERTIES
    OUTPUT_NAME ${WOWCLIENT_OUTPUT_NAME}
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/bin/Win
)

foreach (config ${CMAKE_CONFIGURATION_TYPES} ${CMAKE_BUILD_TYPE})
    string(TOUPPER ${config} config)
    set_target_properties(WowClient PROPERTIES RUNTIME_OUTPUT_DIRECTORY_${config} ${CMAKE_SOURCE_DIR}/bin/Win)
endforeach ()

target_include_directories(WowClient
    PRIVATE
        ${CMAKE_SOURCE_DIR}
)

target_link_options(WowClient PRIVATE "/INCREMENTAL:NO" "/ENTRY:start")

target_link_libraries(WowClient
    PRIVATE
        BLPFile
        Base
        BlizzardCore
        ComSat
        ConsoleBase
        Event
        FFX
        Frame
        FrameScript
        lua
        FrameXML
        Gx
        Gxu
        Images
        Model2
        Os
        Scrn
        Services
        ShaderEffect
        SoundEngine
        Storm
        Tempest
        WoWCommon
        Console
        ConsoleDevice
        DB
        Game
        Glue
        LiquidSystem
        Magic
        Minigame
        Net
        Object
        ObjectAlloc
        ObjectMgrClient
        SoundInterface
        UIUtil
        Ui
        WorldClient
        dbghelp
)
