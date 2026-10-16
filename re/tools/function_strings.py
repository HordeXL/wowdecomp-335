#!/usr/bin/env python3
"""Dump the string literals referenced by every function.

Reads the function inventory from <outdir>/functions.txt, disassembles each function bounded by the
next function start, and writes:

    <outdir>/function_strings.tsv   "0x00ADDR<TAB>str1 | str2 | ..."  (only functions with strings)

Use it to identify functions quickly: `grep <string> re/243/function_strings.tsv`, then confirm the
candidate by cross-referencing the string against the 3.3.5a source (`git grep <string> main`).

Usage: python re/tools/function_strings.py <Wow.exe> <outdir>
"""
import re
import sys
from pathlib import Path

import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_32

HEX = re.compile(r"0x([0-9a-fA-F]{4,8})")


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 1
    pe = pefile.PE(sys.argv[1])
    base = pe.OPTIONAL_HEADER.ImageBase
    text = [s for s in pe.sections if s.Name.rstrip(b"\x00") == b".text"][0]
    tva = base + text.VirtualAddress
    code = text.get_data()

    secs = []
    for s in pe.sections:
        va = base + s.VirtualAddress
        secs.append((va, va + max(s.Misc_VirtualSize, s.SizeOfRawData), s.get_data()))

    def cstr(va):
        for sva, eva, sdata in secs:
            if sva <= va < eva:
                off = va - sva
                end = sdata.find(b"\x00", off, off + 120)
                if end < 0:
                    return None
                raw = sdata[off:end]
                if len(raw) >= 6 and any(65 <= c <= 90 or 97 <= c <= 122 for c in raw) \
                        and all(32 <= c < 127 for c in raw):
                    return raw.decode("latin1")
        return None

    out = Path(sys.argv[2])
    starts = set()
    for line in (out / "functions.txt").read_text(encoding="utf-8").splitlines():
        if line.strip():
            starts.add(int(line.split("\t")[0], 16))

    md = Cs(CS_ARCH_X86, CS_MODE_32)
    rows = []
    for addr in sorted(starts):
        found = []
        seen = set()
        n = 0
        for i in md.disasm(code[addr - tva:addr - tva + 0x800], addr):
            n += 1
            for m in HEX.finditer(i.op_str):
                s = cstr(int(m.group(1), 16))
                if s and s not in seen:
                    seen.add(s)
                    found.append(s)
            nxt = i.address + i.size
            if i.mnemonic in ("ret", "retn") and n > 3:
                break
            if nxt in starts and nxt != addr:
                break
            if n > 400:
                break
        if found:
            rows.append("%08X\t%s" % (addr, " | ".join(found[:40])))

    (out / "function_strings.tsv").write_text("\n".join(rows) + "\n", encoding="utf-8")
    print("function_strings: %d/%d functions reference strings -> %s"
          % (len(rows), len(starts), out / "function_strings.tsv"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
