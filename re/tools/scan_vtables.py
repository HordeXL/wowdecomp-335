#!/usr/bin/env python3
"""Recover virtual-method addresses from MSVC RTTI vtables.

MSVC x86 layout:
    TypeDescriptor      T:  [0]=&type_info vftable, [4]=spare, [8]=name (".?AVClass@@")
    CompleteObjectLocator C: [0]=signature(1), [4]=offset, [8]=cdOffset, [12]=&TypeDescriptor
    vftable             V:  [0]=&CompleteObjectLocator, [4..]=method pointers

Scans for COLs (signature 1, [12] pointing at a TypeDescriptor), then for vtables whose first word
points at a COL, and collects the method pointers. Merges them into <outdir>/functions.txt.

Usage: python re/tools/scan_vtables.py <Wow.exe> <outdir>
"""
import struct
import sys
from pathlib import Path

import pefile


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 1
    pe = pefile.PE(sys.argv[1])
    base = pe.OPTIONAL_HEADER.ImageBase

    secs = []
    for s in pe.sections:
        va = base + s.VirtualAddress
        secs.append((va, va + s.SizeOfRawData, s.get_data()))
    text = [s for s in pe.sections if s.Name.rstrip(b"\x00") == b".text"][0]
    tlo, thi = base + text.VirtualAddress, base + text.VirtualAddress + text.SizeOfRawData
    rdata = [s for s in pe.sections if s.Name.rstrip(b"\x00") == b".rdata"][0]
    rlo, rhi = base + rdata.VirtualAddress, base + rdata.VirtualAddress + rdata.SizeOfRawData

    def dword(va):
        for sva, eva, sdata in secs:
            if sva <= va < eva and va - sva + 4 <= len(sdata):
                return struct.unpack("<I", sdata[va - sva:va - sva + 4])[0]
        return None

    def find_all(needle):
        out = []
        for sva, eva, sdata in secs:
            i = sdata.find(needle)
            while i != -1:
                out.append(sva + i)
                i = sdata.find(needle, i + 1)
        return out

    # TypeDescriptor addresses (name string is at T+8); used only for the report.
    tds = {a - 8 for a in find_all(b".?AV")}

    # A vtable's first word is the RTTI pointer (into .rdata); the following words are method
    # pointers (into .text). Find those runs.
    methods = set()
    vtables = 0
    for sva, eva, sdata in secs:
        off = 0
        n = len(sdata)
        while off + 8 <= n:
            p0 = struct.unpack("<I", sdata[off:off + 4])[0]
            if rlo <= p0 < rhi:
                j = off + 4
                run = []
                while j + 4 <= n:
                    fn = struct.unpack("<I", sdata[j:j + 4])[0]
                    if tlo <= fn < thi:
                        run.append(fn)
                        j += 4
                    else:
                        break
                if run:
                    vtables += 1
                    methods.update(run)
            off += 4

    out = Path(sys.argv[2])
    existing = set()
    fp = out / "functions.txt"
    if fp.exists():
        for line in fp.read_text(encoding="utf-8").splitlines():
            if line.strip():
                existing.add(int(line.split("\t")[0], 16))

    allfn = sorted(existing | methods)
    with open(fp, "w", encoding="utf-8") as fh:
        for a in allfn:
            fh.write("0x%08X\tsub_%X\n" % (a, a))

    print("scan_vtables: %d TDs, %d vtables, %d new vtable methods" % (len(tds), vtables, len(methods - existing)))
    print("functions.txt now has %d functions (was %d)" % (len(allfn), len(existing)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
