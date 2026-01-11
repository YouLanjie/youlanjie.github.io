#!/usr/bin/env python
"""构建博客用脚本"""

import argparse
import re
import time
import subprocess
from pathlib import Path

try:
    from lib.python import orgreader2
    from lib.python import pytools
except ModuleNotFoundError as e:
    print("[ERROR] lib.python.orgreader2.py 不可用")
    print("[ERROR] 尝试：git submodule init")
    print("[ERROR] 尝试：git submodule update")
    raise e

class EmacsBacken:
    """Emacs服务"""
    def __init__(self) -> None:
        self.avaliable = False
        ret = subprocess.run("type emacs", capture_output=True, shell=True, check=False)
        if ret.returncode == 0:
            self.avaliable = True
        self.started = False
    def _exec(self, cmd, capture_output = True):
        if not self.avaliable:
            return None
        ret= subprocess.run(cmd, capture_output=capture_output, check=False)
        if ret.returncode != 0:
            print(f"[Code:{ret.returncode}] Cmd:{cmd}")
            if ret.stderr:
                print("\033[31m"+ret.stderr.decode("utf-8")+"\033[0m")
        return ret
    def start(self, loop=False):
        """启动进程"""
        ret = self._exec(["emacs", "--bg-daemon", "ORG_TO_HTML_SERVER", "-Q"])
        if ret and ret.returncode == 0:
            self.started = True
            print("Emacs Deamond had running")
        elif ret and ret.returncode == 1:
            self.started = True
            self.stop()
            if not loop:
                self.start(True)
        else:
            print("[INFO] Emacs Deamond start FAILD")
            return
        ret = self._exec(["emacsclient", "-e", """(progn (require 'package) (package-initialize)
(setq-default make-backup-files nil auto-save-default nil)
(setq-default org-src-fontify-natively t org-export-with-sub-superscripts '{} org-use-sub-superscripts '{})
(require 'monokai-theme) (load-theme 'monokai t) (require 'htmlize))"""])
    def stop(self):
        """退出emacs"""
        if self.started:
            self._exec(["emacsclient", "-e", "(kill-emacs)"])
            self.started = False
    def update_file(self, filename):
        """更新文件（自动过滤css）"""
        if not self.started:
            self.start()
        filename = str(filename)
        ret = self._exec(["emacsclient", "-e",
        f"""(progn (find-file "{filename}")(org-mode)(org-html-export-to-html)(kill-buffer-and-window)())"""])
        if ret and ret.returncode != 0:
            return
        file = Path(filename)
        if not file.is_file():
            return
        content = file.read_text(encoding="utf8").splitlines()
        i = 0
        flag = False
        while i < len(content):
            if content[i].startswith('<style type="text/css">'):
                flag = True
            if content[i].startswith('</style>'):
                del content[i]
                break
            if flag:
                del content[i]
            i += 1
        file.write_text("\n".join(content), encoding="utf8")

ARGS = None
project_dir = Path(pytools.sys.argv[0]).parent
formatter = orgreader2.HtmlExportVisitor()
emacs = EmacsBacken()

def update_file(file:Path) -> tuple[str,str,str,str]:
    """更新文件"""
    if not file.is_file():
        pytools.print_err(f"[WARN] '{file}' 不是文件")
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
            pytools.print_err(f"[ERROR] '{file}' 既不是utf8也不是gbk编码")
            return ("", str(outputf), f"[ERROR]{file}", "既不是utf8也不是gbk编码")

    content = content.splitlines()
    if not is_newer and len(content) > ((ARGS and ARGS.limit) or 100):
        content = content[:((ARGS and ARGS.limit) or 100)]    # 偷偷摸摸限制长度提高读取速度(实际上是在偷懒)
    if ARGS and ARGS.verbose:
        print(f"[INFO] 正在处理文件 '{file}'")

    if ARGS and ARGS.no_build_home and ARGS.emacs:
        ret =  ("", str(outputf), str(outputf), "[NONUPDATE]")
        doc = None
    else:
        doc = orgreader2.Document(
                content, str(file),
                setting={"progress":(ARGS and ARGS.verbose and ARGS.progress)})
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
        link = str(pytools.calculate_relative(outputf, project_dir))
        ret = (date, link, " ".join(doc.meta["title"]) if
               doc.meta["title"] else file.stem,
               " ".join(doc.meta["description"]))

    if outputf.is_dir():
        print(f"ERROR 输出文件名被文件夹占用 - {outputf}")
        return ret
    if is_newer and ARGS:
        if not ARGS.no_update:
            print(f"INFO 输出文件 - {outputf}")
            if doc:
                outputf.write_text(doc.accept(formatter), encoding="utf8")
            else:
                emacs.update_file(file)
        elif ARGS.touch and outputf.is_file():
            print(f"INFO 更新文件时间 - {outputf}")
            outputf.touch()
    return ret

