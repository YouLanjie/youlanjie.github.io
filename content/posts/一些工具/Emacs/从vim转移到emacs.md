---
title: "从vim转移到emacs"
date: 2023-01-16T12:30:19+08:00
draft: true
---

随手记下我是怎么从一个重度Vim用户转为一位Emacs用户的

<!--more-->

<a id="orgbc3bc9e"></a>

# 开始


<a id="orgecd3801"></a>

## 原因

最开始的原因是，看到别人吹emacs的org-mode有多么厉害，功能多么强大，而vim下安装插件也只是模仿了一半而已，功能残缺。出于“试一试”的心态，我就第一次安装了Emacs


<a id="orgd727f57"></a>

## 几次失败

既然是第一次，那么在我打开的一瞬间，我就觉得那些夸emacs好的人是不是在搞诈骗，因为它的初始的默认的界面其实异常地丑，给人一种极端复古的感觉。下面是两张Emacs终端界面和图形界面的截图（非开始界面）

![img](/img/2023-01-16_01/2023-01-16_01-01.png "终端界面")

![img](/img/2023-01-16_01/2023-01-16_01-02.png "图形界面")

这种界面给我的第一印象就是： **简陋** 。

我很难理解为什么一个被夸赞成“神的编辑器”居然看起来是如此地简陋。我甚至一度怀疑那些界面好看的Emacs都是虚假的。就这么，我放弃了Emacs，回到了Vim的舒适区内。后来我又尝试过几次，都都没有坚持下去。僵持近一年后，就到了23年1月，我开始了最后一次尝试，也是唯一成功的一次。


<a id="org22612e4"></a>

## 正式开始


<a id="orgc58c89a"></a>

### 先前阶段的学习

实际上，无配置的Emacs的开始界面并非如上图所示，而是有一个开始页面。在这个页面中，我看见了个字眼: `tutor` 。它是什么意思我并不清楚，但是我知道在安装Vim后会有一个命令： `vimtutor` ，我但是就判断：这很有可能是Emacs的教程，加上在图形界面Emacs是默认开启了鼠标操作的，于是我就用鼠标打开了" *Emacstutor* "，正式开启了对Emacs的学习


<a id="orgff7cb39"></a>

### 键位问题

Emacs的这份帮助文档是中文的，这极利于我学习Emacs，而摆在所有Vim党前面的最大问题实际上是Emacs看似十分不合理的键位布局。由于没有像Vim里的“编辑模式”这种东西，所以说它的大多数快捷键都是通过“ *叠Buff* ”给叠起来的简单来说就是套娃。再通俗一点就是先按下一套快捷键，再按下另一套快捷键实现对应的功能，只有常用的快捷键不用“套娃”，如移动、复制、删除等。

但是有一个大问题，Emacs的快捷键对于Alt键和Ctrl键有着极强的依赖。对于我来说，Alt键可以很轻松地按下——只需要左手大拇指向内勾，但是Ctrl就不是省油的灯了。因为Emacs的移动就是使用C-bnpf <sup><a id="fnr.1" class="footref" href="#fn.1" role="doc-backlink">1</a></sup> 来移动的，所以说这对于小拇指的工作压力是极大的。为什么会有这种问题呢？那是因为Emacs的键位并非是按照现在的键盘设计的，所以说会有这种“逆天”的快捷键组合。

但是实际上，这个问题是有解的，解一就是让 `Caps Lock（大写锁定）` 和 `Ctrl` 两个按键调换功能，或者是直接让 `Caps Lock` 直接变成 `Ctrl` 键。但方法<sup><a id="fnr.2" class="footref" href="#fn.2" role="doc-backlink">2</a></sup>我就不在此赘述。

解二实际上现实得多，也对新手特别是Vim党特别友好——使用Evil


<a id="org4b734f1"></a>

### Evil

首先，我先下个定义： **Evil** 是一个Emacs的插件。不同于Vim，Emacs有一个内置的插件管理器和一个较为统一的插件仓库EPLA。它似乎又有一些其他的分支， `GNU MPLA` 是GNU Emacs的官方插件仓库，而 `MEPLA` 则是一个非官方插件仓库。不管怎样，我还是将全部的仓库放入了配置文件<sup><a id="fnr.3" class="footref" href="#fn.3" role="doc-backlink">3</a></sup>里
\#+BEGIN<sub>SRC</sub>: Python
print("Hello World")
\#+END<sub>SRC</sub>


<a id="orge63e2b4"></a>

# 脚注


# Footnotes

