# 2.4.3 entry chain

Disassembled from `Wow.exe` 2.4.3.8606 with `re/tools/entry_chain.py` (capstone). Image base
`0x00400000`.

| Address | Name | Notes |
|---|---|---|
| `0x00401000` | `start` | `call 0x00643020` (StormRtlInitialize); `jmp 0x0040A552` (WinMainCRTStartup) |
| `0x0040A552` | `WinMainCRTStartup` | CRT: `call 0x0040CE21` (_security_init_cookie); `jmp 0x0040A372` (__tmainCRTStartup) |
| `0x0040A372` | `__tmainCRTStartup` | CRT |
| `0x00406870` | **`WinMain`** | called by the CRT with `(hInstance=0x400000, 0, lpCmdLine, nShowCmd)`; `ret 0x10` |
| `0x0046C7E0` | `InvalidParameterHandler` | single `ret` (empty handler) |
| `0x00749F20` | *unknown* | process setup, references `GetCurrentProcess`; called by WinMain |
| `0x00406790` | `CommonMain` *(inferred)* | game entry; called by WinMain; `ret` |

## WinMain body (0x00406870)

```
00406870  push 0x46C7E0          ; InvalidParameterHandler
00406875  call 0x40B2B0          ; _set_invalid_parameter_handler
0040687A  call 0x40ADD0          ; _clearfp
0040687F  push -1
00406881  push 0x9001F
00406886  call 0x40AEA7          ; _control87(0x9001F, 0xFFFFFFFF)
0040688B  add  esp, 0xC
0040688E  call 0x749F20          ; process setup (unknown)
00406893  call 0x406790          ; CommonMain
00406898  ret  0x10
```

## Difference from 3.3.5a

3.3.5a's `WinMain` creates a fiber (`ConvertThreadToFiber` / `CreateFiberEx` / `SwitchToFiber`) and
runs `main()` on it. **2.4.3 does not use fibers** — there is no fiber import, no `MainFiberProc`,
and no separate `main`; `WinMain` runs the CRT setup inline and calls `CommonMain` directly.

The `start` shape (`StormRtlInitialize` then tail-jump to `WinMainCRTStartup`) and the
`_control87(0x9001F, 0xFFFFFFFF)` call match 3.3.5a.

Ported into `WoW/Source/Win32/WinMain.cpp`. `0x00406790` and `0x00749F20` still need to be identified
and ported.
