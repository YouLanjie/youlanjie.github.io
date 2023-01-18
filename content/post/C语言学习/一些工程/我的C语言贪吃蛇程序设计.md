---
title: "我的纯C语言贪吃蛇程序"
date:   2022-07-20 22:56:29 +0800
draft: true
---

我的cgame3项目（非C++）

<!--more-->

# 我的C语言贪吃蛇程序设计

我的程序托管在[github上](https://github.com/youlanjie/cgame3)，想要查看源代码的可以在上面查看。倘若无法进入，也可以在[gitee上](https://gitee.com/youlanjie/cgame3)查看。再不行也可以在[gitlab上](https://gitlab.com/youanjie/cgame3)查看

本文章侧重于游戏过程的实现，其他的内容基本不讲

## 程序构思

- 主界面功能：打印菜单接受输入并进行判断选择，启用对应的功能
- 游戏功能：接受输入，同时更新游戏数据并打印
- 历史记录：无需要
- 游戏帮助：打印所有的游戏帮助
- 清除记录：无需要

## 程序实现

程序的菜单借助于*include/tools.c*文件实现，该文件内容理应与windows系统是兼容的，但本程序不兼容windows。其Menu函数可以实现打印菜单、让用户可视化地选择选项、分页显示、返回选择结果功能。如果有需要请自取（还有，声明文件是*include/include.h*）

基于贪吃蛇长度不限的特点，为了保存蛇的信息，选择结构体链表的形式保存：
定义一个结构体保存数据：
```c
struct Snake {
	short x;    /* 保存蛇身的横坐标（自左向右） */
	short y;    /* 保存蛇身的纵坐标 */
	struct Snake * pNext;    /* 保存指向的下一个节点 */
}
```
声明启动游戏的函数：
```c
void Game();

```

<++>




















