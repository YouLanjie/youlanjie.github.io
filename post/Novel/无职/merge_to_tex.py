#!/usr/bin/env python
# Created:2025.12.07
# pandoc required

from string import Template
from pathlib import Path
import time
import datetime
import subprocess
import json
import argparse
import tempfile
import os
import re

class Template2(Template):
    """自定义模板类(变量名可含'.')"""
    delimiter = "#$"
    braceidpattern = "(?a:[._a-z][._a-z0-9]*)"

def get_strtime(dt:datetime.datetime = datetime.datetime.now(), h=True,m=True,s=True) -> str:
    """获取标准时间格式"""
    t = dt.strftime("%Y-%m-%d ")
    t += "一二三四五六日"[dt.weekday()]
    l = [i[1] for i in ((h,"%H"),(m,"%M"),(s,"%S")) if i[0]]
    t += dt.strftime(" "+":".join(l) if l else "")
    return t

def merge_dict(old:dict, new:dict):
    """将new词典的内容依照old的结构和类型合并"""
    for k in new:
        if ".*" in old:
            old[k] = old[".*"]
        if k not in old:
            continue
        if type(old[k]) != type(new[k]):
            continue
        if isinstance(old[k], dict):
            merge_dict(old[k], new[k])
            continue
        old[k] = new[k]
    if ".*" in old:
        old.pop(".*")

def squash_dict(data:dict, prefix="") -> dict:
    """将分级词典以'.'为分割字符合并为同级词典"""
    new = {}
    if prefix:
        prefix+="."
    for k in data:
        if isinstance(data[k], dict):
            new.update(squash_dict(data[k], prefix=f"{prefix}{k}"))
            continue
        new[f"{prefix}{k}"] = data[k]
    return new

