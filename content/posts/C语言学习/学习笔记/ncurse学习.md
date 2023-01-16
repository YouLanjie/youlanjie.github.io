---
title: ncurse学习
tags: ["linux" , "c语言"]
categories: ["开发"]
draft: true
date: 2022-09-03
---

记录我学习ncurse的过程
<!--more-->

> 声明：这篇博客主要记录我个人学习ncurses库的理解，可能会有不严谨的地方。

## 介绍

在这里我引用一段话：

> [ncurses](http://www.gnu.org/software/ncurses/ncurses.html)(new curses)是一套编程库，它提供了一系列的函数以便使用者调用它们去生成基于文本的用户界面。
> ncurses名字中的n意味着“new”，因为它是curses的自由软件版本。由于AT&T“臭名昭著”的版权政策，人们不得不在后来用ncurses去代替它。
> ncurses是[GNU计划](https://en.wikipedia.org/wiki/GNU_Project%20GNU%E8%AE%A1%E5%88%92)的一部分，但它却是少数几个不使用GNU GPL或LGPL授权的GNU软件之一。

ncurses库能够让开发者自由地在终端指定位置打印指定的字符，并且提供了接受鼠标、键盘功能键输入的功能。许多有名的控制台软件就用到了ncurses库，例如 `vim` `emacs` 等。

## 安装

> 由于我使用的是Arch，所以我并不清楚在Ubuntu下的安装方式。据我所知，windows下还没有ncurses库

在ArchLinux下使用以下命令安装：

```shell
sudo pacman -S ncurses
```

## 简单使用

### 实际演示

先编写一个小程序，命名文件为 `test.c` ：

```c
#include <ncurses.h>

int main(int argc, char *argv[])
{
	initscr();
	raw();
	noecho();
	curs_set(0);

	mvprintw(LINES / 2, (COLS - 12) / 2, "Hello,world!");
	refresh();

	getch();
	endwin();

	return 0;
}
```

然后使用gcc编译并运行
```sh
gcc test.c -o test -lncurses
./test
```

如果没有出错，那么应该会看到这样的画面：

![效果](/img/2022-09-03_01/2022-09-03_01-01.png)

即一串字符打印在终端的中央位置。

### 代码分析

可以看到，这个程序并没有引用 `stdio.h` 头文件，而是只引用了 `ncurses.h` 头文件，所以屏幕上的字符并非是由`printf`打印出来的，而是使用ncurses库的`mvaddstr`函数打印出来的。

要使用ncurses“接管”屏幕输出，需要使用函数`initscr()`进行初始化，接下来是进行一些设置：

| 函数                             | 对应的功能                                                                   |
|:---------------------------------|:-----------------------------------------------------------------------------|
| `raw()`                          | 用于取消程序输入的缓冲区，使输入的字符在无需按下回车即可被程序接收。         |
| `cbreak()`                       | 该函数也可以实现同`raw`的功能                                                |
| `noecho()`                       | 设置输入不回显，即输入的字符不显示在屏幕上                                   |
| `curs_set(int)`                  | 用于设置光标的可见性。2可见，1半可见，0不可见                                |
| `mvaddstr(int y, int x, char *)` | 用于在指定的坐标添加字符串。坐标顺序为y、x                                   |
| `refresh()`                      | 将缓冲区内容打印到屏幕上，因为输出的内容并非是直接输出到屏幕而是输出到缓存内 |
| `getch()`                        | 效果等同于getchar()，但是输入不回显，无缓冲区                                |
| `endwin()`                       | 结束ncurses模式，同时可以恢复终端执行命令前的内容，结束程序前必须要执行      |

## 更多操作

### 输入

- `getch()`： 接受字符输入的函数（该函数在windows下被包含进系统了，但Linux没有）

### 输出

- `move(int, int)`： 移动光标到指定坐标（顺序(y, x)并且从0开始计算，其他移动光标的函数也一样）
  - `LINES`：一个宏，表示终端的行数，从1开始计算。所以`LINES - 1`则表示为最后一行
  - `COLS`： 另一个宏，表示终端的列数，从1开始计算。使用`COLS - 1`表示最后一列
- `printw(char *, ...)`： 像printf那样格式化输出
- `mvaddch(int, int, char)`： 在指定坐标（y, x）打印一个字符
- `mvaddstr(int, int, char *)`： 在指定坐标（y, x）打印一个字符串

#### 颜色

要使用颜色同样需要初始化，启用颜色。判断终端是否支持彩色显示：

```c
has_colors();
```

如果不支持则返回`FALSE`（一个宏），若支持则使用下面的函数启用颜色：

```c
start_color();
```

要让字体彩色显示，则需要使用函数

```c
init_pair(short)
```

<++>


