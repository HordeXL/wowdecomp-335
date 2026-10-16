#include <windows.h>
#include <cstdlib>
#include <cstdint>
#include <process.h>
#include "Engine/Source/Storm/H/storm.h"

// STATIC: 0x00D754F4
static int32_t s_exitcode;

// STATIC: 0x00D754F8
static int32_t s_exitcount;

// OFFSET: 0x00648F80
static void StormAtExit() {
    if (s_exitcount++ == 0) {
        _cexit();
        StormRtlDestroy();
        _exit(s_exitcode);
    }
}

// OFFSET: 0x00649020
void StormExitProcess(int32_t code) {
    s_exitcode = code;
    ExitProcess(code);
}

// Still to port (both need the SFile class from BlizzardCore/SFile2-Core.h):
//   StormInitialize (0x00648FB0) = SStrInitialize + SErrInitialize + SFile::Initialize
//   StormDestroy    (0x00648FC0) = SRgnDestroy + SMsgDestroy + SEvtDestroy + SCmdDestroy
//                                  + SFile::Destroy + SCompDestroy + SStrDestroy + atexit(StormAtExit)
// (2.4.3 calls six destroy functions, one fewer than 3.3.5a, and registers StormAtExit at 0x00648F80.)
