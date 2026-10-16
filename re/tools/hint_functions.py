#!/usr/bin/env python3
"""Hint at each function's identity from the string literals it references.

Builds a "string literal -> source files that contain it" index from an extracted copy of the
3.3.5a source tree, then scores each function in function_strings.tsv against it by shared strings.

Usage:
    # once:
    git archive main -- WoW/Source Engine/Source WoW/Common | tar -x -C /tmp/wow335src
    # then:
    python re/tools/hint_functions.py /tmp/wow335src re/243/function_strings.tsv re/243/function_hints.tsv

Output: "0x00ADDR<TAB>score<TAB>top_file<TAB>other_files<TAB>matched_strings".
A hint is a lead, not a match: confirm against the source.
"""
import re
import sys
from collections import Counter
from pathlib import Path

LIT = re.compile(r'"((?:[^"\\]|\\.)*)"')


def unescape(s):
    out = []
    i = 0
    while i < len(s):
        c = s[i]
        if c == "\\" and i + 1 < len(s):
            n = s[i + 1]
            out.append({"n": "\n", "t": "\t", "r": "\r", "\\": "\\", '"': '"', "0": "\0"}.get(n, n))
            i += 2
        else:
            out.append(c)
            i += 1
    return "".join(out)


def main():
    src_dir = Path(sys.argv[1])
    tsv = Path(sys.argv[2])
    out = Path(sys.argv[3])

    index = {}
    for p in src_dir.rglob("*"):
        if p.suffix not in (".cpp", ".h"):
            continue
        rel = p.relative_to(src_dir).as_posix()
        text = p.read_text(encoding="utf-8", errors="ignore")
        for m in LIT.finditer(text):
            s = unescape(m.group(1))
            if len(s) >= 6:
                index.setdefault(s, set()).add(rel)

    rows = []
    for line in tsv.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        addr, rest = line.split("\t", 1)
        strs = [s.strip() for s in rest.split(" | ") if s.strip()]
        files = Counter()
        matched = []
        for s in strs:
            fl = index.get(s)
            if fl:
                matched.append(s)
                for f in fl:
                    files[f] += 1
        if not files:
            continue
        ranked = files.most_common()
        top, top_score = ranked[0]
        others = ";".join("%s(%d)" % (f, n) for f, n in ranked[1:4])
        rows.append("%s\t%d\t%s\t%s\t%s" % (addr, top_score, top, others, " | ".join(matched)))

    out.write_text("\n".join(rows) + "\n", encoding="utf-8")
    print("hint_functions: %d functions matched -> %s" % (len(rows), out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
