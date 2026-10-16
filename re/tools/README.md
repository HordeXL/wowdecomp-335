# re/tools

Reverse-engineering helpers for the 2.4.3 (build 8606) port. None of these are part of the build;
they produce reference data consumed while filling in the source tree.

Python scripts here need `pefile` and `capstone` (`pip install pefile capstone`). The IDA script runs
inside IDA's IDAPython.

## Scripts

| Script | Purpose |
|---|---|
| `dump_metadata.py <Wow.exe> <outdir>` | Dump RTTI class names and printable strings (see `re/243/`). |
| `module_markers.py <outdir>` | Count module markers in the dumped strings/RTTI to sanity-check the module layout. |
| `entry_chain.py <Wow.exe>` | Disassemble the entry point and locate the entry-chain functions. |
| `identify_func.py <Wow.exe> <hex addr>...` | List a function's string and import references to identify it (cross-reference with `git grep` on the 3.3.5a source). |
| `scan_functions.py <Wow.exe> <outdir>` | Recursive-descent function inventory (precise but incomplete). |
| `scan_vtables.py <Wow.exe> <outdir>` | Recover virtual methods from MSVC RTTI vtables; merges them into `functions.txt`. |
| `function_strings.py <Wow.exe> <outdir>` | Dump the string literals each function references. |
| `hint_functions.py <srcdir> <function_strings.tsv> <out>` | Score functions against the 3.3.5a source by shared strings. |
| `ida_export_offsets.py` | **Run inside IDA.** Export every function's address and name as `// OFFSET:` lines. |

## Typical workflow

```powershell
# 1. Metadata from the exe (no IDA needed)
python re/tools/dump_metadata.py "E:/Program Files/WoW 2.43/Wow.exe" re/243
python re/tools/module_markers.py re/243

# 2. Entry chain
python re/tools/entry_chain.py "E:/Program Files/WoW 2.43/Wow.exe"

# 3. Inside IDA, on Wow.exe (build the IDB first)
#    File > Script file... > re/tools/ida_export_offsets.py
#    -> re/243/wow243_offsets.txt
#    -> re/243/wow243_offsets_comments.txt  (// OFFSET: 0x00XXXXXX  name, ready to paste)
#    Or headless:
idat64 -A -S"re/tools/ida_export_offsets.py" "E:/Program Files/WoW 2.43/Wow.exe"
```

Set `WOW243_EXPORT_DIR` to change where `ida_export_offsets.py` writes.
