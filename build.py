#!/usr/bin/env python
"""构建博客用脚本"""

import argparse
import re
from pathlib import Path
import orgreader2

ARGS = None

def update_file(file:Path) -> tuple[str,str,str,str]:
    """更新文件"""
    if not file.is_file():
        return ("", "", "", "")
    outputf = Path(re.sub(r"\.org$", ".html", str(file)))
    content = ""
    is_newer = (ARGS and ARGS.ignore_time) or \
            (not outputf.exists() or outputf.stat().st_mtime < file.stat().st_mtime)
    if not is_newer and ARGS and ARGS.no_build_home:
        return ("", str(outputf), str(outputf), "[NONUPDATE]")

    try:
        content = file.read_text(encoding="utf8")
    except UnicodeDecodeError:
        try:
            content = file.read_text(encoding="gbk")
        except UnicodeDecodeError:
            orgreader2.pytools.print_err(f"[ERROR] '{file}' 既不是utf8也不是gbk编码")
            return ("", str(outputf), f"[ERROR]{file}", "既不是utf8也不是gbk编码")

    content = content.splitlines()
    if not is_newer and len(content) > 1000:
        content = content[:1000]    # 偷偷摸摸限制长度提高读取速度(实际上是在偷懒)
    doc = orgreader2.Document(content, str(file))
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
    ret = (date, str(outputf), " ".join(doc.meta["title"]), " ".join(doc.meta["description"]))
    if outputf.is_dir():
        print(f"ERROR 输出文件名被文件夹占用 - {outputf}")
        return ret
    if is_newer and ARGS and not ARGS.no_update:
        print(f"INFO 输出文件 - {outputf}")
        outputf.write_text(doc.to_html(), encoding="utf8")
    return ret

BLACKLIST = {"post/Novel/SAO/",
             "post/Novel/无职/"}
WHITELIST = {"post/Novel/SAO/index.html",
             "post/Novel/无职/index.html"}

def check_list(s:str, li:list|set) -> bool:
    """检查文件s是否在列表内"""
    for i in li:
        if s.startswith(i):
            return True
    return False

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
        if ret[1] and (not check_list(ret[1], BLACKLIST) or check_list(ret[1], WHITELIST)):
            node.append(ret)
            timeline.append(ret)

def list_to_str(tree:list, hide_time:bool=False) -> str:
    """将文件列表转为org字符串"""
    ret = ""
    for node in tree:
        if isinstance(node, str):
            ret += f"- {node}\n"
            continue
        if isinstance(node, list):
            ret += "  "+"\n  ".join(list_to_str(node, hide_time).splitlines())+"\n"
            continue
        time_format = f" /[{node[0] or "NULL"}]/" if not hide_time else ""
        ret += f"  - [[./{node[1]}][*{node[2]}*]]{time_format}"
        ret += f"\\\\\n    {node[3]}\n" if node[3] else "\n"
    return ret

def build_homepage(tree:list, timeline:list):
    """构建主页和时间线"""
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
* 我的文章（按目录结构排列）
"""
    print("INFO 构建首页 index.org")
    content_index = index_template+re.sub(r"^\- ", "** ", list_to_str(tree,True), flags=re.M)
    Path("index.org").write_text(content_index, encoding="utf8")
    update_file(Path("index.org"))

    timeline_template = "#+TITLE: TimeLine\n#+setupfile: setup.setup\n"
    print("INFO 构建时间轴 timeline.org")
    content_timeline = [i[2:] for i in list_to_str(timeline).splitlines()]
    for i in range(2020, 2030):
        ind = 0
        has = False
        for ind,l in enumerate(content_timeline):
            if f"[{i}-" in l:
                has = True
                break
        if not has:
            continue
        content_timeline.insert(ind, f"* {i}")
    content_timeline = timeline_template + "\n".join(content_timeline)
    Path("timeline.org").write_text(content_timeline, encoding="utf8")
    update_file(Path("timeline.org"))

    update_file(Path("about.org"))
    update_file(Path("404.org"))

def main():
    """主函数"""
    if ARGS and ARGS.add:
        p1 = Path(orgreader2.pytools.sys.argv[0]).parent/"setup.setup"
        p2 = Path(ARGS.add)
        if p2.exists():
            print(f"文件或目录'{p2}'已存在")
            return
        setupf = orgreader2.pytools.calculate_relative(p1, p2)
        t = "#+TITLE: \n"
        t += f"#+DATE: <{orgreader2._get_strtime(s=False)}>\n"
        t += f"#+SETUPFILE: {setupf}\n\n请输入文本\n"
        p2.write_text(t, encoding="utf8")
        print(f"已创建文件'{p2}'")
        return

    timeline = []
    tree = []
    for i in sorted(Path("post").iterdir()):
        fordir(i, tree, timeline)
    timeline = sorted(timeline, key=lambda x:x[0], reverse=True)

    if ARGS and not ARGS.no_build_home:
        build_homepage(tree, timeline)

if __name__ == "__main__":
    parser=argparse.ArgumentParser(description="构建博客用脚本")
    parser.add_argument("-n", "--no-update", action="store_true", help="不输出文件")
    parser.add_argument("-a", "--add",type=str, help="模板建立一个指定的org文件")
    parser.add_argument("-I", "--ignore-time", action="store_true", help="忽略时间")
    parser.add_argument("-N", "--no-build-home", action="store_true", help="不构建主页")
    ARGS = parser.parse_args()
    main()
