---
type: post
title: Flatpak概念及其基础使用方法
date: 2023-09-14 0:00
updated: 2023-09-14 0:00
categories: 自由探索
tags:
  - Flatpak
  - Linux
---

## 为什么使用Flatpak？

- 问题：已经有了`apt`、`dnf`等这种系统级的包管理器，为什么还要使用Flatpak？
    1. Flatpak给软件提供**相对独立的运行环境（沙箱）**，并**提供权限控制功能**，避免软件破坏或任意修改系统；
    2. Flatpak很大程度上**解决了软件的兼容性问题**，让“新系统跑旧软件”或“旧系统跑新软件”成为可能；因此Flatpak可以在非滚动更新的发行版上安装 比系统源内版本更高的软件；
    3. Flatpak支持诸多发行版，在不同的发行版上能够**获得几乎相同的软件使用体验**；
    4. Flatpak允许**同一个软件的不同版本在系统内共存**；
    5. Flatpak允许**非root用户在单用户作用域内安装软件**；
- 问题：我在用Snap或者AppImage，它们和Flatpak有什么区别嘛？
    1. Flatpak性能中等，略优于Snap，略差于AppImage；
    2. Flatpak、AppImage不需要服务（Service），而Snap需要Snapd；
    3. Flatpak、Snap提供权限控制功能，而AppImage不提供；
    4. Flatpak、Snap统一提供所有软件包的更新，而AppImage需要打包者自行适配应用内更新或利用第三方工具更新；
    5. Flatpak、Snap在发行版的预装情况方面有区别：
        - Flatpak预装在这些发行版中：
          - Fedora (Workstation/Silverblue/Kinoite)
          - Manjaro
          - Endless OS
          - Linux Mint
          - Rocky Linux (GNOME)
          - AlmaLinux (GNOME)
          - CentOS (GNOME)
          - EuroLinux (GNOME)
          - Pop!_OS
          - elementary OS
          - Clear Linux (Desktop)
          - PureOS
          - Zorin OS
          - MX Linux
          - KDE neon
          - ......
        - 而Snap预装在这些发行版中：
          - Ubuntu系列 (Ubuntu Desktop, Ubuntu Server, KUbuntu, XUbuntu......)
          - KDE neon
          - Manjaro
          - Solus
          - Zorin OS
          - ......
    6. Flatpak和Snap均得到了两个软件中心（GNOME Software Center、KDE Plasma Discover）的支持，而Appimage需要使用第三方软件中心（如[prateekmedia/appimagepool](https://github.com/prateekmedia/appimagepool)、[app-outlet/app-outlet（同样支持Flatpak）](https://github.com/app-outlet/app-outlet)）

<!--more-->

## 什么时候不用Flatpak？

- **软件与系统结合非常紧密、不适合在沙箱中运行时**不应该使用Flatpak
  - 或者说，这种情况下软件很难打包成Flatpak
  - 例如：GParted、Wireshark、Virt-Manager
  - 应当考虑系统软件包管理器（`apt`、`dnf`等）
- **需要软件的便携性时**不应该使用Flatpak
  - 应当考虑将程序打包成单个文件的AppImage
- **命令行软件**不应该使用Flatpak
  - Flatpak有计划支持命令行程序，但目前体验不佳
    - Flatpak不会自动创建软件包内程序文件的链接和别名，例如不能直接执行`go`只能执行`flatpak run --command=/usr/lib/sdk/golang/bin/go org.freedesktop.Sdk//21.08`
  - 例如：Golang，Gcc，Docker，Minikube
  - 应当考虑Snap或系统软件包管理器
- **运行内存（RAM）或存储空间（Storage）极为有限的时候**不应该使用Flatpak
  - 应当考虑系统软件包管理器；

## App和Runtime

Flatpak 分为两种软件包：

- Application（App）：应用本体；
- Runtime：应用所需的运行时；

“运行时”均是支持GUI显示的基本运行时（“没它打不开”），与桌面环境相关，一个“应用本体”只依赖一个“运行时”。

“运行时”目前主要有以下四种：

1. FreeDesktop：最基础的运行时，提供D-Bus、GTK3、X11、Wayland等
    - `org.freedesktop.Platform`
    - `org.freedesktop.Sdk`
2. GNOME：GNOME=FreeDesktop+GNOME_Specific；提供Gjs、GStreamer、GVFS等；
    - `org.gnome.Platform`
    - `org.gnome.Sdk`
3. KDE：KDE=FreeDesktop+KDE_Specific；提供Qt等；
    - `org.kde.Platform`
    - `org.kde.Sdk`
4. elementary：elementary=GNOME+elementary_Specific；提供elementaryOS专属的图标、Granite等；
    - `io.elementary.Platform`
    - `io.elementary.Sdk`

## ID

每个App或Runtime都有一个ID，类似Andorid下App的包名，例如：

- （App） Blender： `org.blender.Blender`
- （Runtime） Gnome Platform：`org.gnome.Platform`

加入架构和版本号，就构成了 ID三元组：

- `org.blender.Blender/x86_64/stable`
- `org.gnome.Platform/x86_64/43`

加入软件包类型，就构成了 该App对应的Flatpak ostree分支名：

- `app/org.blender.Blender/x86_64/stable`
- `runtime/org.gnome.Platform/x86_64/43`

## App和Extension

另一种对软件包的分类是：

- Application（App）：（主要）应用，即可直接打开或运行的应用，例如：VLC、Blender；
- Extension：应用的扩展，有多种情况：
  - 支持特定应用正常运行的其他软件或库（“没它用不了”），如：Wine、FFMpeg、Mesa；
  - 特定应用所需的程序包（“没它用不好”），如：TeX环境、Rust语言（编译器）、Go语言（编译器）；
  - 软件自身的一部分，如：Blender的语言文件；

对应第一种分类时，App和Runtime都可以有Extension。Extension有自己的ID，命名规则是在App或Runtime的包名后加上Extension名：

- App的Extension，例如：`org.blender.Blender.Codecs`

应用安装时，应用依赖的运行时和扩展也会被安装；

## 安装范围

Flatpak 有两种安装范围：

- System：系统级安装，**需要root权限**，安装的应用 系统上所有的用户均可见；
- User：用户级安装，安装的应用 仅当前用户（触发安装的用户）可见；

## 软件包的源

与其他的包管理器（系统级或Snap）一样，Flatpak也有“软件源”的概念（即“软件包源”）。

Flatpak的软件包源是一个OSTree Repo，Flatpak包按照软件包类型、ID、架构与版本存储在对应的OSTree分支中；而软件包的各种信息和描述（元数据，MetaData）则存放在特定的分支中以供软件中心调取；

每个Flatpak 的OSTree Repo就是一个文件夹；一般使用HTTPd/NGINX/Caddy做HTTP服务器分发该文件夹下的文件，而Flatpak及各软件中心使用HTTP协议访问和下载OSTree Repo内的文件。

## .flatpakref

`.flatpakref`文件描述了**单个软件包**的信息和获取方式，文件结构大致如下：

```
[Faltpak Ref]
Name=<软件包的ID>
Branch=<软件包的版本>
Title=<描述该软件包的标题（软件包名字）>
Url=<软件包所在的源的地址>
RuntimeRepo=<软件包依赖的运行时所在的源的地址>
IsRuntime=<本软件包是不是运行时>
GPGKey=<Base64编码的GPG密钥>
```

示例：

```
[Flatpak Ref]
Name=fr.free.Homebank
Branch=stable
Title=fr.free.Homebank from flathub
Url=https://dl.flathub.org/repo/
RuntimeRepo=https://dl.flathub.org/repo/flathub.flatpakrepo
IsRuntime=false
GPGKey=mQINBFlD2sABEADsiUZUO...
```

`.flatpackref`文件可直接用于安装软件包的命令中，也可直接使用软件中心打开；


## .flatpakrepo

`.flatpakrepo`文件描述了单个软件包源的信息，文件结构大致如下：

```
[Flatpak Repo]
Title=<软件包源的名字>
Url=<软件包源的地址>
Homepage=<软件包源的主页，或软件包源维护者的主页>
Comment=<软件包源的简单描述，或是软件包维护者的信息>
Description=<软件包源的描述>
Icon=<软件包源的图标>
GPGKey=<软件包源的GPGKey>
```

示例：

```
[Flatpak Repo]
Title=Flathub
Url=https://dl.flathub.org/repo/
Homepage=https://flathub.org/
Comment=Central repository of Flatpak applications
Description=Central repository of Flatpak applications
Icon=https://dl.flathub.org/repo/logo.svg
GPGKey=mQINBFlD2sABEADsiUZUO...
```

`.flatpakrepo`文件可用于`flatpak remote-add`命令添加软件源，也可以直接使用软件中心打开；

## 列出已安装的软件包

只列出App：

```bash
flatpak list
```

也可以：

```bash
flatpak list --app
```

只列出Runtime：

```bash
flatpak list --runtime
```

列出System App：

```bash
flatpak list --system
```

列出User Runtime：

```bash
flatpak list --user --runtime
```

## 卸载软件包

卸载特定软件包：

```bash
flatpak uninstall <ID>
```

**卸载所有无用（useless）的运行时和扩展（相当于 `apt-get autoremove`）**:

```bash
flatpak uninstall --unused
```

## 升级软件包

升级所有已安装软件包：

```bash
flatpak update
```

升级所有User范围内的软件包：

```bash
flatpak update --user
```

升级某个特定的软件包：

```bash
flatpak update <ID>
```

## 搜索软件包

类似`apt search`：

```bash
flatpak search <keyword>
```

关键字可以是ID内出现的字符串（与ID相关），也可能是软件包描述内出现的字符串（与描述有关）；

在某一个源内搜索软件包：

```bash
# 找带关键字的所有软件包 -> grep过滤出特定的源
flatpak search <keyword> | grep <repo_name>
# 列出特定源里的所有软件包 -> grep过滤出特定的软件包（需要keyword与ID相关）
flathub remote-ls <repo_name> | grep <keyword>
```

## 安装软件包

在不知道软件包的ID时，可以直接使用关键字，flatpak会查找所有匹配的项并询问要安装哪个：

```bash
flatpak install <keyword>
```

知道软件包的ID时，可根据ID直接安装：

```bash
flatpak install <ID>
```

知道软件包源和软件包ID时，可安装指定源内的某软件包：

```bash
flatpak install <repo_name> <ID>
```

- 控制安装软件的范围：加`--system`或`--user`
- 控制安装软件的版本（即**安装某个旧版本而不是最新版**）：使用ID三元组
  - flatpak可自动检测当前系统的架构，三元组可简写为二元组，例如：`org.blender.Blender/x86_64/stable` -> `org.blender.Blender//stable`

有些情况下，软件包所在的软件包源（Repo）系统中并没有添加（比如第三方源，或者本地源），此时若软件包提供者提供了flatpakref文件，软件包可以在不添加源的情况下安装；

```bash
flatpak install <flatpakref_url>
```

## 修复软件包

软件包的文件丢失或出错，可以联网快速修复：

```bash
flatpak repair
```

修复操作包括校验安装的所有软件包、重新下载安装文件缺失或出错的软件包、删除没被任何ostree commit引用的文件，等。

可以使用`--system`和`--user`指定修复的范围。

## 查询flatpak操作历史

会列出flatpak的拉取（pull）、部署（depoly）、卸载（uninstall）等动作的历史记录；

```bash
flatpak history
```

## 查询软件包的详细信息

需要是已安装的软件包的ID；

```bash
flatpak info <ID>
```

会给出类似下面的输出（`LANG=en-US.UTF-8`）：

```text
Blender - Free and open source 3D creation suite

          ID: org.blender.Blender
         Ref: app/org.blender.Blender/x86_64/stable
        Arch: x86_64
      Branch: stable
     Version: 3.4.1
     License: GPL-3.0
      Origin: flathub
  Collection: org.flathub.Stable
Installation: system
   Installed: 879.3?MB
     Runtime: org.freedesktop.Platform/x86_64/22.08
         Sdk: org.freedesktop.Sdk/x86_64/22.08

      Commit: 477316037ec442424b97d3d5fddc898d5908f47af6b3976ded5d070f8ed72d38
      Parent: 9bcff42b740d86faf8e64484ed5bcab9b0598c47ee0eebb604c7c52f1a9c2233
     Subject: [fix #18] enable spnav socket (e10330e0)
        Date: 2022-12-28 14:15:54 +0000
```

## 查询哪些软件包正在运行

需要以**和运行软件时相同的用户身份**进行查询（查询userA正在运行的软件包就`su userA`）；

> 类似 `docker ps`

```bash
flatpak ps
```

有时只需要软件包ID或者是只需要实例ID，可以使用参数`--columns=<column_name>`进行输出限定；`column_name`是输出列的英文名称；

```bash
# 只看实例ID列
flatpak ps --columns=instance
# 只看ID和PID两个列
flatpak ps --columns=application,pid
```

## 强制退出正在运行的软件包

与`kill`不同，不能用于发送信号，只能用于强制停止软件包运行；

> 类似 `docker stop`

```bash
flatpak kill <ID>
```

## 使用命令行运行软件包

有时需要对软件包进行这些操作：

- 查看软件包对stdout的输出（log等）；
- 给软件包增加启动参数（例如给Discord软件包增加`--proxy-server=<url>`使Discord通过代理连接服务器）；
- 修改、增加或删除软件包中的环境变量；
- 强制使软件包使用某个运行时；
- 修改软件包的入口点（使用自定义的软件包启动命令）；
- 临时赋予软件包某些权限，如允许访问某些文件系统（路径等）、允许访问特定设备（共享内存等）......

> 类似`docker run`

直接运行：

```bash
flatpak run <ID>
```

增加启动参数：

```bash
flatpak run <ID> <params>
# 例如：
flatpak run com.discordapp.Discord --proxy-server=http://127.0.0.1:7890
```

其他常用的命令参数，**参数需要放到软件包ID的前面**：

- 环境变量
  - 修改或增加：`--env=<var_name>=<var_value>`
  - 删除：`--unset-env=<var_name>`
- 入口点
  - 修改运行软件包时执行什么命令：`--command=<command>`
- 强制指定运行时（需要ID或ID三元组）
  - `--runtime=<ID>`
- 临时修改权限相关设置
  - 文件系统：`--filesystem`，`--nofilesystem`
  - 规则：`--add-policy`，`--remove-policy`
  - 设备：`--device`，`--nodevice`
  - Socket：`--socket`，`--nosocket`
  - ......
- 其他选项可参照官方文档了解

## 进入正在运行的软件包的环境

flatpak的软件包运行在相对独立的环境中（类似于容器），因此只能通过命令进入正在运行中的软件包的环境；需要正在运行中的软件包的实例ID；

> 类似`docker exec`

```bash
flatpak enter <instance_id> <command>
```

## 软件包的权限

要查看某个软件包获取了哪些权限：

```bash
flatpak permission-show <ID>
```

修改软件包的权限：不推荐直接使用命令行修改，可以使用软件包 [Flatseal](https://flathub.org/apps/details/com.github.tchx84.Flatseal)

若软件包出现权限问题，可尝试重置软件包权限解决：

```bash
flatpak permission-reset <ID>
```

## 软件包源

与直接编辑配置文件增加/删除软件源不同，软件包源是通过flatpak命令行增删和管理的；

查看当前已有的源：

```bash
# 会显示源的名称（Repo name）和源的选项（Options）
flatpak remotes
# 如果要显示源的链接、优先级等详细信息：
flatpak remotes --show-details
```

删除某个源：

```bash
flatpak remote-delete <repo_name>
```

添加某个源：软件包源的维护者会提供源的描述文件（`.flatpakrepo`），而添加源时需要这个描述文件的位置；

```bash
flatpak remote-add <repo_name> <flatpakrepo_url>
```

其他常用的命令参数

- 指定作用域：`--user`，`--system`
- 关闭GPG签名校验，测试时非常好用：`--no-gpg-verify`
- 本地导入源的GPG密钥：`--gpg-import=<gpg_file_url>`
- ......
- 其他选项可参照官方文档了解

添加源时没有使用命令行参数设置选项，可在以后使用命令行修改；

```bash
flatpak remote-modify <repo_name>
```

## 软件包源内的软件包

查看某个软件包源内包含的所有软件包：

```bash
flatpak remote-ls <repo_name>
```

查看某软件包源内某个软件包的具体信息：

```bash
flatpak remote-info <repo_name> <ID>
```
