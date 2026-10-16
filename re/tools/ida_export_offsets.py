"""IDAPython: export function offsets for the 2.4.3 port.

Run inside IDA (File > Script file..., or `idat64 -A -S"re/tools/ida_export_offsets.py" Wow.exe`).
It walks every function in the database and writes, into EXPORT_DIR:

    wow243_offsets.txt           "0x00ADDR<TAB>size<TAB>name" sorted by address
    wow243_offsets_comments.txt  one "// OFFSET: 0xADDR  name" line per function, ready to paste

The offsets are absolute virtual addresses (image base 0x00400000), matching the `// OFFSET:` tags
used by the source tree.
"""
import os

try:
    import idautils
    import idaapi
    import idc
    import ida_funcs
except ImportError:  # pragma: no cover - only runs inside IDA
    raise SystemExit("ida_export_offsets.py must be run inside IDA (IDAPython).")

# Where to write. Override with the WOW243_EXPORT_DIR environment variable.
EXPORT_DIR = os.environ.get("WOW243_EXPORT_DIR", r"F:/Github/wowdecomp/re/243")


def iter_functions():
    for ea in idautils.Functions():
        f = ida_funcs.get_func(ea)
        if not f:
            continue
        name = ida_funcs.get_func_name(f.start_ea) or ("sub_%X" % f.start_ea)
        yield f.start_ea, (f.end_ea - f.start_ea), name


def main():
    os.makedirs(EXPORT_DIR, exist_ok=True)
    funcs = sorted(iter_functions(), key=lambda t: t[0])

    with open(os.path.join(EXPORT_DIR, "wow243_offsets.txt"), "w", encoding="utf-8") as fh:
        for ea, size, name in funcs:
            fh.write("0x%08X\t%d\t%s\n" % (ea, size, name))

    with open(os.path.join(EXPORT_DIR, "wow243_offsets_comments.txt"), "w", encoding="utf-8") as fh:
        for ea, _size, name in funcs:
            fh.write("// OFFSET: 0x%08X  %s\n" % (ea, name))

    print("ida_export_offsets: wrote %d functions to %s" % (len(funcs), EXPORT_DIR))


if __name__ == "__main__":
    main()
