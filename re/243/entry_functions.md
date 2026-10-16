# Entry-chain function identification (2.4.3)

Produced with `re/tools/identify_func.py` (string + import references) cross-referenced against the
3.3.5a source (`git grep <string> main`).

| Address | Evidence | Identity | Confidence |
|---|---|---|---|
| `0x00401000` | `call 0x00643020`; `jmp 0x0040A552` | `start` | confirmed (matches 3.3.5a shape) |
| `0x0040A552` | `_security_init_cookie`; `jmp __tmainCRTStartup` | `WinMainCRTStartup` (CRT) | confirmed |
| `0x00406870` | CRT calls it with `(0x400000,0,cmdline,showcmd)`, `ret 0x10`; `_set_invalid_parameter_handler`, `_clearfp`, `_control87(0x9001F,-1)` | `WinMain` | confirmed |
| `0x0046C7E0` | single `ret` | `InvalidParameterHandler` | confirmed (matches 3.3.5a) |
| `0x00406790` | `SRegLoadValue("World of Warcraft\\Client","SendErrorLogs")`, title `"World of WarCraft (build 8606)"` | `CommonMain` | high |
| `0x00749F20` | `OpenProcessToken`, `GetTokenInformation`, `AllocateAndInitializeSid`, `InitializeAcl`, `AddAccessDeniedAce/AddAccessAllowedAce`, `SetSecurityInfo` | process DACL hardening — **ported** to `WoW/Source/Win32/WinMain.cpp` as `ProtectProcessSecurity` | high — 2.4.3-only, not in 3.3.5a |
| `0x0065A3F0` | `xor al,al; ret` | constant-**false** predicate | high |
| `0x00402460` | `cmp dword[0xBDB208],2; sete al` | returns `(g_0xBDB208 == 2)` — the launch-mode flag (3.3.5a `s_unk_B2FA10`) | high |
| `0x00402C40` | `'InstallPath'`, `'World of Warcraft'` | **`SetInstallPath`** (3.3.5a `Client.cpp:815`) | high |
| `0x004063B0` | `'WoW.mfil'`, `'Config.wtf'`, `'locale'`, `'dbCompress'`, `'processAffinityMask'`, `'timingMethod'`, `'.\Client.cpp'` | big init (~313 insns, ~55 calls): `CmdLineProcess`/CVar registration, not 3.3.5a's small `InitializeGlobal` | medium |
| `0x00667090` | `mov al,1; ret` | constant-**true** predicate | high |
| `0x00427E80` | thunk `jmp 0x00429D50` | thunk to `0x00429D50` (resets `[0xBDCF7C]`, calls `0x00649480`/`0x00429AC0`) | high |
| `0x00405E50` | `'World of Warcraft'`, `'.PAD'`; large body calling `0x006470F0`,`0x0074BEB0`,... | large teardown sequence (`BeginCloseGame` candidate) | medium |

## CommonMain control flow (2.4.3, raw addresses)

```
StormInitialize / SErrCatchUnhandledExceptions / CreateNamedEventA / StormSetOption(10,11)
OsSystemEnableCpuLog / SetPaths
SRegLoadValue/SaveValue "SendErrorLogs"
SErrSetLogTitleString("...build 8606") / SErrSetLogCallback(WowLogHeader) / SErrRegisterHandler(SendErrorLog)

if (!isFalse() && !(g_0xBDB208 == 2))   # 0x0065A3F0 (always false) / 0x00402460 (== 2)
    SetInstallPath();                    # 0x00402C40   -- the 3.3.5a InitializeGlobal prologue

if (0x004063B0()) {                      # big init: CmdLineProcess + CVar registration
    if (isTrue())                        # 0x00667090 (always true)
        0x00427E80();                    # thunk -> 0x00429D50 (subsystem reset)
    0x00405E50();                        # large teardown sequence (BeginCloseGame?)
}
StormDestroy();                          # 0x00648FC0
```

Notes: `0x0065A3F0`/`0x00667090` are constant false/true stubs (possibly trial/build flags);
`0x00402460` reads the launch-mode flag at `0x00BDB208`. The game loop (3.3.5a
`EventDoMessageLoop`) has not been located yet — it is somewhere in the `0x004063B0` path.