class Config:
    """配置类"""
    cfg_temerate = {
            "title":"",
            "author":"",
            "setting":{
                "gen_info":True,
                "mktitle":False,
                "mktoc":True,
                "ruler":False,    # 尺子，测试用
                "papersize":"a4paper",
                "fontsize":4,
                "fontname":"DengXian Light",
                "border":{
                    "left":0.7,
                    "right":0.7,
                    "top":0.5,
                    "bottom":0.9,  # 由于页码在该边距之外,所以要大点
                    "bindingoffset":.9,
                    "footskip":6.5, # pt
                    },
                "cols":9,
                "toc_cols":5,
                },
            "filelist":{
                ".*":{
                    "ignore":[],
                    "add":[]
                    }
                },
            "output":"output_#${title}_#${setting.papersize}_#${setting.fontsize}px_#${template.gtst}.tex",
            }
    pandoc_template = r"""% 生成于: #${template.generate_time}
\documentclass{article}
% 页边距需要考虑打印机实际情况
\usepackage[
	#${setting.papersize},
	left=#${setting.border.left}cm,
	right=#${setting.border.right}cm,
	top=#${setting.border.top}cm,
	bottom=#${setting.border.bottom}cm,
	footskip=#${setting.border.footskip}pt,  % 页码到正文的间距
	bindingoffset=#${setting.border.bindingoffset}cm,
	twoside,
]{geometry}
% \usepackage{footmisc}
% \usepackage{dblfnote}
\usepackage{fontspec}
\usepackage[hidelinks]{hyperref}
\usepackage{multicol}
\usepackage[UTF8]{ctex}
\usepackage{xcolor}
\usepackage{titling}   % 保留title等变量
\usepackage{fancyhdr}  % 自定义脚注
\usepackage{titlesec}  % 控制标题格式
\usepackage{enumitem}  % 控制列表格式
\usepackage{tcolorbox} % 自定义quote环境格式用
\usepackage{listings}  % 自定义src环境格式用#${template.ruler}

% 多栏设置
\setlength{\columnsep}{6mm}

% 缩小最大段落间距防止翻页时因为标题过度自动拉伸浪费空间
% 如果固定为0会导致每页底部无法对齐很难看
\setlength{\parskip}{0ex plus 0.00001ex}

% 脚注设置
\setlength{\footnotesep}{0.5\footnotesep} % 减少脚注之间的间距
\setlength{\skip\footins}{0.5\skip\footins} % 减少脚注与正文的间距
\renewcommand{\footnote}[1]{{【脚注：#1】}} % 替换原生脚注

% 需要装有windows自带的 "等线 light" 字体,
% 4pt字体对于600dpi激光打印机足够了
\setmainfont{#${setting.fontname}}
\newcommand{\setsmallf}{\fontsize{#${setting.fontsize}}{0.1}\selectfont\CJKfontspec{#${setting.fontname}}}

% 使用 titlesec 重新定义标题格式，保持目录功能
\titleformat{\section}
  {\fontsize{#${setting.fontsize.section}}{0.1}\selectfont\bfseries}
  {【\arabic{section}.】}
  {0pt}
  {}
\titleformat{\subsection}
  {\fontsize{#${setting.fontsize.subsection}}{0.1}\selectfont\bfseries}
  {【\arabic{section}.\arabic{subsection}.】}
  {0pt}
  {}
\titleformat{\subsubsection}
  {\fontsize{#${setting.fontsize.subsubsection}}{0.1}\selectfont\bfseries}
  {【\arabic{section}.\arabic{subsection}.\arabic{subsubsection}.】}
  {0pt}
  {}
% 移除标题间距
\titlespacing*{\section}{0pt}{0pt}{0pt}
\titlespacing*{\subsection}{0pt}{0pt}{0pt}
\titlespacing*{\subsubsection}{0pt}{0pt}{0pt}

% 页脚设置
\pagestyle{fancy}
\fancyfoot[C]{\setsmallf\thepage}
\fancyfoot[RO]{\setsmallf【\thetitle】|【\leftmark】}
\fancyfoot[LE]{\setsmallf【\thetitle】|【\leftmark】}
\fancyfoot[LO]{\setsmallf【\thedate】}
\fancyfoot[RE]{\setsmallf【\thedate】}

% 设置列表的间距
\setlist{noitemsep,leftmargin=1em,labelsep=0.1em,topsep=0.1em,partopsep=0.1em}

% 自定义quote环境
\tcbuselibrary{skins,breakable}
% 定义新环境：左侧有竖线，整体左缩进1em，段首缩进2em
\renewtcolorbox{quote}[1][]{
	breakable,
	enhanced,
	frame hidden,
	colback=white,
	left=1em,
	right=0pt,
	top=0pt,
	bottom=0pt,
	sharp corners,
	before skip=0.5\baselineskip,
	after skip=0.5\baselineskip,
	overlay={
		\draw[line width=0.6pt, black](frame.north west) -- (frame.south west);
	},
	parbox=false,
	#1
}
% 设置环境内段落缩进
\usepackage{etoolbox}
\AtBeginEnvironment{quote}{\setlength{\parindent}{2em}}

% 自定义src环境
\lstset{
    breaklines=true,
    breakatwhitespace=false,     % 允许在任意位置换行
    breakindent=2em,            % 换行缩进
    prebreak=\mbox{\textcolor{red}{$\hookleftarrow$}\space},
    postbreak=\mbox{\space\textcolor{red}{$\hookrightarrow$}},
    numbers=left,      % 行号位置
    numbersep=0.5em,   % 行号距左侧宽度
    xleftmargin=1em,   % 左侧整体偏移
    %numberstyle=\tiny\color{gray},
    %basicstyle=\ttfamily\small,
}

% 文档信息
\hypersetup{
  pdftitle={#${title}},
  pdfauthor={#${author}},
  hidelinks,
  pdfcreator={LaTeX via pandoc(and a python script)}}
\title{#${title}}
\author{#${author}}
\date{#${template.generate_time}}

% pandoc的奇怪东西
\providecommand{\tightlist}{}

\begin{document}
% 分栏、字体设置
\setsmallf
#${template.mktitle}
#${template.mktoc}
\begin{multicols}{#${setting.cols}}

#${template.gen_info}

$body$

\end{multicols}
\end{document}
"""
    pandoc_template_toc = r"""\begin{multicols}{#${setting.toc_cols}}
\tableofcontents
\end{multicols}
"""
    pandoc_template_info = "\n\n\\noindent\n".join(r"""\section{页面设置}
生成于:#${template.generate_time}
纸张类型：#${setting.papersize}
上下左右边距：#${setting.border.top}cm ,#${setting.border.bottom}cm ,#${setting.border.left}cm ,#${setting.border.right}cm,
footskip：#${setting.border.footskip}pt,
装订偏移：#${setting.border.bindingoffset}cm,
字体大小(h1,h2,h3,正文)：#${setting.fontsize.section}pt, #${setting.fontsize.subsection}pt ,#${setting.fontsize.subsubsection}pt ,#${setting.fontsize}pt
字词统计：#${counter.words}k,
LINES:#${counter.lines}""".splitlines())
    pandoc_template_fgruler = r"""
\usepackage[type=alledges]{fgruler}
\fgrulerdefuser{
    \ifnum\value{page}<3\relax
        \fgrulertype{\fgrulerunit}{alledges}
    \fi
}
"""
    def __init__(self, cfg_f:Path):
        self.cfg_f = cfg_f
        self.cfg = self.cfg_temerate
        cfg = {}
        if cfg_f.is_file():
            try:
                cfg = json.loads(cfg_f.read_bytes())
            except json.JSONDecodeError as e:
                print(e)
        if not isinstance(cfg, dict):
            print(f"Err type: {type(cfg)}")
            cfg = {}
        merge_dict(self.cfg, cfg)
    def print_config_template(self):
        print(json.dumps(self.cfg_temerate, ensure_ascii=False, indent='\t'))
    def generate_org_file(self) -> str:
        filelist = set()
        home = self.cfg_f.parent
        for inp_dir in self.cfg["filelist"]:
            print(f"[INFO] searching '{home/inp_dir}'")
            fl = set((home/inp_dir).glob("**/*.org"))
            bl = {home/inp_dir/i for i in self.cfg["filelist"][inp_dir]["ignore"]}
            wl = {home/inp_dir/i for i in self.cfg["filelist"][inp_dir]["add"]}
            filelist |= {i.resolve() for i in ((fl-bl)|wl)}
        filelist = sorted(filelist)
        content = []
        for i in filelist:
            content += ["", f"【FILE:{i.name}】",""]
            content += i.read_text(encoding="utf-8").splitlines()
        content = "\n".join(content)
        content = re.sub(r"^\s*#\+title:(.*)", r"\n【TITLE:\1】\n",content, flags=re.I+re.M)
        content = re.sub(r"^\s*#\+author:(.*)", r"\n【AUTHOR:\1】\n",content, flags=re.I+re.M)
        content = re.sub(r"^\s*#\+date:(.*)", r"\n【DATE:\1】\n",content, flags=re.I+re.M)
        # content = re.sub(r"^\s*#\+begin_(.*)", "\n【BEGIN:\\1】\n", content, flags=re.I+re.M)
        # content = re.sub(r"^\s*#\+end_(.*)", "\n【END:\\1】\n", content, flags=re.I+re.M)
        content = f"""#+title: {self.cfg["title"]}
#+author: {self.cfg["author"]}
#+date: {get_strtime()}

""" + content
        return content
    def generate_template_dict(self, content:str = "") -> dict:
        """生成用于模板的词典"""
        k : dict[str, str|int|float] = {
                "template.gtst": time.strftime("%Y%m%d_%H%M%S"),
                "template.generate_time": get_strtime(),
                }
        k.update(squash_dict(self.cfg))
        k["setting.fontsize.section"] = float(k["setting.fontsize"]) + 2
        k["setting.fontsize.subsection"] = float(k["setting.fontsize"]) + 1
        k["setting.fontsize.subsubsection"] = k["setting.fontsize"]
        if content:
            content = "\n".join(i for i in content.splitlines() if i)
        k["counter.words"] = (len(content)-len(content.splitlines()))/1000
        k["counter.lines"] = len(content.splitlines())
        k["template.mktitle"] = r"\maketitle{}" if k["setting.mktitle"] else ""
        k["template.mktoc"] = Template2(self.pandoc_template_toc).safe_substitute(k) if k["setting.mktoc"] else ""
        k["template.ruler"] = self.pandoc_template_fgruler if k["setting.ruler"] else ""
        k["template.gen_info"] = Template2(self.pandoc_template_info).safe_substitute(k) if k["setting.gen_info"] else ""
        return k
    def generate_pandoc_template(self, content:str = "") -> str:
        # print(s)
        # __import__('pprint').pprint({k1:k[k1] for k1 in set(k) - set(t.get_identifiers())})
        # __import__('pprint').pprint({k1:k[k1] for k1 in set(t.get_identifiers()) & set(k)})
        # __import__('pprint').pprint(set(t.get_identifiers()) - set(k))
        return Template2(self.pandoc_template).safe_substitute(self.generate_template_dict(content))

