#!/usr/bin/python
from pathlib import Path

def main():
    f = Path("./无职转生～到了异世界就拿出真本事～.org")
    con = f.read_text().splitlines()
    f = None
    t = ""
    count = 1
    chapter = ""
    for i in con:
        if i.startswith("* "):
            if f:
                f.write_text(t)
            name = i[2:]
            num = 2
            nsp = name.split()
            print(nsp)
            if nsp[2][-1] == "篇":
                num = 3
            if " ".join(nsp[:num]) != chapter:
                chapter = " ".join(nsp[:num])
                print(chapter)
                f = Path(f"{count:03d}_{chapter}.org")
                count+=1
                t = f"#+title: {chapter}\n#+setupfile: ./setup.setup\n"
        t  += f"{i}\n"
    if f:
        f.write_text(t)

if __name__ == "__main__":
    main()
