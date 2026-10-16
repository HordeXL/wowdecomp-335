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
| `functions.txt` | Function inventory from `scan_functions.py` (7,824 direct-call targets; incomplete — misses vtable-only methods) |
| `entry_chain.md` | Disassembly of the `start`/`WinMain`/`CommonMain` chain |
| `entry_functions.md` | Entry-chain + `CommonMain` callee identification (string/import evidence) |

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
