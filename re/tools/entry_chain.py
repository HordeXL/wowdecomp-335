#!/usr/bin/env python3
"""Disassemble the Wow.exe entry chain (start -> WinMainCRTStartup -> WinMain -> fiber -> main).

Usage: python re/tools/entry_chain.py <path to Wow.exe>

Locates the fiber-API xrefs (ConvertThreadToFiber / CreateFiberEx / SwitchToFiber / DeleteFiber)
to find WinMain and the fiber procedure, and disassembles the entry point.
"""
import struct
import sys

import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_32

FIBER_APIS = ["ConvertThreadToFiber", "CreateFiberEx", "SwitchToFiber", "DeleteFiber"]


def main():
    pe = pefile.PE(sys.argv[1], fast_load=True)
    pe.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_IMPORT"]])
    image_base = pe.OPTIONAL_HEADER.ImageBase
    entry = image_base + pe.OPTIONAL_HEADER.AddressOfEntryPoint

    text = None
    for s in pe.sections:
        if s.Name.rstrip(b"\x00") == b".text":
            text = s
    text_va = image_base + text.VirtualAddress
    text_data = text.get_data()

    md = Cs(CS_ARCH_X86, CS_MODE_32)
    md.detail = False

    def disasm(va, n=40):
        off = va - text_va
        for insn in md.disasm(text_data[off:off + n * 8], va):
            print(f"  {insn.address:08X}  {insn.mnemonic:<6} {insn.op_str}")
            if insn.mnemonic in ("ret", "jmp") and "[" not in insn.op_str:
                pass
        return

    print(f"image base {image_base:08X}, entry {entry:08X}")
    print("\n== entry point ==")
    disasm(entry, 12)

    # IAT addresses of the fiber APIs
    iat = {}
    for imp in pe.DIRECTORY_ENTRY_IMPORT:
        for f in imp.imports:
            if f.name:
                n = f.name.decode()
                if n in FIBER_APIS:
                    iat[n] = f.address

    print("\n== fiber API IAT ==")
    for k, v in iat.items():
        print(f"  {k:<22} {v:08X}")

    # find `call dword ptr [iat]` (FF 15 xx xx xx xx) references
    print("\n== xrefs to fiber APIs ==")
    for name, addr in iat.items():
        pat = b"\xff\x15" + struct.pack("<I", addr)
        start = 0
        while True:
            i = text_data.find(pat, start)
            if i < 0:
                break
            print(f"  {name:<22} at VA {text_va + i:08X}")
            start = i + 1

    # disassemble around the first CreateFiberEx xref (likely WinMain)
    if "CreateFiberEx" in iat:
        pat = b"\xff\x15" + struct.pack("<I", iat["CreateFiberEx"])
        i = text_data.find(pat)
        if i >= 0:
            print(f"\n== around CreateFiberEx xref (VA {text_va + i:08X}) ==")
            disasm(text_va + i - 0x40, 40)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
