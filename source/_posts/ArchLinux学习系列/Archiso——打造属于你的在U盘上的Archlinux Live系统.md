---
title: "Archiso——打造属于你的在U盘上的Archlinux Live系统"
tags: 
  - archlinux
  - linux
categories: linux
layout: post
date:   2022-08-12 04:04:29 +0800
---

## Archiso是什么？

这里引用arch wiki的描述：

> [Archiso](https://gitlab.archlinux.org/archlinux/archiso) 是一个高度可定制的工具，用于构建 Arch Linux live CD/USB ISO 映像。[官方映像](https://archlinux.org/download/) 是用 Archiso 构建的。它可以用作救援系统、linux 安装程序或其他系统的基础。

### Archiso能够做什么？

　　archiso用于制作装有archlinux的iso镜像文件，可以使用dd工具将其烧录进U盘，可以在作系统出问题时开展紧急补救工作（例如重新安装grub引导、重新安装linux内核、直接修改root密码等）。  
　　若是只用于补救系统，archlinux官方的镜像文件就够用了，但是我还想要更多，希望能够在U盘上安装一个能临时办公的系统。  

### 一开始的探索

　　一开始我尝试直接在系统上安装软件，但是我发现它的文件实际存储在内存上，没有办法存储在U盘内，而且烧录好的U盘变成了只读文件系统，没有办法存储文件甚至不能调整分区。  
　　我若尝试在U盘上安装系统时，文件大小轻松超过我的U盘大小，根本没有可能。并且U盘的读写速度非常的慢，就算是shell启动都要等很久。  
　　于是我决定要学习使用archiso定制一个属于自己的iso系统镜像。

## 真正的开始

### 基本的准备

　　首先你需要安装 archiso 或 archiso-git 包获取基本的制作工具及配置文件。在安装好软件后，你的 `/usr/share/archiso/configs` 目录下应该会有两个文件夹，分别为： **releng** 和 **baseline** 。它们的介绍如下：

> - releng用于创建正式的每月安装ISO。它可以作为创建自定义ISO映像的起点。  
> - baseline是一种最低限度的配置，它只包括从介质启动 Live 环境所需的最低限度的软件包。

　　将以上两种配置中的任意一个复制到一个可读写目录下，并自己为其命名。例如：

```shell
# cp -r /usr/share/archiso/configs/releng/ archlive
```

> 　　注意：本篇文章中的所有演示命令均在root权限下执行，如果是普通用户则需要使用sudo等程序提权后操作。如：
> 
> ```shell
> $ sudo cp -r /usr/share/archiso/configs/releng/ archlive
> ```
> 
`

　　其中，*archlive* 为复制出的目录名字。为了方便讲解，你可以在终端使用以下命令定义一个变量，将其作为路径的开头，以代替绝对路径，防止出现错误。其中， *archlive* 为变量名，而其值为当前工作目录的绝对路径。

```shell
# cd archlive
# archlive=`pwd`
```

### 自定义

#### 软件包

　　要设置镜像中安装的软件包，需要编辑 *\$archlive/packages.x86_64* 文件。每行为一个软件包名。需要移除包时删除该行，添加包时添加包名到新的一行即可。  
　　若是需要添加AUR的软件包，可以先下载软件的 *PAGBUILD* 文件到本地并使用 `makepkg` 工具将其构建成软件包（文件名格式一般为 `packages-name-version-arch.pkg.tar.zst` ）。将所有要安装的软件包放置在同一个可读文件下，使用 `repo-add` **新建一个本地仓库**（Arch Wiki: [en](https://wiki.archlinux.org/title/Pacman/Tips_and_tricks#Custom_local_repository) [中文](https://wiki.archlinux.org/title/Pacman_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)/Tips_and_tricks_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)#%E8%87%AA%E5%BB%BA%E6%9C%AC%E5%9C%B0%E4%BB%93%E5%BA%93)）并将软件包信息放入。并添加如下信息到 *$archlive/pacman.conf* 文件中：

```conf
[customrepo]
SigLevel = Optional TrustAll
Server = file:///path/to/customrepo
```

> 　　注意：要将示范中的 *customrepo* 替换为你创建的仓库名称（不是文件名），*Server* 后面的路径要提换为仓库文件所在的路径（不包括文件名）。  
> 　　注意：一般情况下要将 *SigLevel* 后的值改为 `Never` 不对仓库进行签名认证，可以省去很多工作。  
> 　　注意（引自arch wiki）：pacman.conf 中的顺序很重要。要为您的自定义存储库提供最高优先级，请将其置于其他存储库条目之上。

> `repo-add` 的帮助信息如下：
> 
> ```text
> repo-add (pacman) 6.0.2
> 
> 用法：repo-add [选项]  <path-to-db> <package> ...
> 
> repo-add 会通过读取某个软件包来更新软件包数据库。
> 可以在命令行中添加多个指定的软件包。
> 
> 选项：
>   -n, --new 只增加数据库中没有的包
>   -R, --remove 在更新数据库之后，删除旧的软件包文件
>   -p, --prevent-downgrade  阻止降级，如果数据库中已有一个更高的版本的软件包存在
>   --nocolor 关闭颜色输出
>   -q, --quiet       最小化输出信息
>   -s, --sign        更新后使用 GnuPG 签名数据库
>   -k, --key <密钥>   使用指定的密钥签名该数据库
>   -v, --verify      更新前验证数据库签名
> 
> 更多可用选项的描述及细节请参见 repo-add(8)。
> 
> 示例：repo-add /path/to/repo.db.tar.gz pacman-3.0.0-1-i686.pkg.tar.gz
> ```
>
`

#### 向镜像内添加文件

　　如果需要向镜像内添加文件，则需要在 *\$archlive/airootfs/* 目录下添加。其中，该文件夹将作为Live系统的 **根目录** （/）的起点，  
　　如果需要为特定的文件、文件夹设置权限或者所有权，请修改 *\$archlive/profiledef.sh* 脚本。

> 　　注意（引自arch wiki）：  
> 　　默认情况下，[权限](https://wiki.archlinux.org/title/File_permissions_and_attributes)将是 `644` （对于文件）和 `755`（对于目录）。所有这些都将归根用户所有。要为特定文件和/或文件夹设置不同的权限或所有权，请使用 `profiledef.sh` 中的 `file_permissions` 关联列表。有关详细信息，请参阅 [README.profile.rst](https://gitlab.archlinux.org/archlinux/archiso/-/blob/master/docs/README.profile.rst)。

#### 修改内核

　　倘若我们不配置gui界面直接使用终端，那么没有中文的影响是致命的（Linux的tty不支持输出中文）。为了使用中文，我们可以使用打过 `cjktty` 补丁的内核。但是出于知识受限，我不会自定义内核。好在 `archlinuxcn/linux-lily` 已经将补丁打入内核了（尽管它的更新速度有点慢），我们只需要在 *\$archlive/packages.x86_64* 中添加软件包名，在 *\$archlive/pacman.conf* 中添加以下内容开启 `archlinuxcn` 仓库，并且修改启动引导即可。

```conf
[archlinuxcn]
Server = https://mirrors.tuna.tsinghua.edu.cn/archlinuxcn/$arch
```

　　但是实际上我也并不清楚该如何更改启动引导，只会更改 *\$archlive/grub/grub.cfg* 文件。在文件中找到 `# Menu entries` 一行，并在下面添加上：

```cfg
menuentry "Arch Linux安装镜像(x86_64, UEFI)(内核linux-lily支持中文)" --class arch --class gnu-linux --class gnu --class os --id 'archlinux-lily' {
    set gfxpayload=keep
    search --no-floppy --set=root --label %ARCHISO_LABEL%
    linux /%INSTALL_DIR%/boot/x86_64/vmlinuz-linux-lily archisobasedir=%INSTALL_DIR% archisolabel=%ARCHISO_LABEL%
    initrd /%INSTALL_DIR%/boot/intel-ucode.img /%INSTALL_DIR%/boot/amd-ucode.img /%INSTALL_DIR%/boot/x86_64/initramfs-linux-lily.img
}
```

### 构建ISO映像

　　在配置好后就应该开始构建镜像了。你可以通过下列命令开始构建镜像文件：

```shell
# mkarchiso -v -w $archlive/../work -o $archlive/../ $archlive/
```

　　这里再引用arch wiki的描述：

> `-w` 指定工作目录。如果未指定该选项，则默认为当前目录中的 `work`。  
> `-o` 指定将放置构建的 ISO 映像的目录。如果未指定该选项，则默认为当前目录中的 `out`。  
> 需要注意的是配置文件 `profiledef.sh` 在运行 mkarchiso 时不能指定，只能指定文件的路径。

　　在这里我再作一些补充：

- `-w` 指定的是输出临时文件的目录。在构建的过程中会产生的文件、要安装的软件包都将会放置在此，空间占用也会非常巨大。
- `-o` 指定的是生成出的iso文件的保存目录，它会自动为ISO文件命名（但是会覆盖同名文件）。
- 最后一个选项是配置文件所在的目录

### 其他设置

　　如果你需要动态调整根目录的大小，你可以尝试使用以下命令：

```shell
# mount -o remount,size=2G /run/archiso/cowspace
```

　　其中的`size`后的值为根分区（交换空间）的目标大小。如果你想，你可以使用它弄出一个1024PB大小的根目录（实际上是假的）。
