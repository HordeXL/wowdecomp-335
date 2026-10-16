#if defined(WOWDECOMP_ARCH_64)

#include <windows.h>
#include <aclapi.h>
#include <malloc.h>
#include <cstdlib>
#include <float.h>
#include "Engine/Source/Storm/H/storm.h"
#include "WoW/Source/Client.h"

// 2.4.3 shipped 32-bit only, so there is no original x64 WinMain. This mirrors the 32-bit boot
// logic (Win32/WinMain.cpp): no fiber startup, same call order. The `// OFFSET:` tags reuse the
// 32-bit addresses of the functions each one corresponds to.

// OFFSET: 0x0046C7E0
static void InvalidParameterHandler(const wchar_t* expression, const wchar_t* function, const wchar_t* file, unsigned int line, uintptr_t reserved) {
}

// OFFSET: 0x00749F20
static bool ProtectProcessSecurity() {
    HANDLE process = GetCurrentProcess();
    bool restricted = false;

    PSID everyoneSid = nullptr;
    HANDLE token = nullptr;
    SID_IDENTIFIER_AUTHORITY worldAuthority = SECURITY_WORLD_SID_AUTHORITY;
    DWORD tokenUserSize = 0;

    if (!AllocateAndInitializeSid(&worldAuthority, 1, SECURITY_WORLD_RID, 0, 0, 0, 0, 0, 0, 0, &everyoneSid)) {
        goto cleanup;
    }

    if (!OpenProcessToken(process, TOKEN_QUERY, &token)) {
        goto cleanup;
    }

    GetTokenInformation(token, TokenUser, nullptr, 0, &tokenUserSize);

    if (tokenUserSize > 0x400) {
        goto cleanup;
    }

    {
        TOKEN_USER* tokenUser = static_cast<TOKEN_USER*>(_alloca(tokenUserSize));
        BYTE aclStorage[0x200];
        ACL* acl = reinterpret_cast<ACL*>(aclStorage);

        if (!GetTokenInformation(token, TokenUser, tokenUser, tokenUserSize, &tokenUserSize)) {
            goto cleanup;
        }

        if (!InitializeAcl(acl, sizeof(aclStorage), ACL_REVISION)) {
            goto cleanup;
        }

        if (!AddAccessDeniedAce(acl, ACL_REVISION, 0xFA, everyoneSid)) {
            goto cleanup;
        }

        if (!AddAccessAllowedAce(acl, ACL_REVISION, 0x100701, tokenUser->User.Sid)) {
            goto cleanup;
        }

        if (SetSecurityInfo(process, SE_KERNEL_OBJECT,
                            DACL_SECURITY_INFORMATION | PROTECTED_DACL_SECURITY_INFORMATION,
                            nullptr, nullptr, acl, nullptr) != ERROR_SUCCESS) {
            goto cleanup;
        }

        restricted = true;
    }

cleanup:
    if (token) {
        CloseHandle(token);
    }
    if (everyoneSid) {
        FreeSid(everyoneSid);
    }
    return restricted;
}

extern "C" int WinMainCRTStartup();

// OFFSET: 0x00401000
extern "C" int start() {
    StormRtlInitialize();
    return WinMainCRTStartup();
}

// OFFSET: 0x00406870
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nShowCmd) {
    _set_invalid_parameter_handler(InvalidParameterHandler);
    _clearfp();
    _control87(0x9001F & ~(_MCW_PC | _MCW_IC), _MCW_DN | _MCW_EM | _MCW_RC);

    ProtectProcessSecurity();

    return CommonMain();
}

#endif
