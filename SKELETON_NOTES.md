# 2.4.3 skeleton notes

This branch is a **layout + CMake skeleton** for the 2.4.3 (build 8606) client. Each module directory
holds only a `CMakeLists.txt`; sources are added as the port progresses.

## Confirmed fingerprint (from the supplied client, `E:\Program Files\WoW 2.43`)

- **Build**: version resource `2, 4, 3, 8606` → 2.4.3.8606.
- **Toolchain**: PE linker version **8.00 → VS2005 (msvc80)**, so the root `CMakeLists.txt` settings
  (`/arch:IA32`, `/fp:fast`, `_USE_32BIT_TIME_T`) hold.
- **Layout**: image base `0x00400000`, entry point `0x00401000`, 32-bit x86, 6 sections
  (`.text/.rdata/.data/.zdata/.tls/.rsrc`). Code is statically linked (no MSVCR import).
- **Original PDB path still embedded**: `e:\BuildServer\bs2\work\WoW-code\branches\wow-patch-2_4_3-branch\WoW\Bin\Wow.pdb`
  — the original tree root was `WoW-code`, branch `wow-patch-2_4_3-branch`, game module `WoW`.
- **RTTI** confirms `NTempest` (Tempest), `CGx*`, `CSimple*`, `CGObject_C`, `CWorldOccluder`, so the
  Tempest, Gx, Frame/UI, World and Object modules are present. `Warden` (anti-cheat) is present.

⚠ The supplied client is a **modified private-server build**: several patched `Wow*.exe` variants
(anti-cheat "去验证" bypass, 40-yard nameplates) whose `.text` differs by a few hundred bytes from each
other, plus `Scan.dll`, ReShade and a custom `opengl32.dll`. `Wow.exe`/`WowClassic.exe` also carry an
extra non-ASCII-named RWX section. The bulk of `.text` is still genuine 2.4.3.8606, but a pristine
retail `Wow.exe` is preferable before locking addresses.

## Module layout

Derived from the 3.3.5a tree, trimmed to what The Burning Crusade is expected to have.

### Engine/Source/

`Base`, `BlizzardCore`, `BLPFile`, `ComSat` ⚠, `ConsoleBase`, `Event`, `FFX`, `Frame`, `FrameScript`,
`FrameXML`, `Gx`, `Gxu`, `Images`, `jpeg`, `lua-5.1`, `Model2`, `Os`, `pcre`, `Scrn`, `Services`,
`ShaderEffect` ⚠, `SoundEngine`, `Storm`, `Tempest` ⚠

### WoW/

- `WoW/Common/` → target `WoWCommon`
- `WoW/Source/`: `Console`, `ConsoleDevice`, `DB`, `Game`, `Glue`, `Magic`, `LiquidSystem`, `Minigame` ⚠,
  `Net`, `Object`, `ObjectAlloc`, `ObjectMgrClient`, `SoundInterface`, `UIUtil`, `Ui`, `WorldClient`

### Removed relative to 3.3.5a

- `Engine/Source/SteelseriesMouse` — SteelSeries peripheral support is believed to be a WotLK-era
  addition. ⚠ verify.
- `WoW/Source/Battlenet`, `WoW/Source/WowServices`, `WoW/Source/WowSvcs` — Battle.net integration did
  not exist in 2.4.3.

## Items to verify against the real build 8606 binary

⚠-marked modules are best-effort guesses from feature history. Confirm each against `Wow.exe`:

1. **Module existence** — confirmed against `Wow.exe` strings/RTTI (see `re/243/README.md`): `Tempest`,
   `ComSat`, `ShaderEffect`, `Minigame` present; `SteelseriesMouse` and `Battlenet` absent. Remaining:
   lock the exact folder/file names.
2. **Module naming / file names** — recover from RTTI, string tables and embedded paths, then lock the
   layout to them. The embedded PDB path (`WoW-code\branches\wow-patch-2_4_3-branch\WoW\...`) is a start.
3. **Compiler / runtime fingerprint** — **confirmed**: VS2005 / msvc80 (linker 8.00).

## Deviations from the 3.3.5a CMake

- Architecture follows the parent project: **x64 is the build target, Win32 stays buildable** as the
  configuration whose struct layouts are checked against the 32-bit original. `Tools/XvidDecoder`
  (restored from `main`) is built for x64, matching `ThirdParty`'s `DivxDecoder` expectation.
- Modules are empty, so each `CMakeLists.txt` falls back to an `INTERFACE` stub when its source glob
  is empty. This keeps `cmake` configurable with no source files. `target_link_libraries(... PRIVATE ...)`
  is replaced by `INTERFACE` in that stub (PRIVATE is illegal on an INTERFACE library before CMake 3.19).
- `Engine/Source/SoundEngine/CMakeLists.txt` is simplified: the 3.3.5a tree vendored FMOD Ex under
  `fmodex/` and assembled it with NASM. That payload and build step must be restored when SoundEngine
  is ported (NASM is not otherwise a build dependency).
- `Engine/Source/pcre` builds target `pcreposix`; the third-party `pcre` lives in `ThirdParty/`.
- `Engine/Source/lua-5.1` builds target `lua`.
- The `Wow`/`WowClient` executables are behind `-DWOWDECOMP_BUILD_CLIENT=ON` (default off), so the
  skeleton configures and builds the module libraries while the client is still being ported.

## Ported so far

- `WoW/Source/Win32/WinMain.cpp` — `start` (0x00401000) and `WinMain` (0x00406870). 2.4.3 has no
  fiber startup, unlike 3.3.5a.
- `WoW/Source/Client.cpp` / `Client.h` — `CommonMain` (0x00406790); the game-loop block (calls at
  0x0040682A) is still a TODO.

Analysis artifacts live under `re/243/` and `re/tools/`.