BLACKLIST = {"post/Novel/SAO/",
             "post/Novel/无职/",
             "post/Novel/春物/",
             "post/Novel/败犬女主/"}
WHITELIST = {"post/Novel/SAO/index.html",
             "post/Novel/无职/index.html",
             "post/Novel/春物/index.html",
             "post/Novel/败犬女主/index.html"}

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
#+setupfile: ./setup.setup
* Welcome
欢迎来到我的个人博客。\\
点击 [[./timeline.html][*/TimeLine/*]] 查看按时间排序的文章列表界面。
在大部分页面点击右上角 [[#][*/UP/*]] 按钮可以回到网页头部。
/Table of Contents/ 是目录，鼠标悬浮或者屏幕点击展开。\\
如遇代码块中英文对不齐的情况可尝试双击代码块。
若屏幕右侧存在脚注栏可尝试双击展开（全屏）或收回。\\
关于页面在[[./about.html][*/这里/*]]
* 我的文章（按目录结构排列）
"""
    print("INFO 构建首页 index.org")
    content_index = index_template+re.sub(r"^\- ", "** ", list_to_str(tree,True), flags=re.M)
    outf_index = project_dir/"index.org"
    outf_index.write_text(content_index, encoding="utf8")
    update_file(outf_index)

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
    outf_timeline = project_dir/"timeline.org"
    outf_timeline.write_text(content_timeline, encoding="utf8")
    update_file(outf_timeline)

def main():
    """主函数"""
    if not (project_dir/".git").exists():
        print("[ERROR] 本构建程序似乎没有被放置到正确的位置")
        return
    if ARGS and ARGS.add:
        p1 = project_dir/"setup.setup"
        p2 = Path(ARGS.add)
        if p2.exists():
            print(f"文件或目录'{p2}'已存在")
            return
        setupf = pytools.calculate_relative(p1, p2)
        t = "#+TITLE: \n"
        t += "#+DESCRIPTION: \n"
        t += f"#+DATE: <{pytools.get_strtime(s=False)}>\n"
        t += f"#+SETUPFILE: {setupf}\n\n请输入文本\n"
        p2.write_text(t, encoding="utf8")
        print(f"已创建文件'{p2}'")
        return

    timeline = []
    tree = []
    for i in sorted((project_dir/"post").iterdir()):
        fordir(i, tree, timeline)
    timeline = sorted(timeline, key=lambda x:x[0], reverse=True)

    if ARGS and not ARGS.no_build_home:
        build_homepage(tree, timeline)
    update_file(project_dir/"about.org")
    update_file(project_dir/"404.org")

def run_server():
    """运行服务器"""
    import socketserver
    import http.server
    import webbrowser
    port = 8080
    for i in range(port, port+100):
        try:
            with socketserver.TCPServer(("", i), http.server.SimpleHTTPRequestHandler) as httpd:
                print(f"[INFO] 服务器(WebUI)运行在 http://localhost:{i}/")
                print("[INFO] 浏览器或将自动打开")
                try:
                    webbrowser.open(f"http://localhost:{i}/")
                except ModuleNotFoundError:
                    print("[INFO] 无法自动打开浏览器")
                # print("按 Ctrl+C 停止服务器")
                try:
                    httpd.serve_forever()
                except KeyboardInterrupt:
                    print("\n[INFO] 服务器已停止")
        except OSError:
            continue
        break

if __name__ == "__main__":
    parser=argparse.ArgumentParser(description="构建博客用脚本")
    parser.add_argument("-n", "--no-update", action="store_true", help="不输出文件")
    parser.add_argument("-a", "--add",type=str, help="模板建立一个指定的org文件")
    parser.add_argument("-I", "--ignore-time", action="store_true", help="忽略时间")
    parser.add_argument("-N", "--no-build-home", action="store_true", help="不构建主页")
    parser.add_argument("-t", "--touch", action="store_true", help="仅更新文件修改时间")
    parser.add_argument("-l", "--limit", type=int, default=300, help="对大文件的简略读取行数")
    parser.add_argument("-r", "--run", action="store_true", help="构建后运行http.server")
    parser.add_argument("-v", "--verbose", action="store_true", help="显示更详细的输出")
    parser.add_argument("-p", "--progress", action="store_true", help="显示进度条")
    parser.add_argument("-w", "--watch", default=0.0, nargs="?", const=5.0, type=float,
                        help="自动循环运行相同命令")
    parser.add_argument("-e", "--emacs", action="store_true", help="Run Emacs as outputor")
    ARGS = parser.parse_args()
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("Stoppping...")
    if ARGS.watch > 1:
        print("[Watching...]")
    while ARGS.watch > 1:
        try:
            time.sleep(ARGS.watch)
            main()
        except (EOFError, KeyboardInterrupt):
            print("[Quit Watching]")
            break
    emacs.stop()
    if ARGS.run:
        run_server()
