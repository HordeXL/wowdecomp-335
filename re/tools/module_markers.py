#!/usr/bin/env python3
"""Count module markers in the dumped strings / RTTI, to sanity-check the module layout.

Usage: python re/tools/module_markers.py <dir with rtti_classes.txt + strings.txt>
"""
import sys
from pathlib import Path

MARKERS = [
    "battle.net", "battlenet", "gluexml", "framexml", "comsat", "voice",
    "shader", "minigame", "steelseries", "warden", "tempest", "cggameui",
    "interface\\", "sound\\", "textures\\", "mpq", ".toc", "scan.dll",
    "realmlist", "lua", "storm", "memcpy",
]


def main():
    d = Path(sys.argv[1] if len(sys.argv) > 1 else "re/243")
    strings = (d / "strings.txt").read_text(encoding="utf-8").splitlines()
    rtti = (d / "rtti_classes.txt").read_text(encoding="utf-8").splitlines()
    low = [s.lower() for s in strings]
    print(f"strings={len(strings)} rtti={len(rtti)}")
    for k in MARKERS:
        n = sum(1 for x in low if k in x)
        print(f"  {k:<14} {n}")
    print("\nRTTI class families:")
    fams = ["CGx", "CSimple", "NTempest", "CGObject", "CWorld", "CChar", "CGlue", "CSpell"]
    for f in fams:
        hits = [x for x in rtti if f in x]
        print(f"  {f:<10} {len(hits)}  {hits[:2]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
