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
| `0x00749F20` | `OpenProcessToken`, `GetTokenInformation`, `AllocateAndInitializeSid`, `InitializeAcl`, `AddAccessDeniedAce/AddAccessAllowedAce`, `SetSecurityInfo` | process security hardening (restricts access to the process) | high — **2.4.3-only**, not in 3.3.5a's `WinMain` |
| `0x0065A3F0` | no string/import refs; returns bool | unknown | low |
| `0x00402460` | `'%s%s'`, `'****'` | unknown (masked-string helper) | low |
| `0x00402C40` | `'InstallPath'`, `'World of Warcraft'` | install-path registry lookup (`SetInstallPath` family in `Client.cpp`) | medium |
| `0x004063B0` | `'WoW.mfil'`, `'Config.wtf'`, `'locale'`, `'dbCompress'`, `'processAffinityMask'`, `'timingMethod'`, `'.\Client.cpp'` | **`InitializeGlobal`** (3.3.5a `Client.cpp:1673`: `LoadMFIL("WoW.mfil")`, CVar registration) | high |
| `0x00667090` | no string/import refs; returns bool | unknown | low |
| `0x00427E80` | no string/import refs | unknown | low |
| `0x00405E50` | `'World of Warcraft'`, `'.PAD'` | unknown (registry/path; possibly `BeginCloseGame`) | low |

## CommonMain control flow (2.4.3, raw addresses)

```
StormInitialize / SErrCatchUnhandledExceptions / CreateNamedEventA / StormSetOption(10,11)
OsSystemEnableCpuLog / SetPaths
SRegLoadValue/SaveValue "SendErrorLogs"
SErrSetLogTitleString("...build 8606") / SErrSetLogCallback(WowLogHeader) / SErrRegisterHandler(SendErrorLog)

0x004065A3F0 ; test al; jne A       # \  preamble not present in 3.3.5a's CommonMain
0x00402460   ; test al; jne A       #  |
0x00402C40                          # /  install-path registry
A: 0x004063B0 ; test al; je C       # if (InitializeGlobal())
   0x00667090 ; test al; je B       #   if (0x667090())
   0x00427E80                       #     0x427E80()
B: 0x00405E50                       #   0x405E50()   (BeginCloseGame?)
C: 0x00648FC0                       # StormDestroy()
```

The `0x004065A3F0 / 0x00402460 / 0x00402C40` preamble and the extra nesting around
`InitializeGlobal` differ from 3.3.5a and still need IDA-quality analysis.
