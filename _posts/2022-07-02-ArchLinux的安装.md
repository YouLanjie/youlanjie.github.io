# ArchLinux的安装

## 写在前边

本blog用于记录我安装ArchLinux的方法，专业教程请查阅[官方Wiki](https://wiki.archlinux.org/title/Installation_guide_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87))

## 安装前的准备 -- 从U盘安装

1. 从[官网](https://archlinux.org/download/)上下载ArchLinux的安装镜像(下滑找到 **China** 分栏有国内镜像服务器源，速度会快很多，推荐清华云与mirrors.tuna.tsinghua.edu.cn阿里云aliyun.com)

2. windows下则使用任意一款U盘拷录软件（自行百度）拷录镜像文件到U盘（注意，被拷录的U盘的所有数据都会丢失，请备份好资料后再执行操作）。
而Linux下则可以（使用root权限）使用命令
```bash
dd if=你的镜像文件名称 of=/dev/sdX bs=512    #sdX为要拷录的U盘设备，实际中应为sda或sdb...
```
拷录镜像文件到U盘上（Linux的磁盘管理机制请自行百度）

3. （除非你能够同时查看教程才这么做，否则建议先记下下面的安装过程较好）重启电脑，更改启动顺序或（一般情况下）按下F12选择启动项，进入Arch的安装镜像系统。倘若系统出现 *FALT* 报错请自行搜索解决

## 安装过程


### 确认引导类型
首先我们需要确认你的电脑是 **EFI引导+GPT分区表** 还是 **BIOS(LEGACY)引导+MBR分区表** 的引导方式。请在终端中执行命令：
```bash
ls /sys/firmware/efi/efivars
```
倘若屏幕提示 **No such file or directory** 则你的电脑是BIOS引导，反则是EFI引导

其实如果在开机时留意一下弹出过的菜单界面就能知道你的是什么引导方式。BIOS引导的长这样：

![BIOS](https://youlanjie.github.io/img/in-post/2022-07-02_02/2022-07-02_02-02.jpg)

而EFI的长这样：

![EFI](https://youlanjie.github.io/img/in-post/2022-07-02_02/2022-07-02_02-01.jpg)

### 联网

有线网络的联网教程请自行百度，这里主要讲无线网络的连接。

无线网络联网，你可以使用 `wifi-menu` 工具联网，而我个人更倾向于使用 `iwd` 工具进行联网。在终端输入
```bash
iwctl
```
打开iwd的设置界面,一下为一些常用命令列表：

|命令|作用|
|:-:|:-:|
|device list|列出可用的网络设备|
|station 设备名称 scan|启用指定的设备|
|station 设备名称 get-networks|获取网络列表|
|station 设备名称 connet 网络名称|连接指定的网络，有密码的会要求输入密码，连接成功后网络列表前会出现 **>** 号|
|exit|退出|
|quit|退出|

最后使用
```bash
ping www.baidu.com
```
判断能否正常上网（使用Ctrl-C退出）

### 软件包

> 这里需要你会使用编辑器Vim

执行命令以编辑文件 */etc/pacman.d/mirrorlist*
```bash
vim /etc/pacman.d/mirrorlist
```

> 提示：输入路径时可以使用Tab补全

按下 **/** 并输入 **China** 回车，跳转到中国源列表。
在列表上方一列输入 `dgg` 删除列表上面的内容，在列表下方一列输入 `dG` 移除列表以下内容，建议将清华、阿里云的源以 `dd` 删除一行，再 `p` 粘贴的操作放在文件最前面几列，最后输入 `:w` 保存 `:q` 退出。例如：

```conf
## China
Server = https://mirrors.tuna.tsinghua.edu.cn/archlinux/$repo/os/$arch
Server = https://mirrors.aliyun.com/archlinux/$repo/os/$arch
Server = http://mirrors.tuna.tsinghua.edu.cn/archlinux/$repo/os/$arch
Server = http://mirrors.aliyun.com/archlinux/$repo/os/$arch
Server = http://mirrors.163.com/archlinux/$repo/os/$arch
```

> 其实可以直接运行命令
```bash
reflector -c China -a 10 --sort rate --save /etc/pacman.d/mirrorlist
```
依照速度进行自动排序，根本不用管

> 编辑 */etc/pacman.conf* 找到 `#ParallelDownloads = 5` 项，把前面的 **#** 号移除可以实现同时下载多个文件，后面的5是最大的同时下载数量

> 在 */etc/pacman.conf* 文件末尾加入
```conf
[archlinuxcn]
Server = https://mirrors.tuna.tsinghua.edu.cn/archlinuxcn/$arch
```
可以启用 **archlinuxcn** 源，里面有一些国内的常用软件的Linux版本

### 更新系统时间

执行
```bash
timedatectl set-ntp true
```

> 正常情况下是没有输出的

### 为系统分区

> 注意！这个步骤要格外小心，命令回车前要确认命令无误，且要知道自己在做什么，重要的硬盘数据应提前备份好，避免带来数据的丢失

执行命令
```bash
fdisk -l
```
查看目前的分区情况

空白的情况下：

![虚拟机——空白](https://youlanjie.github.io/img/in-post/2022-07-02_02/2022-07-02_02-03.jpg)

#### 硬盘分区

##### 使用fdisk

使用命令开始为硬盘分区
```bash
fdisk /dev/sdX   #sdX为目标硬盘，实际中应为sda或sdb...
```

关于fdisk的命令教程:

- m 查看命令作用
- g 使用GTP分区表
- p 打印分区表（若p命令后中Disklable type:后为dos则为MBR分区表，gpt则为gpt分区表）
- n 新建分区
  - MBR分区表
    1. 确认分区类型
      - p 主分区（最多四个，编号1~4）
      - e 扩展分区（占用主分区数量，最多一个，有了则不显示，编号同主分区）
      - l 逻辑分区（不限量，前提是得有一个扩展分区，无则不显示，最大大小为扩展分区大小，即包容在扩展分区内，编号5~?）
  - GPT分区表
    1. 无需确认分区类型，无分区类型之分
  - 共同步骤
    2. 确认分区编号
    3. 分区起始扇区（一般不管）
    4. 分区结束扇区（+单位 表示多大， -单位 表示剩余多大空间）
- d 移除分区，输入编号即可
- t 更改指定分区的分区类型（作用）
- w 保存退出
- q 不保存直接退出

[也可以参考官方wiki](https://wiki.archlinux.org/title/Fdisk_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87))

![fdisk](https://youlanjie.github.io/img/in-port/2022-07-02_02/2022-07-02_02-04.jpg)

##### 使用cfdisk

cfdisk有着伪图形界面，对萌新更友好。

刚进入cfdisk时如果硬盘没有分区表会询问你。上下方向键移动，回车选择。BIOS选择dos，EFI选择gpt就好。具体的操作就不细讲了。

![cfdisk](https://youlanjie.github.io/img/in-port/2022-07-02_02/2022-07-02_02-05.jpg)

##### 文件系统

使用
```bash
mkfs.filesystemtype /dev/sdXn    #filesystemtype为对应的文件系统类型（ext3,ext4,vfat...），sdXn为硬盘上的第n个分区，n为分区编号
```

格式化分区，对应的看下面 **分区建议** 表格

##### 挂载分区

使用mount,格式：
```bash
mount /dev/sdXn /dir
```
> sdXn为硬盘分区，/dir 为挂载目标目录，详见下表，但是在挂载硬盘时时不能直接按照下表挂载，/根目录一般挂载在USB系统的 */mnt* 目录下，其他的磁盘挂载点跟着变化就行了，但一定要先挂载根目录再依文件夹的关系一个个挂载，没有的文件夹使用 `mkdir -p` 创建就好（例如：/boot/efi -> /mnt/boot/efi)

#### 分区建议

- BIOS

|分区|大小|类型|文件系统|挂载点|作用|
|:-:|:-:|:-:|:-:|:-:|:-:|
|BOOT|200~500M|Linux / BIOS BOOT|ext4|/boot|作为启动分区|
|/|>=20G(建议，不是太低也行)|Linux|ext4|/|作为根目录|
|*home||Linux|ext4|/home|作为用户家目录，利于数据保护、重装系统，可分可不分|
|*SWAP||Linux Swap|||可选，用作交换分区，可当替补的内存理解|

- EFI引导

|分区|大小|类型|文件系统|挂载点|作用|
|:-:|:-:|:-:|:-:|:-:|:-:|
|EFI|100~500M|EFI System|vfat|/boot/efi|作为启动分区|
|/|>=20G(建议，不是太低也行)|Linux|ext4|/|作为根目录|
|*BOOT|200~500M|Linux / BIOS BOOT|ext4|/boot|可选|
|*home||Linux|ext4|/home|作为用户家目录，利于数据保护、重装系统，可分可不分|
|*SWAP||Linux Swap|||可选，用作交换分区，可当替补的内存理解|

### 安装系统

在硬盘全部挂载后，我们就可以开始安装系统了

安装基本系统：
```bash
pacstrap -i /mnt/ base base-devel linux linux-firmware
```

> 命令中的 */mnt/* 要替换成你所挂载根目录分区的目录名，忘记了可以使用 `df -h` 或者 `lsblk` 查看

> 你还可以在安装完基本系统后安装额外的软件方便使用，使用
```bash
passtrap -i /mnt/ 软件包
```
安装软件包。建议装上 **dhcpcd**（DNS服务） **iwd**（联网） **vim** （文件编辑） **fish** （一种shell，默认就有强大的自动补全配置）

> 倘若在前面的软件包设置里启用了archlinuxcn源，其实你可以额外安装内核软件包 **linux-lily** 在tty界面它原装支持显示中文

配置分区表：
```bash
genfstab -U /mnt/ >> /mnt/etc/fstab
```

> 这里的 */mnt/* 同理。-U 为使用UUID标识的意思

进入新安装的系统：
```bash
arch-chroot /mnt/ /bin/bash
```

> 若前面你安装了 **fish** 就可以使用命令
```bash
arch-chroot /mnt/ /bin/fish
```
进入新的系统

#### 本地化

设置中文:
```bash
vim /etc/locale.gen
```

输入 **/** 搜索zh_CN.UTF-8与en_US.UTF-8,分别去除前面的 **#** 号，并将其放到文件头部。如下：
```conf
zh_CN.UTF-8 UTF-8
zh_CN.GBK GBK
en_US.UTF-8 UTF-8
......
```

并执行
```bash
locale-gen
```

以及
```bash
echo "LANG=zh_CN.UTF-8" >> /etc/locale.conf
export LANG=zh_CN.UTF-8
```

设置时区为上海：
```bash
ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
```

> 意义不明的命令：
```bash
hwclock --systohc --utc
```

#### 安装GRUB引导

执行
```bash
pacman -S grub efibootmgr os-prober
```

安装引导：

##### BIOS

```bash
grub-install --targer=i386-pc /dev/sdXn
```

> /dev/sdXn为硬盘上的第n个分区，也是你的BOOT分区（挂载到 */boot/*）

##### EFI

```bash
grub-install
```

（更新）配置:
```bash
grub-mkconfig -o /boot/grub/grub.cfg
```

> 如果使用多系统，可以编辑 */etc/default/grub* ，找到 **GRUB_DISABLE_OS_PROBER** 并将后面的 **"true"** 改为 **"false"** 并重新执行更新配命令

#### 用户

为root用户设置密码（否则无法登录）：
```bash
paswwd root
```
> **root** 可以省略

创建用户：
```bash
useradd -m USERNAME -s /bin/SHELL
```
> **USERNAME** 为你的用户名,SHELL为你想用的shell名称，默认为bash，可以省略

添加组/启用sudo：
```bash
usermod USERNAME -aG sudo
```

> 将用户添加进 **sudo** 组

为新用户创建密码（否则无法登录）：
```bash
passwd USERNAME
```

#### 最后的配置

启用dhcpcd服务（未安装的使用 ```pacman -S dhcpcd``` 安装）：
```bash
systemctl enable dhcpcd
```

> 同理，可以启用iwd服务，启用后普通用户也可以使用iwctl了（未开启时必须使用root

sudo启用sudo组内用户的支持：
```bash
vim /etc/sudoers
```

找到 `%sudo ALL=(ALL:ALL) ALL` ，移除 **#** 号取消注释， `:w!` 强制保存后退出

退出重启：
```bash
exit
reboot
```

### 扩展——配置系统

#### 使用图形界面

> 以下操作均在root权限下执行，请自行 `su root` 或者在命令前加上 `sudo `

安装最基本的X服务
```bash
pacman -S xorg
```

输入法
```bash
pacman -S fcitx fcitx-configtool
echo -e "GTK_IM_MODULE    DEFAULT=fcitx\nQT_IM_MODULE     DEFAULT=fcitx\nXMODIFIERS       DEFAULT=\@im=fcitx" >> ~/.pam_environment
```

- gnome
```bash
pacman -S alacarte gnome networkmanager
systemctl enable gdm
```

> gdm为gnome的图形界面登录系统

- xfce
```bash
pacman -S xfce
systemctl enable xfce
```

- kde
```bash
pacman -S plassma konsole dolphin sddm
pacman -S kdeconnet ark
systemctl enable sddm
```

- i3-wm
```bash
pacman -S i3-gaps i3blocks i3lock i3status
```

> i3-wm只是一个窗口管理器而已，并非桌面系统，需要安装其他软件。我个人习惯安装kde的软件并在i3wm下使用。即
```bash
pacman -S i3-gaps i3blocks i3lock i3status sddm kdeconnet konsole dolphin ark qt5c picom polybar feh rofi
```

> qt5c用于设置在i3-wm下kde程序的主题,配置：
```bash
echo "QT_QPA_PLATFORMTHEME DEFAULT=qt5ct" >> ~/.pam_environment
```
picom用于美化窗口界面。polybar用于替代i3status。feh用于使用壁纸。rofi用于启动应用

#### 中文字体

```bash
pacamn -S ttf-liberation wqy-zenhei ttf-fira-code ttf-fira-mono ttf-nerd-fonts-symbols-mono
```

#### 使用AUR

使用AUR助手yay:
```bash
git clone https://aur.archlinux.org/yay-bin.git
cd yay-bin
makepkg -si
```

使用AUR安装软件:
```bash
yay -S google-chrome picom-jonaburg-git bat siji-git ttf-unifont autotiling netease-cloud-music utools
```

> **netease-cloud-music** 与 **utools** 实际上已经被包含在archlinuxcn库里了

|软件包名|软件作用|
|:-:|:-:|
|google-chrome|浏览器|
|picom-jonaburg-git|picom合成器的分支，支持动画|
|bat|文本查看器|
|siji-git/ttf-unifont|字体|
|autotiling|自通垂直/横向排列窗口|
|netease-cloud-music|网易云音乐|
|utools|强大的工具箱|
