#!/usr/bin/env python
# Created:2025.12.07

from pathlib import Path
import subprocess

def main():
    content = []
    li = sorted(Path().glob("*.org"))
    li = [i for i in li if ("025" not in str(i)) and ("026" not in str(i)) and ("index" not in str(i))]
    print(li)
    for i in li:
        content += i.read_text().splitlines()[2:]
        content += [""]
    outf = Path("tmp.org")
    outf.write_text("\n".join(content))
    outf2 = Path("tmp.tex")
    print("RUN PANDOC...")
    subprocess.run(["pandoc",outf,"--template=pandoc_template.tex","-o",outf2])
    outf.unlink()

if __name__ == "__main__":
    main()

