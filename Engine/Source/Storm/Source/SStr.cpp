#include <cstdint>
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

// Still to port from SStr.cpp: SStrCmp/SStrCmpI (2.4.3: 0x00644A90 has extra null checks that
// 3.3.5a's one-line strncmp wrappers do not, so the bodies must be reversed), the UTF-8 compare
// helpers, SStrCopy/SStrLen/SStrPack/SStrPrintf/SStrToInt/SStrHash and the rest.
