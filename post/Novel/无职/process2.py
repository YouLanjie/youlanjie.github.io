#!/usr/bin/python
from pathlib import Path

def main():
    f = Path("./无职转生～到了异世界就拿出真本事～_org-style.txt")
    con = f.read_text().splitlines()
    f = None
    t = ""
    count = 1
    chapter = ""
    for i in con:
        if i.startswith("* "):
            print(i[2:])
            if f:
                f.write_text(t)
            name = i[2:]
            if " ".join(name.split()[:2]) != chapter:
                chapter = " ".join(name.split()[:2])
                f = Path(f"{count:03d}_{chapter}.org")
                count+=1
                t = f"#+title: {chapter}\n#+setupfile: ./setup.setup\n"
        t  += f"{i}\n"
    if f:
        f.write_text(t)

if __name__ == "__main__":
    main()
