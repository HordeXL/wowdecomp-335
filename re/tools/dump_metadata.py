#!/usr/bin/env python3
"""Dump RTTI class names and printable strings from a PE (Wow.exe 2.4.3).

Usage:
    python re/tools/dump_metadata.py <path to Wow.exe> <output dir>

Writes:
    <out>/rtti_classes.txt   one MSVC-mangled RTTI class name per line (sorted, unique)
    <out>/strings.txt        ASCII strings, min length 4 (sorted, unique)
    <out>/strings_utf16.txt  UTF-16LE strings, min length 4 (sorted, unique)
"""
import re
import sys
from pathlib import Path


def uniq_sorted(items):
    return sorted(set(items))


def extract_rtti(data):
    names = set()
    for m in re.finditer(rb"\.\?AV[A-Za-z0-9_@?$<>:`]{1,200}@@", data):
        names.add(m.group(0).decode("latin1"))
    return names


def extract_ascii(data, minlen=4):
    out = set()
    cur = bytearray()
    for b in data:
        if 32 <= b < 127:
            cur.append(b)
        else:
            if len(cur) >= minlen:
                out.add(cur.decode("ascii"))
            cur = bytearray()
    if len(cur) >= minlen:
        out.add(cur.decode("ascii"))
    return out


def extract_utf16(data, minlen=4):
    out = set()
    i = 0
    n = len(data)
    cur = bytearray()
    while i + 1 < n:
        lo, hi = data[i], data[i + 1]
        if hi == 0 and 32 <= lo < 127:
            cur.append(lo)
            i += 2
        else:
            if len(cur) >= minlen:
                out.add(cur.decode("ascii"))
            cur = bytearray()
            i += 1
    if len(cur) >= minlen:
        out.add(cur.decode("ascii"))
    return out


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 1
    exe = Path(sys.argv[1])
    out = Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    data = exe.read_bytes()

    rtti = uniq_sorted(extract_rtti(data))
    ascii_s = uniq_sorted(extract_ascii(data))
    utf16_s = uniq_sorted(extract_utf16(data))

    (out / "rtti_classes.txt").write_text("\n".join(rtti) + "\n", encoding="utf-8")
    (out / "strings.txt").write_text("\n".join(ascii_s) + "\n", encoding="utf-8")
    (out / "strings_utf16.txt").write_text("\n".join(utf16_s) + "\n", encoding="utf-8")

    print(f"rtti_classes: {len(rtti)}")
    print(f"ascii strings: {len(ascii_s)}")
    print(f"utf16 strings: {len(utf16_s)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
