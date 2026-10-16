# 2.4.3 (build 8606) metadata dump

Derived from a `Wow.exe` 2.4.3.8606 client with:

```
python re/tools/dump_metadata.py "<path to Wow.exe>" re/243
```

| File | Contents |
|---|---|
| `rtti_classes.txt` | MSVC-mangled RTTI class names (255) |
| `strings.txt` | ASCII strings, min length 4 (23,453 unique) |
| `strings_utf16.txt` | UTF-16LE strings, min length 4 (129 unique) |
| `functions.txt` | Function inventory (10,802): `scan_functions.py` direct-call targets + `scan_vtables.py` RTTI vtable methods |
| `entry_chain.md` | Disassembly of the `start`/`WinMain`/`CommonMain` chain |
| `entry_functions.md` | Entry-chain + `CommonMain` callee identification (string/import evidence) |
| `function_map.md` | Identified Storm/Os/operator addresses with confidence levels |
| `function_strings.tsv` | Per-function string references (1,530 of the 10,802 functions reference strings) |
| `function_hints.tsv` | Functions scored against the 3.3.5a source by shared strings (1,027 matched) |

### Functions by source file (hints)

`cut -f3 function_hints.tsv | sort | uniq -c | sort -rn` — where the string-referencing functions
likely live:

```
164  WoW/Source/Magic/MagicClient/Spell_C.cpp
 61  WoW/Source/Ui/ScriptEvents_Scripts.cpp
 36  WoW/Source/Ui/ChatFrame_Scripts.cpp
 33  WoW/Source/Ui/GameUI_Scripts.cpp
 32  WoW/Source/Glue/GlueScriptEvents_Scripts.cpp
 27  Engine/Source/Storm/Source/Win32/MachineState.cpp
 26  WoW/Source/Client.cpp
 21  WoW/Source/WorldClient/MapObj.cpp
 21  WoW/Source/Ui/MailInfo_Scripts.cpp
 21  Engine/Source/Storm/Source/Win64/SErr.cpp
 20  WoW/Source/Ui/ClassTrainerFrame_Scripts.cpp
 18  WoW/Source/UIUtil/Tooltip_Scripts.cpp
```

`Win64/` in the paths is just where the 3.3.5a tree keeps that code; the 2.4.3 code is the same
source, compiled 32-bit. Hints are leads, not matches — confirm each against the source.

## Fingerprint

- Build **2.4.3.8606**; PE linker **8.00 → VS2005 (msvc80)**.
- Image base `0x00400000`, entry point `0x00401000`, 32-bit x86.
- Embedded original PDB path: `e:\BuildServer\bs2\work\WoW-code\branches\wow-patch-2_4_3-branch\WoW\Bin\Wow.pdb`.

## Module markers (see `re/tools/module_markers.py`)

Confirms the skeleton module list against the binary:

| Marker | Hits | Reading |
|---|---:|---|
| `comsat` | 20 | **ComSat present** (keep) |
| `voice` | 112 | voice chat present |
| `shader` | 76 | ShaderEffect likely present |
| `minigame` | 8 | Minigame likely present |
| `tempest` / `NTempest` (RTTI) | 7 / 6 | **Tempest present** |
| `warden` | 5 | Warden (anti-cheat) present |
| `gluexml` / `framexml` / `.toc` | 6 / 9 / 5 | FrameXML/GlueXML UI present |
| `mpq` | 40 | MPQ/Storm present |
| `steelseries` | 0 | **SteelseriesMouse absent** (correctly removed) |
| `battlenet` / `battle.net` | 0 / 1 | **no Battlenet module** (correctly removed) |

RTTI class families: `CGx*` (7), `CSimple*` (7), `NTempest*` (6), `CGObject*` (2), `CWorld*` (2).

## Caveat

The source client is a **modified private-server build** (patched `Wow*.exe` variants, `Scan.dll`,
ReShade, custom `opengl32.dll`). `.text` is genuine 2.4.3.8606 apart from a few hundred patched bytes.
Prefer a pristine retail `Wow.exe` before locking addresses.
