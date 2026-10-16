# wowdecomp — 2.4.3 (The Burning Crusade)

A C++ decompilation of the World of Warcraft 2.4.3 client (`Wow.exe`, build 8606, March 2008).

**This branch (`tbc-2.4.3`) is a skeleton only.** It sets up the TBC source tree layout and the
CMake build so modules can be filled in function by function. Every module directory currently
contains just a `CMakeLists.txt`; there is no ported source yet.

The 3.3.5a tree lives on `main`.

## How it works

Every function is reconstructed from the original binary and keeps the address it came from in an
`// OFFSET:` tag, so each one can be compared against the original. The source tree follows the
layout of the original client (`Engine/Source/<Module>`, `WoW/Source/<Module>`, original file
names).

The original 2.4.3 client (`Wow.exe`, build 8606) is a 32-bit x86 binary. **x64 is the build
target**; Win32 still builds and is the configuration whose struct layouts can be checked against
the 32-bit original.

## Requirements

- Windows 10 or 11
- Visual Studio 2022 with the **Desktop development with C++** workload (MSVC v143 and a Windows SDK)
- CMake 3.10 or newer (the one that ships with Visual Studio works)
- For Win32 builds only: [NASM](https://www.nasm.us/) on `PATH` (the Win32 build assembles FMOD Ex
  `.s`/`.nasm` sources once `SoundEngine` is ported) and `DivxDecoder.dll` from your 2.4.3 client
  copied to `ThirdParty/DivxDecoder/` (the x64 build uses its own `XvidDecoder` instead)
- A World of Warcraft **2.4.3 (8606)** client. No game data is included in this repository.

## Building

```powershell
git clone https://github.com/SatyPardus/wowdecomp.git
cd wowdecomp
git switch tbc-2.4.3

# x64 (main target)
cmake -S . -B build/x64 -G "Visual Studio 17 2022" -A x64
cmake --build build/x64 --config Release --target WowClient --parallel

# Win32 (optional; used to check struct layouts against the 32-bit original)
cmake -S . -B build/win32 -G "Visual Studio 17 2022" -A Win32
cmake --build build/win32 --config Release --target WowClient --parallel
```

In-source builds are refused, so keep the build directory separate (`build/` above).

While this branch is still being ported, the `Wow`/`WowClient` executables are behind
`-DWOWDECOMP_BUILD_CLIENT=ON` (off by default), so an un-ported checkout still configures and builds
the module libraries.

The client is written to `bin/Win/`:

| Target | x64 | Win32 |
|---|---|---|
| `WowClient` | `WowClient64.exe` | `WowClient32.exe` |
| `Wow` | `Wow64.exe` | `Wow32.exe` |

`WowClient` is the client with a crash logger: it opens a console window and writes
`WowClient_crash.log` when the client crashes. `Wow` is the same client without it.

## Layout

| Path | Contents |
|---|---|
| `Engine/Source/` | Engine modules: Storm, Gx (Direct3D 9 / OpenGL), Model2, Frame/FrameXML UI, SoundEngine, Lua, ... |
| `WoW/Source/` | Game modules: objects, world rendering, UI, networking, database, glue screens |
| `WoW/Common/` | Code shared by the game modules |
| `ThirdParty/` | Libraries linked from their upstream sources |
| `Tools/WowClient/` | The `WowClient` executable target |
| `Tools/XvidDecoder/` | x64 movie decoder that replaces the original 32-bit `DivxDecoder.dll` |

See `SKELETON_NOTES.md` for the module list and the items that still need to be verified against the
build 8606 binary.

## Special thanks

- [binana](https://github.com/thunderbrewhq/binana)
- [thunderbrew](https://github.com/thunderbrewhq/thunderbrew)
- [whoa](https://github.com/whoahq/whoa)
- The WoW modding community
