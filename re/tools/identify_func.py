#!/usr/bin/env python3
"""Identify a function by its string and import references.

Disassembles a function and lists every immediate that resolves to a printable string, plus the
imported DLL!function behind each `call dword ptr [IAT]`. Cross-reference the strings against the
3.3.5a source (`git grep <string> main`) to name the function.

Usage: python re/tools/identify_func.py <Wow.exe> <hex addr> [<hex addr> ...]
"""
import re
import struct
import sys

import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_32

HEX = re.compile(r"0x([0-9a-fA-F]+)")


def main():
    exe = sys.argv[1]
    addrs = [int(a, 16) for a in sys.argv[2:]]
    pe = pefile.PE(exe)
    base = pe.OPTIONAL_HEADER.ImageBase
    data = pe.__data__

    secs = []
    for s in pe.sections:
        va = base + s.VirtualAddress
        secs.append((va, va + max(s.Misc_VirtualSize, s.SizeOfRawData), s.get_data()))

    # IAT map
    iat = {}
    for e in pe.DIRECTORY_ENTRY_IMPORT:
        for f in e.imports:
            if f.name:
                iat[f.address] = "%s!%s" % (e.dll.decode(), f.name.decode())

    def read_cstr(va, maxlen=200):
        for sva, eva, sdata in secs:
            if sva <= va < eva:
                off = va - sva
                if off >= len(sdata):
                    return None
                end = sdata.find(b"\x00", off, off + maxlen)
                if end < 0:
                    return None
                raw = sdata[off:end]
                if len(raw) >= 4 and all(32 <= c < 127 for c in raw):
                    return raw.decode("latin1")
        return None

    text = [s for s in pe.sections if s.Name.rstrip(b"\x00") == b".text"][0]
    tva = base + text.VirtualAddress
    code = text.get_data()
    md = Cs(CS_ARCH_X86, CS_MODE_32)

    for addr in addrs:
        print("\n===== sub_%X =====" % addr)
        strings = []
        calls = []
        n = 0
        for i in md.disasm(code[addr - tva:addr - tva + 0x800], addr):
            n += 1
            for m in HEX.finditer(i.op_str):
                v = int(m.group(1), 16)
                if v in iat:
                    calls.append((i.address, iat[v]))
                s = read_cstr(v)
                if s:
                    strings.append((i.address, s))
            if n > 300 or (i.mnemonic == "ret" and n > 5):
                break
        seen = set()
        for a, s in strings:
            if s in seen:
                continue
            seen.add(s)
            print("  str  %08X  %r" % (a, s))
        for a, c in calls:
            print("  call %08X  %s" % (a, c))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
