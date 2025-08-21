#!/usr/bin/env python
"""构建博客用脚本"""

import argparse
import re
from pathlib import Path
import orgreader2

ARGS = []

def update_file(file:Path) -> tuple[str,str,str,str]:
    """更新文件"""
    if not file.is_file():
        return ("", "", "", "")
    doc = orgreader2.Document(file.read_text(encoding="utf8").splitlines(), str(file))
    doc.setting["css_in_html"] = ""
    doc.setting["js_in_html"] = """\
<script>
window.MathJax = { tex: { ams: { multlineWidth: '85%' }, tags: 'ams', tagSide: 'right', tagIndent: '.8em' },
chtml: { scale: 1.0, displayAlign: 'center', displayIndent: '0em' },
svg: { scale: 1.0, displayAlign: 'center', displayIndent: '0em' },
output: { font: 'mathjax-modern', displayOverflow: 'overflow' } };
</script>
<script id="MathJax-script" async src="/theme/tex-mml-chtml.js"></script>"""
    date = re.sub(r"<(.*)>", r"\1", " ".join(doc.meta["date"]))
    date = re.sub(r"([^ ]*) [一|二|三|四|五|六|日]", r"\1", date)
    outputf = Path(re.sub(r"\.org$", ".html", str(file)))
    ret = (date, str(outputf), " ".join(doc.meta["title"]), " ".join(doc.meta["description"]))
    if outputf.is_dir():
        print(f"ERROR 输出文件名被文件夹占用 - {outputf}")
        return ret
    is_newer = (ARGS and ARGS[0].ignore_time) or \
            (not outputf.exists() or outputf.stat().st_mtime < file.stat().st_mtime)
    if is_newer and ARGS and not ARGS[0].no_update:
        print(f"INFO 输出文件 - {outputf}")
        outputf.write_text(doc.to_html(), encoding="utf8")
    return ret

def fordir(d:Path, node:list, timeline:list):
    """遍历文件夹"""
    if not d.is_dir():
        return
    node.append(d.name)
    for file in sorted(d.iterdir()):
        if file.is_dir():
            subdir = []
            fordir(file, subdir, timeline)
            if len(subdir) > 1:
                node.append(subdir)
            continue
        if file.suffix != ".org":
            continue
        ret = update_file(file)
        node.append(ret)
        timeline.append(ret)

def list_to_str(tree:list, hide_time:bool=False) -> str:
    """构建主页"""
    ret = ""
    for node in tree:
        if isinstance(node, str):
            ret += f"- {node}\n"
            continue
        if isinstance(node, list):
            ret += "  "+"\n  ".join(list_to_str(node, hide_time).splitlines())+"\n"
            continue
        time_format = f"/{node[0]}/ " if not hide_time else ""
        ret += f"  - {time_format}[[{node[1]}][*{node[2]}*]]"
        ret += f"\\\\\n    {node[3]}\n" if node[3] else "\n"
    return ret

def main():
    """主函数"""
    parser=argparse.ArgumentParser(description="构建博客用脚本")
    parser.add_argument("-n", "--no-update", action="store_true", help="不输出文件")
    parser.add_argument("-I", "--ignore-time", action="store_true", help="忽略时间")
    parser.add_argument("-N", "--no-build-home", action="store_true", help="不构建主页")
    ARGS.append(parser.parse_args())
    # args.update
    timeline = []
    tree = []
    for i in sorted(Path("post").iterdir()):
        fordir(i, tree, timeline)
    timeline = sorted(timeline, key=lambda x:x[0], reverse=True)
    if not ARGS[0].no_build_home:
        index_template = r"""#+TITLE: 我的个人博客
# #+OPTIONS: toc:nil
# #+OPTIONS: num:nil
#+setupfile: ./setup.setup
* Welcome
欢迎来到我的个人博客。\\
点击 [[./timeline.html][*/TimeLine/*]] 查看按时间排序的文章列表界面。
在大部分页面点击右上角 [[#][*/UP/*]] 按钮可以回到网页头部。
/Table of Contents/ 是目录，鼠标悬浮或者屏幕点击展开。
如遇代码块中英文对不齐的情况可尝试双击代码块。
* 我的文章（按内容分类）
"""
        print("INFO 构建首页 index.org")
        content_index = index_template+list_to_str(tree,True)
        Path("index.org").write_text(content_index, encoding="utf8")
        update_file(Path("index.org"))

        timeline_template = "#+TITLE: TimeLine\n#+setupfile: setup.setup\n"
        print("INFO 构建时间轴 timeline.org")
        content_timeline = timeline_template+\
                "\n".join([i[2:] for i in list_to_str(timeline).splitlines()])
        Path("timeline.org").write_text(content_timeline, encoding="utf8")
        update_file(Path("timeline.org"))

        update_file(Path("about.org"))
        update_file(Path("404.org"))

if __name__ == "__main__":
    main()

