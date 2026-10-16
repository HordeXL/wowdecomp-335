#include <cstddef>
#include "Engine/Source/Storm/H/storm.h"

// SLOG_FUNCTION is -1 in 2.4.3 (the __LINE__ slot), confirmed in the disassembly of both operators.

// OFFSET: 0x00401010
void* operator new(size_t bytes) {
    return SMemAlloc(bytes, "new", SLOG_FUNCTION, 0);
}

// OFFSET: 0x00401030
void operator delete[](void* ptr) noexcept {
    if (ptr) {
        SMemFree(ptr, "delete[]", SLOG_FUNCTION, 0);
    }
}

// Still to port from this file (3.3.5a Engine/Source/Storm/Source/SMem.cpp):
//   SMemSetDebugFlags (0x0076E4A0), FatalError (2.4.3: 0x00643140), SMemAlloc (0x006441F0),
//   SMemFree (0x00644230), SMemIsValidPointer, SMemReAlloc, operator delete, SMemDestroy,
//   SMemInitialize. operator delete still needs its 2.4.3 address.
