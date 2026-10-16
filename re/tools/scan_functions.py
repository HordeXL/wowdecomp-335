#!/usr/bin/env python3
"""Recursive-descent function inventory for Wow.exe (no IDA needed).

Walks the code from the entry point (fall-through + direct call/jmp targets) and records every
function start. Writes, into <outdir>:

    functions.txt   "0x0086XXXX\tsub_86XXXX" for every discovered function, sorted by address

This is a substitute for the IDA export (`ida_export_offsets.py`) when IDA is unavailable. Code only
reached through data (vtables, function-pointer tables) is missed.

Usage: python re/tools/scan_functions.py <Wow.exe> <outdir>
"""
import sys
from pathlib import Path

import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_32

COND_JMP = {
    "ja", "jae", "jb", "jbe", "jc", "je", "jg", "jge", "jl", "jle", "jna", "jnae",
    "jnb", "jnbe", "jnc", "jne", "jng", "jnge", "jnl", "jnle", "jno", "jnp", "jns",
    "jnz", "jo", "jp", "jpe", "jpo", "js", "jz", "jcxz", "jecxz",
}


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 1
    pe = pefile.PE(sys.argv[1], fast_load=True)
    base = pe.OPTIONAL_HEADER.ImageBase
    text = [s for s in pe.sections if s.Name.rstrip(b"\x00") == b".text"][0]
    tva = base + text.VirtualAddress
    code = text.get_data()
    lo, hi = tva, tva + len(code)

    md = Cs(CS_ARCH_X86, CS_MODE_32)

    entry = base + pe.OPTIONAL_HEADER.AddressOfEntryPoint
    starts = {entry}
    worklist = [entry]
    visited = set()

    # NOTE: no prologue heuristic. "push ebp; mov ebp, esp" appears constantly inside real code and
    # data, so seeding on it floods the list with false starts (100k+). This scan only records
    # functions reachable through direct calls, which is precise but incomplete: methods called only
    # through vtables / function-pointer tables are not found. Use IDA (`ida_export_offsets.py`) for
    # the complete list.

    def target_of(op):
        if op.startswith("0x"):
            try:
                return int(op, 16)
            except ValueError:
                return None
        return None

    while worklist:
        ea = worklist.pop()
        while lo <= ea < hi and ea not in visited:
            visited.add(ea)
            insns = list(md.disasm(code[ea - tva:ea - tva + 16], ea))
            if not insns:
                break
            insn = insns[0]
            nxt = ea + insn.size
            m = insn.mnemonic
            t = target_of(insn.op_str)
            if m == "call":
                if t is not None and lo <= t < hi and t not in starts:
                    starts.add(t)
                    worklist.append(t)
            elif m == "jmp":
                if t is not None and lo <= t < hi:
                    if t not in starts:
                        starts.add(t)
                        worklist.append(t)
                    break
            elif m in COND_JMP:
                if t is not None and lo <= t < hi and t not in starts:
                    starts.add(t)
                    worklist.append(t)
            elif m in ("ret", "retn", "int3", "hlt", "ud2"):
                break
            ea = nxt

    out = Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    starts_sorted = sorted(starts)
    with open(out / "functions.txt", "w", encoding="utf-8") as fh:
        for a in starts_sorted:
            fh.write("0x%08X\tsub_%X\n" % (a, a))

    print("scan_functions: %d functions (%d instructions visited)" % (len(starts_sorted), len(visited)))
    print("wrote %s" % (out / "functions.txt"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
