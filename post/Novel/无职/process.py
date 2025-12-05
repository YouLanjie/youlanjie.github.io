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
    content = inp.read_text(encoding="gbk")

    words = (("鲁迪鸟斯","鲁迪乌斯"), ("卢迪","鲁迪"),
             ("洛克希","洛琪希"), ("艾丽丝","艾莉丝"),
             ("米格尔多","米格路德"), ("瑞杰尔德","瑞杰路德"),
             ("奥尔斯蒂德","奥尔斯帝德"), ("爱莎","爱夏"),
             ("艾丽娜莉兹","艾莉娜丽洁"), ("莉兹","丽洁"),
             ("基司","基斯"), ("飞利浦","菲利普"),
             ("艾丽爱尔","爱丽儿"), ("阿苏拉","阿斯拉"),
             ("格瑞拉特","格雷拉特"),
             ("身分","身份"), ("徵","征"),
             ("计画","计划"),
             )
    for w1,w2 in words:
        print(f"替换 '{w1}' 为 '{w2}' : 共计{len(content.split(w1))-1}处")
        content = content.replace(w1, w2)

    content = content.splitlines()
    groups = []
    now_group = []
    begin = False
    for line in content:
        if line == "":
            continue
        if re.match(r"[　]*(第.*卷.*)", line):
            if now_group:
                groups.append(now_group)
            now_group = []
            begin = True
        if begin:
            now_group.append(line)
    if now_group:
        groups.append(now_group)
    repeat = []
    ind = 1
    contents = []
    content = []
    while ind < len(groups):
        if not repeat:
            repeat = get_same(groups[ind-1][0].split(), groups[ind][0].split())
            if content:
                contents.append(content)
            content = []
            content.append(f"* {" ".join(repeat)}")
            if "插图" not in groups[ind-1][0]:
                content.append(f"** {" ".join(groups[ind-1][0].split()[len(repeat):])}")
            content+=groups[ind-1][1:]
            print(f"==> {repeat}")
            print(f"  --> {groups[ind-1][0].split()[len(repeat):]}")
        if groups[ind][0].split()[:1] != repeat[:1]:
            repeat = []
        else:
            if "插图" not in groups[ind][0]:
                content.append(f"** {" ".join(groups[ind][0].split()[len(repeat):])}")
            content+=groups[ind][1:]
            print(f"  --> {groups[ind][0].split()[len(repeat):]}")
        ind += 1
    if content:
        contents.append(content)
    # import rich
    # rich.print(new_li)
    ind = 1
    for content in contents:
        h1 = content[0][2:]
        outf = Path(f"{ind:03d}_{h1}.org")
        print((outf.is_file(), outf))
        s = "\n\n".join([i for i in content if i])
        outf.write_text(f"""\
#+title: {h1}
#+setupfile: ./setup.setup
""" + s)
        ind += 1

if __name__ == "__main__":
    main()