def main():
    ARGS = parse_arg()
    config = Config(ARGS.config)
    if ARGS.print_config:
        config.print_config_template()
        return
    if ARGS.print_pandoc_template:
        print(config.generate_pandoc_template())
        return
    print("[INFO] Config:")
    __import__('pprint').pprint(config.cfg)
    content = config.generate_org_file()
    temp_dict = config.generate_template_dict(content)
    pandoc_template = Template2(config.pandoc_template).safe_substitute(temp_dict)
    outputf = config.cfg_f.parent/Template2(config.cfg["output"]).safe_substitute(temp_dict)

    if ARGS.no_to_tex:
        outputf = Path(outputf.stem+".org")
        print(f"[INFO] 保存org文件到:{outputf}")
        outputf.write_text(content, encoding="utf-8")
        return
    org_f = tempfile.mkstemp(prefix=f"output_org_file.{time.strftime("%Y%m%d_%H%M%S")}.",
                             suffix=".org")
    os.write(org_f[0], content.encode("utf-8"))
    os.close(org_f[0])

    template = tempfile.mkstemp(prefix=f"pandoc_template.{time.strftime("%Y%m%d_%H%M%S")}.",
                                suffix=".tex")
    os.write(template[0], pandoc_template.encode("utf-8"))
    os.close(template[0])

    cmd = ["pandoc", org_f[1],"--template",template[1],"-o",outputf]
    print(f"[INFO] RUN: {cmd}")
    try:
        subprocess.run(cmd, check=True)
        print(f"[INFO] 输出文件为'{outputf}'")
    except KeyboardInterrupt:
        print("[INFO] 转换取消，临时文件未删除")
        return
    except FileNotFoundError:
        print("[WARN] pandoc不存在, 转换取消，临时文件未删除")
        return
    except subprocess.CalledProcessError:
        print("[WARN] pandoc报错, 转换取消，临时文件未删除")
        return
    Path(org_f[1]).unlink()
    Path(template[1]).unlink()

def parse_arg() -> argparse.Namespace:
    parser=argparse.ArgumentParser(description="合并org文件并利用pandoc生成缩印用的tex文件")
    parser.add_argument("-c", "--config", type=Path, default=Path("config.json"),
                        help="配置文件")
    parser.add_argument("-n", "--no-to-tex", action="store_true", help="输出.org文件")
    parser.add_argument("-P", "--print-config", action="store_true", help="打印配置文件模板")
    parser.add_argument("-D", "--print-pandoc-template", action="store_true", help="打印pandoc模板")
    return parser.parse_args()

if __name__ == "__main__":
    main()

