#!/usr/bin/env python
# Created:2025.11.23

from pathlib import Path

outf = Path("无职合集.org")

s = ["#+title: 无职転生合集", "#+setupfile: ./setup.setup"]
for i in sorted(Path().glob("0*.org")):
    print(i)
    s += i.read_text().splitlines()[2:]
outf.write_text("\n".join(s))
