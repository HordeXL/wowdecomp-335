#include <cstdint>
#include <cstring>
#include "Engine/Source/Storm/H/storm.h"

// OFFSET: 0x006449D0
char* SStrChr(const char* string, char search) {
    if (!string) {
        SErrSetLastError(STORM_ERROR_INVALID_PARAMETER);
        return nullptr;
    }

    for (; *string; string++) {
        if (*string == search) {
            return const_cast<char*>(string);
        }
    }

    return nullptr;
}

// OFFSET: 0x00644A10
char* SStrChrR(const char* string, char search) {
    if (!string) {
        SErrSetLastError(STORM_ERROR_INVALID_PARAMETER);
        return nullptr;
    }

    const char* result = nullptr;

    for (; *string; string++) {
        if (*string == search) {
            result = string;
        }
    }

    return const_cast<char*>(result);
}

// OFFSET: 0x00644A90
// 2.4.3 adds the null guard that 3.3.5a's one-line strncmp wrapper does not.
int32_t STORMAPI SStrCmp(const char* string1, const char* string2, size_t maxchars) {
    if (!string1 || !string2) {
        SErrSetLastError(STORM_ERROR_INVALID_PARAMETER);
        return static_cast<int32_t>(reinterpret_cast<intptr_t>(string1) - reinterpret_cast<intptr_t>(string2));
    }

    return strncmp(string1, string2, maxchars);
}

// Still to port from SStr.cpp: SStrCmpI (0x00644AD0 inlines its case-insensitive compare and returns
// 0 on a null argument), the UTF-8 compare helpers, SStrCopy/SStrLen/SStrPack/SStrPrintf/SStrToInt/
// SStrHash and the rest.
