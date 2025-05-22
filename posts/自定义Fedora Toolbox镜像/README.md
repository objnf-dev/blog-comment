---
type: page
title: 自定义Fedora Toolbox镜像
date: 2023-09-14 0:00
updated: 2023-09-14 0:00
categories: 自由探索
tags:
  - 容器
  - Linux
---

[Toolbox](https://github.com/containers/toolbox) 可看做是Podman的Wrapper，力求将容器与主机的操作系统（Host OS）无缝集成。与Toolbox类似的工具还有Distrobox。它们在牺牲一些容器安全性（端口控制、资源控制、文件的独立性等）的情况下可以做到：

- 用户穿透：在容器中使用与当前Host user一样的user与home目录；
- 设备穿透：直接使用Host的`/dev`、`/media`等；
- 网络穿透：直接使用Host网络，获得与主机一致的网络体验；
- 服务穿透：通过直接使用Host的`/run/user/<uid>`和`/tmp`以及关键服务的Socket，实现在容器中访问主机的显示服务（X11/Wayland）、网络服务（Avahi）、D-Bus、systemd journal等；

因此，Toolbox可以用来：

- **作为不可变系统的软件安装方式之一。**如Fedora Silverblue、Fedora CoreOS等不可变系统中均预装Toolbox，另一些不可变系统中可能预装Distrobox；
- 使用其他发行版的镜像，**在当前发行版中无缝运行针对其他发行版制作的程序**。如在Fedora下运行只提供Ubuntu deb包的GUI程序；
- 在没有Host的root权限时**创造一个假root环境**。如非privileged的Toolbox容器同样可以使用`sudo dnf install`安装软件；
  - 需要镜像中预装sudo，并支持`sudo`、`wheel`组获取root权限，且支持`NOPASSWD`选项；
- 使用不同版本的镜像实现**“旧程序运行在新系统上”或“新程序运行在旧系统上”**，或对程序进行兼容性测试；
- 可以通过对镜像进行自定义，实现**快速且一致的开发环境搭建**；

<!--more-->

## 创建自己的Toolbox镜像

符合OCI标准的容器镜像均可被Toolbox使用。换言之，依照通常的Docker镜像构建方法就可以构建自己的Toolbox镜像。

Fedora社区持续维护着Fedora的Toolbox镜像构建文件 [container/fedora-toolbox](https://src.fedoraproject.org/container/fedora-toolbox)，GitHub上也有社区维护的各主流发行版的Toolbox镜像 [toolbx-images/images](https://github.com/toolbx-images/images)。

以Fedora的Toolbox镜像为例，以下是官方给出的Dockerfile示例：

```
# 使用fedora:37，而不是fedora-toolbox:37
FROM registry.fedoraproject.org/fedora:37

# 镜像标签
ENV NAME=fedora-toolbox VERSION=37
LABEL com.github.containers.toolbox="true" \
      com.redhat.component="$NAME" \
      name="$NAME" \
      version="$VERSION" \
      usage="This image is meant to be used with the toolbox command" \
      summary="Base image for creating Fedora toolbox containers" \
      maintainer="Debarshi Ray <rishi@fedoraproject.org>"
 
COPY README.md /

# 使dnf安装软件包时 同步安装所有语言的语言文件 及文档文件
RUN rm /etc/rpm/macros.image-language-conf
RUN sed -i '/tsflags=nodocs/d' /etc/dnf/dnf.conf

# [A] 安装完整的 核心工具（GNU Coreutils）及其语言文件
RUN dnf -y upgrade
RUN dnf -y swap coreutils-single coreutils-full
RUN dnf -y swap glibc-minimal-langpack glibc-all-langpacks

# [B] 通过重装的方式补齐语言和文档
COPY missing-docs /
RUN dnf -y reinstall $(<missing-docs)
RUN rm /missing-docs

# [C] 安装额外的软件包
COPY extra-packages /
RUN dnf -y install $(<extra-packages)
RUN rm /extra-packages

# [D] 保证关键文档文件存在
COPY ensure-files /
RUN ret_val=0; \
  while read file; do \
    if ! compgen -G "$file" >/dev/null; then \
      echo "$file: No such file or directory" >&2; \
      ret_val=1; \
      break; \
    fi; \
  done <ensure-files; \
  if [ "$ret_val" -ne 0 ]; then \
    false; \
  fi
RUN rm /ensure-files

RUN dnf clean all
```

同时还需要三个额外的文件 `ensure-files`、`extra-packages`和`missing-docs`。

想增加或删减Toolbox中的镜像，可直接修改`extra-packages`文件，修改时尽量保证每行只有一个软件包的包名。也可以仿照上述Dockerfile的`[C]`节，在不修改`extra-packages`文件时使用自定义文件；

仿写：

```
COPY added-packages /
RUN dnf -y install $(<added-packages)
RUN rm /added-packages
```

`added-packages`例子：

```text
nodejs
npm
python3-pip
gcc
g++
```

### 给Toolbox镜像增加中文支持

可以通过修改`LANG`变量、重新生成语言文件、安装中文字体等方法使Toolbox内的命令行/GUI程序支持并默认显示中文。

1. 添加语言文件：在上述Dockerfile示例的`[B]`节前添加如下内容

```
# 中文语言
RUN dnf install -y  glibc-locale-source glibc-langpack-zh langpacks-zh_CN
RUN localedef -c -i zh_CN -f UTF-8 zh_CN.UTF-8
```

2. 安装字体和输入法：在上述Dockerfile示例的`[C]`节或`[D]`节前添加如下内容

```
# 安装字体和输入法
RUN dnf install -y wqy-microhei-fonts wqy-zenhei-fonts fcitx5
```

3. 设置`LANG`环境变量：在上述Dockerfile示例的最后添加如下内容

```
# 设置环境变量
ENV LANG zh_CN.UTF-8
```

## 使用Toolbox镜像

以自定义镜像的tag为`a.com/fedora-toolbox-customized:37`为例：

1. 通过`podman`拉取自定义镜像

```bash
podman pull a.com/fedora-toolbox-customized:37
```

2. 使用`toolbox`创建容器

```bash
# 容器名可以随意指定
# 当主机为Fedora系统，且容器名为 fedora-toolbox-<主机Fedora版本号> 时，该容器为Toolbox默认容器
toolbox create --image a.com/fedora-toolbox-customized:37 fedora-toolbox-37
```

3. 进入容器环境或执行容器内特定程序

```bash
# 当主机只有一个Toolbox容器时，会直接进入该容器
# 当Fedora系统的主机有默认容器时，会直接进入默认容器
toolbox enter
# 可以直接指定需要运行的命令
toolbox run <命令>
# 在存在多个Toolbox容器时，可通过命令参数指定运行哪个容器
toolbox enter <容器名>
toolbox run --container <容器名> <命令>
```

## 删除Toolbox容器和镜像

```bash
# 需要退出所有正在使用Toolbox Shell/命令行程序/GUI程序的窗口
# 停止容器
podman stop <容器名>
# 删除容器
toolbox rm <容器名>
# 删除镜像
podman rmi a.com/fedora-toolbox-customized:37
```