<sup><a id="fn.1" href="#fnr.1">1</a></sup> 即Ctrl-b（向左）、Ctrl-n（向下）、Ctrl-p（向上）、Ctrl-f（向左）

在Emacs中（其实这套方案大都通用）， `Key-key` 通常表示要从左到右同时按下的按键，而 `Key key` 则是先按下 `Key` 后再按下 `key` 的快捷键组合

<sup><a id="fn.2" href="#fnr.2">2</a></sup> 这里仅补充Linux如何设置按键映射。

在X环境下请参考[这篇ArchWiki学习使用setxkbmap](https://wiki.archlinux.org/title/Xorg/Keyboard_configuration#Using_setxkbmap)并参考[其中的这段文字学习查看相关选项](https://wiki.archlinux.org/title/Xorg/Keyboard_configuration#Swapping_Caps_Lock_with_Left_Control)。这里给出相关命令及其结果
\#+BEGIN<sub>SRC</sub>: Shell

$ grep -e "ctrl:\\|:ctrl" /usr/share/X11/xkb/rules/evdev.lst
  grp:ctrl<sub>select</sub>      Left Ctrl to first layout; Right Ctrl to second layout
  grp:ctrls<sub>toggle</sub>     Both Ctrls together
  grp:ctrl<sub>shift</sub><sub>toggle</sub> Ctrl+Shift
  grp:ctrl<sub>alt</sub><sub>toggle</sub>  Alt+Ctrl
  grp:ctrl<sub>space</sub><sub>toggle</sub> Ctrl+Space
  ctrl:nocaps          Caps Lock as Ctrl
  ctrl:lctrl<sub>meta</sub>      Left Ctrl as Meta
  ctrl:swapcaps        Swap Ctrl and Caps Lock
  ctrl:hyper<sub>capscontrol</sub> Caps Lock as Ctrl, Ctrl as Hyper
  ctrl:ac<sub>ctrl</sub>         To the left of "A"
  ctrl:aa<sub>ctrl</sub>         At the bottom left
  ctrl:rctrl<sub>ralt</sub>      Right Ctrl as Right Alt
  ctrl:menu<sub>rctrl</sub>      Menu as Right Ctrl
  ctrl:swap<sub>lalt</sub><sub>lctl</sub>  Swap Left Alt with Left Ctrl
  ctrl:swap<sub>lwin</sub><sub>lctl</sub>  Swap Left Win with Left Ctrl
  ctrl:swap<sub>rwin</sub><sub>rctl</sub>  Swap Right Win with Right Ctrl
  ctrl:swap<sub>lalt</sub><sub>lctl</sub><sub>lwin</sub> Left Alt as Ctrl, Left Ctrl as Win, Left Win as Left Alt
  caps:ctrl<sub>modifier</sub>   Make Caps Lock an additional Ctrl
  altwin:ctrl<sub>win</sub>      Ctrl is mapped to Win and the usual Ctrl
  altwin:ctrl<sub>rwin</sub>     Ctrl is mapped to Right Win and the usual Ctrl
  altwin:ctrl<sub>alt</sub><sub>win</sub>  Ctrl is mapped to Alt, Alt to Win
  terminate:ctrl<sub>alt</sub><sub>bksp</sub> Ctrl+Alt+Backspace

$ setxkbmap -option 'caps:ctrl<sub>modifier</sub>'

$ setxkbmap -option 'swapcaps'
\#+END<sub>SRC</sub>

若是在无图形界面环境下，请参考[这篇ArchWiki学习配置](https://wiki.archlinux.org/title/Linux_console/Keyboard_configuration)，其中[这段](https://wiki.archlinux.org/title/Linux_console/Keyboard_configuration#Other_examples)是交换按键的具体例子。这里再附上[中文版本连接](https://wiki.archlinuxcn.org/wiki/Linux_%E6%8E%A7%E5%88%B6%E5%8F%B0/%E9%94%AE%E7%9B%98%E9%85%8D%E7%BD%AE)和[片段连接](https://wiki.archlinuxcn.org/wiki/Linux_%E6%8E%A7%E5%88%B6%E5%8F%B0/%E9%94%AE%E7%9B%98%E9%85%8D%E7%BD%AE#%E5%85%B6%E4%BB%96%E4%BE%8B%E5%AD%90Other_examples)。希望能有帮助。

<sup><a id="fn.3" href="#fnr.3">3</a></sup> 我的配置文件[链接](https://github.com/youlanjie/emacs.d/)，虽然比较烂，但可以用作参考。
