#include <cstddef>
#include <cstring>
#include "Engine/Source/Storm/H/storm.h"

// The Storm heap object lives at 0x00D73700 (validation flag at +0x424, critical section at +0x42C,
// 8-byte allocation header). Its Alloc/Free bodies and helpers are ported separately; declared here
// so the SMem wrappers compile.
class SHeap {
public:
    void* Alloc(size_t bytes, const char* filename, int32_t linenumber);
    void Free(void* ptr, const char* filename, int32_t linenumber);
};

static SHeap s_memory;  // 0x00D73700

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

// OFFSET: 0x006441F0
void* STORMAPI SMemAlloc(size_t bytes, const char* filename, int32_t linenumber, uint32_t flags) {
    void* ptr = s_memory.Alloc(bytes, filename, linenumber);

    if (flags & SMEM_FLAG_ZEROMEMORY) {
        memset(ptr, 0, bytes);
    }

    return ptr;
}

// OFFSET: 0x00644230
int32_t STORMAPI SMemFree(void* ptr, const char* filename, int32_t linenumber, uint32_t flags) {
    s_memory.Free(ptr, filename, linenumber);
    return 1;
}

// Still to port from this file (3.3.5a Engine/Source/Storm/Source/SMem.cpp):
//   FatalError (2.4.3: 0x00643140, called by the heap's Alloc; 2.4.3 drops the s_exitonfailure check
//   and calls the 6-argument SErrDisplayError), the heap Alloc/Free (0x00644090 / 0x00644190) and
//   their helpers (0x006434A0 / 0x00643A20 / 0x00643680 / 0x00643F00), SMemIsValidPointer,
//   SMemReAlloc, operator delete, SMemSetDebugFlags, SMemDestroy, SMemInitialize.
