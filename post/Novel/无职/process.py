#!/usr/bin/env python
# Created:2025.11.29
"""测试用，未完工"""

import re
from pathlib import Path

def get_same(li1:list, li2:list) -> list:
    limit = min(len(li1), len(li2))
    while li1[:limit] != li2[:limit]:
        limit -= 1
    return li1[:limit]

def main():
    inp = Path("./无职转生～到了异世界就拿出真本事～.txt")
    content = inp.read_text(encoding="gbk").splitlines()
    li = []
    for ind,line in enumerate(content):
        if line == "":
            continue
        if re.match(r"[　]*(第.*卷.*)", line):
            # print(f"[{ind:03}] --> {line}")
            li.append((ind, line))
    repeat = []
    last = ""
    new_li = []
    sub_li = []
    for ind,line in li:
        if not repeat:
            if last:
                repeat = get_same(last.split(), line.split())
                sub_li.append((ind, repeat))
                sub_li.append((ind, last.split()[len(repeat):]))
                print(f"==> {repeat}")
                print(f"  --> {last.split()[len(repeat):]}")
                last = ""
            else:
                last = line
                continue
        if line.split()[:1] != repeat[:1]:
            repeat = []
            last = line
            new_li.append(sub_li)
            sub_li = []
            continue
        print(f"  --> {line.split()[len(repeat):]}")
        sub_li.append((ind, line.split()[len(repeat):]))
    if sub_li:
        new_li.append(sub_li)
    # import rich
    # rich.print(new_li)
    for ind,chapters in enumerate(new_li):
        title = " ".join(chapters[0][1])
        outf = Path(f"{ind+1:03d}_{title}.org")
        print((outf.is_file(), outf))
        # cont = content[]
        for i in chapters[1:]:
            pass

if __name__ == "__main__":
    main()

