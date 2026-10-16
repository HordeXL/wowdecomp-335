#include <windows.h>
#include <cstdio>
#include <cstddef>
#include <cstring>
#include "Engine/Source/Storm/H/storm.h"

// The Storm heap object lives at 0x00D73700: a size-classed free-list allocator. Allocations carry
// an 8-byte header (the user pointer is block + 8) and Alloc/Free guard the bins with the critical
// section at +0x42C.
class SHeap {
public:
    void* Alloc(size_t bytes, const char* filename, int32_t linenumber);
    void Free(void* ptr, const char* filename, int32_t linenumber);

private:
    uint32_t GetSizeClass(size_t bytes, const char* filename, int32_t linenumber);  // 0x006434A0
    void* AllocateBlock(uint32_t sizeClass, size_t bytes, int32_t unk);              // 0x00643A20
    int32_t ValidateBlock(void* block, const char* filename, int32_t linenumber);    // 0x00643680
    void ReleaseBlock(void* block);                                                  // 0x00643F00

    // Layout: bins at +0x0C (class * 0x10), free-list heads at +0x20C (class * 4), stats at
    // +0x40C/+0x410/+0x414, enabled flag at +0x424, guarding critical section at +0x42C.
    uint8_t m_bins[0x40C];
    uint32_t m_unk40C;
    uint32_t m_unk410;
    uint32_t m_unk414;
    uint8_t m_pad0[0x424 - 0x418];
    uint32_t m_enabled;
    uint8_t m_pad1[0x42C - 0x424 - 4];
    CRITICAL_SECTION m_criticalSection;
};

static SHeap s_memory;  // 0x00D73700

// OFFSET: 0x00643140
static void FatalError(size_t bytes, const char* filename, int32_t linenumber) {
    char buffer[128];
    sprintf(buffer, "Requested %u bytes of memory", static_cast<uint32_t>(bytes));
    SErrDisplayError(STORM_ERROR_NOT_ENOUGH_MEMORY, filename, linenumber, buffer, 0, 1);
    StormExitProcess(1);
}

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

// OFFSET: 0x006434A0
uint32_t SHeap::GetSizeClass(size_t bytes, const char* filename, int32_t linenumber) {
    uint32_t size = static_cast<uint32_t>(bytes);
    uint32_t sizeClass = 3;

    if (size > 0xFFFFFFF7) {
        sizeClass = 0x20;
    } else {
        uint32_t needed = size + 8;
        while (sizeClass < 0x20 && (1u << sizeClass) < needed) {
            ++sizeClass;
        }
    }

    if (sizeClass == 0x20) {
        FatalError(bytes, filename, linenumber);
    }

    return sizeClass;
}

// OFFSET: 0x00644090
void* SHeap::Alloc(size_t bytes, const char* filename, int32_t linenumber) {
    uint32_t sizeClass = GetSizeClass(bytes, filename, linenumber);

    EnterCriticalSection(&m_criticalSection);

    void* block = nullptr;
    if (m_enabled) {
        block = AllocateBlock(sizeClass, bytes, 1);
    }

    LeaveCriticalSection(&m_criticalSection);

    if (!block) {
        FatalError(bytes, filename, linenumber);
    }

    return static_cast<uint8_t*>(block) + 8;
}

// OFFSET: 0x00644190
void SHeap::Free(void* ptr, const char* filename, int32_t linenumber) {
    if (!ptr) {
        return;
    }

    void* block = static_cast<uint8_t*>(ptr) - 8;

    EnterCriticalSection(&m_criticalSection);

    if (m_enabled && ValidateBlock(block, filename, linenumber)) {
        ReleaseBlock(block);
    }

    LeaveCriticalSection(&m_criticalSection);
}

// Still to port: the heap's bin helpers (AllocateBlock 0x00643A20, ValidateBlock 0x00643680,
// ReleaseBlock 0x00643F00) and the heap initialization (the global at 0x00D73700), plus
// SMemIsValidPointer, SMemReAlloc, operator delete, SMemSetDebugFlags, SMemDestroy, SMemInitialize.
