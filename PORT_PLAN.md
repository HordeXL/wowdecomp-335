# 2.4.3 (TBC) port plan

Plan for the remaining work on the `tbc-2.4.3` branch: turning the skeleton + entry chain into a
playable 2.4.3 (build 8606) client. Work items are ordered so that everything not blocked on an IDA
database is done first.

## 0. Current state

Done and committed:

- **Skeleton** — `Engine/Source/*` + `WoW/*` module tree for TBC, per-module `CMakeLists.txt` with an
  INTERFACE fallback, x64 build target with Win32 as the layout-verification config, and the
  `Wow`/`WowClient` executables behind `-DWOWDECOMP_BUILD_CLIENT` (default off) so the tree builds.
- **Boot layer (partial)** — `WoW/Source/Win32/WinMain.cpp` (`start` 0x401000, `WinMain` 0x406870)
  and `WoW/Source/Client.{h,cpp}` (`CommonMain` 0x406790).
- **Tooling + metadata** — `re/tools/` (7 scripts) and `re/243/` (function inventory of 10,802,
  RTTI, strings, string→source hints for 1,027 functions).
- **Fingerprint** — build 2.4.3.8606, VS2005/msvc80, image base 0x400000, entry 0x401000, embedded
  PDB path `WoW-code\branches\wow-patch-2_4_3-branch\WoW\Bin\Wow.pdb`.

## 1. Blockers / prerequisites (external)

| # | Item | Why | Status |
|---|---|---|---|
| B1 | A **pristine retail 2.4.3.8606 `Wow.exe`** | the supplied client is a modified private-server build (patched `Wow*.exe`, `Scan.dll`, ReShade) | open |
| B2 | **IDA** with the 8606 IDB (or a community IDB) | functions without strings/vtables cannot be named or reconstructed reliably without xrefs/types | open |
| B3 | `ThirdParty/DivxDecoder/DivxDecoder.dll` copied in | Win32 client build needs it | open |

Nothing in Phase 1 depends on B1–B3. Phases 2+ do.

## 2. Methodology

- Every function carries `// OFFSET: 0xADDR` (its address in the original) and, once verified,
  `// VERIFY: <hash> auto|manual` (re/r/tools/verify.py in the 3.3.5a workflow).
- Ports are written against the 3.3.5a source (`git show main:<file>`) where the binary matches, then
  corrected for 2.4.3 differences (build strings, feature set, addresses).
- The build must stay **configuration-clean**; `WOWDECOMP_BUILD_CLIENT` is flipped on only when the
  client is far enough to link.

## 3. Phases

### Phase 1 — Finish the boot layer (no IDA needed)

| # | Work item | Deliverable | Status |
|---|---|---|---|
| P1.1 | Identify the 4 remaining `CommonMain` callees (0x65A3F0, 0x402460, 0x667090, 0x427E80) via call-graph/behavior analysis | named in `re/243/entry_functions.md` | **done** |
| P1.2 | Port `0x749F20` (process DACL hardening: OpenProcessToken/SetSecurityInfo) | `ProtectProcessSecurity` in `WinMain.cpp` | **done** |
| P1.3 | Finalize `CommonMain` with the real control flow | `WoW/Source/Client.cpp` game-loop block | blocked (game loop needs IDA) |
| P1.4 | Port `WoW/Source/Win64/WinMain.cpp` (x64 counterpart) from the 3.3.5a source | x64 build reaches `CommonMain` | open |
| P1.5 | Port the other Client.cpp entry helpers that are string-identifiable (`SetPaths`/`SetInstallPath` family) | `// OFFSET:` functions in `Client.cpp` | open |

### Phase 2 — Foundation modules (bottom-up, IDA-assisted)

Order by dependency, smallest first:

| Order | Module | 3.3.5a .cpp | Notes |
|---|---|---:|---|
| 1 | `Engine/Source/Storm` | 43 | memory, MPQ, SErr, SCmd, crypto — everything depends on it |
| 2 | `Engine/Source/Base` | 18 | |
| 3 | `Engine/Source/BlizzardCore` | 84 | streaming/manifests |
| 4 | `Engine/Source/Os` | 44 | time, system |
| 5 | `Engine/Source/Event` | 12 | event queue/scheduler |
| 6 | `WoW/Source/DB` | 249 | DBC/DB2 loading |

### Phase 3 — Engine modules

`Gx` (23) + `Gxu` (11), `Model2` (8), `Images` (3) + `BLPFile` + `jpeg`, `Frame` (67) +
`FrameScript` (3) + `FrameXML` (3), `Tempest` (27), `Services` (14), `Scrn` (3), `FFX` (6),
`ShaderEffect` (4), `ConsoleBase`, `lua-5.1`, `pcre`, `ComSat` (36).
`SoundEngine` (166) additionally needs the **vendored FMOD Ex + NASM** build restored.

### Phase 4 — Game modules

`Net` (2), `Object` (91) + `ObjectAlloc` (4) + `ObjectMgrClient` (3), `WorldClient` (58),
`SoundInterface` (16), `UIUtil` (20), `Ui` (186 — the `*_Scripts.cpp` files dominate), `Glue` (19),
`Magic` (8 — `Spell_C.cpp` alone is 164 hinted functions), `LiquidSystem` (11), `Game` (35),
`Console` (2), `ConsoleDevice` (4), `WoW/Common` (7).

### Phase 5 — Integration & verification

- Flip `WOWDECOMP_BUILD_CLIENT=ON`, fix the link line, resolve the crash logger.
- Build the x64 + Win32 executables; run against `Data/`.
- Add/replace `re/tools/verify.py` to check struct layouts and function hashes.
- Milestones: **M3** reaches the Glue login screen; **M4** enters the world.

## 4. Reusable aids

- `re/243/function_hints.tsv` — which 3.3.5a source file each 2.4.3 function likely belongs to.
  `grep <addr>` / `cut -f3 | sort | uniq -c` for a per-module work list.
- `re/243/function_strings.tsv` — each function's string references.
- 3.3.5a source via `git show main:<file>`.

## 5. Milestones

| M | Definition |
|---|---|
| M1 | Boot layer complete (Phase 1); client reaches `CommonMain` with the real game-loop block |
| M2 | Storm + Base ported; memory/file subsystems work |
| M3 | Glue login screen renders |
| M4 | Client enters the world |

## 6. Immediate next step

**P1.1** — identify the 4 remaining `CommonMain` callees by disassembling them and tracing their
calls/globals, since it needs no IDA and unblocks P1.3.
