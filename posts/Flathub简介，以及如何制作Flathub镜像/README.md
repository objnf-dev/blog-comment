---
type: post
title: Flathub简介，以及如何制作Flathub镜像
date: 2023-09-16 0:00
updated: 2023-09-16 0:00
categories: 自由探索
tags:
  - Flatpak
  - Flathub
  - Linux
---

## 什么是Flathub？

- Flathub之于Flatpak，正如Snapcraft之于Snap
  - 类似于“官方Repo”，但是由社区维护
  - 与AUR不同，Flathub存储了软件的二进制文件，而不只是构建文件
  - Flathub有着自己的大型CI集群[Flathub Buildbot](https://buildbot.flathub.org/#/)
- 安装发行版上的Flatpak时，不一定默认启用Flathub，需要手动查看和添加

## 启用Flathub

- 查看已经启用的源

```bash
flatpak remotes
```

- 如果没有`flathub`源，就需要手动添加
- 添加Flathub源

```bash
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
```

- 随后就可以安装Flathub中的软件包了

<!--more-->

## 搭建Flathub镜像

- Flatpak Repo的本质就是一个OSTree Repo，Flathub也不例外
- Flathub的OSTree Repo地址可从flatpakrepo文件中找到：`https://dl.flathub.org/repo/`
- 使用该地址可以进行部分镜像或全量镜像

### 编外：RSYNC同步全量镜像

- OSTree Repo实际上支持使用`rsync`同步大型Repo，但需要分发Repo的服务器支持SSH或RSYNC协议
  - 目前Flathub仍未开放SSH/RSYNC支持，并且倾向于不使用`rsync`而使用`ostree`；见[[Feature Request] use rsync to host flatpak repository · Issue #4383 · flatpak/flatpak](https://github.com/flatpak/flatpak/issues/4383)
- 可以使用第三方脚本`rsync-repos`，脚本的代码见[ostree-releng-scripts/rsync-repos at master · ostreedev/ostree-releng-scripts](https://github.com/ostreedev/ostree-releng-scripts/blob/master/rsync-repos)

操作流程：

- 安装`rsync`
- 下载脚本
- 创建文件夹
- 运行`rsync-repos`脚本

```bash
# 安装rsync
sudo dnf install rsync
# 下载脚本
wget https://raw.githubusercontent.com/ostreedev/ostree-releng-scripts/master/rsync-repos
# 同步到哪里？
mkdir repo/
# 使用rsync-repos进行同步
python3 ./rsync-repos --src rsync://abc.com/ --dst ./repo/ 
```

### OSTree同步镜像

- 可以自己选择同步哪些软件包（以及哪些架构和版本），也可以自行对软件包的历史进行控制
- 需要的存储空间和同步时间不定，全量镜像可能需要3TB以上存储空间
- 直接使用`ostree`，需要编写脚本

操作流程：

- 安装`ostree`和`flatpak`
- 创建本地的OSTree Repo
- 给本地的OSTree Repo添加Flathub的Remote
- 添加并信任Flathub的GPGKey
- 编写脚本，选择Ref进行同步
- 删除无用的OSTree Repo Commit历史
- 生成新的OSTree Summary和Flatpak Repo Summary

```bash
# 安装ostree
sudo dnf install flatpak ostree
# 创建并初始化本地的OSTree Repo
mkdir repo
# collection-id必须设置为org.flathub.Stable，否则ref位置会变化
ostree init --repo=./repo --mode=archive --collection-id=org.flathub.Stable
# 添加Remote
ostree remote add --repo=./repo flathub https://dl.flathub.org/repo/
# 添加并信任Flathub的GPGKey
# 给当前系统的Flatpak添加Flathub源
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
# Flatpak会把Flathub的GPGKey放到特定位置，使用gpg导入并信任
gpg --import /var/lib/flatpak/repo/flathub.trustedkeys.gpg
echo -e "4\ny\n" | gpg --command-fd 0 --expert --edit-key flathub@flathub.org trust
# 把GPGKey导入到OSTree Repo中
ostree --repo=./repo remote gpg-import -k /var/lib/flatpak/repo/flathub.trustedkeys.gpg flathub
```

然后编写同步脚本并运行，脚本示例如下：

```bash
# Repo位置
REPO="./repo"

declare -a FLATHUB_REFS
declare -a PATTERNS
declare -A SYNC_LIST

# 软件包名
# 运行时
PATTERNS+=( \
    "runtime/org.gnome.Sdk" \
    "runtime/org.gnome.Platform" \
    "runtime/org.kde.Platform" \
    "runtime/org.kde.Sdk" \
    "runtime/org.kde.Platform" \
    "runtime/org.freedesktop.Platform" \
    "runtime/org.freedesktop.Sdk" \
    "runtime/io.elementary.Platform" \
    "runtime/io.elementary.Sdk" \
);
# 元数据
PATTERNS+=( \
    "appstream/" \
    "appstream2/" \
);
# Extensions
PATTERNS+=( \
    "org.blender.Blender.Codecs" \
);
# Apps
PATTERNS+=( \
    "org.blender.Blender" \
    "com.usebottles.bottles" \
    "com.github.tchx84.Flatseal" \
    "com.moonlight_stream.Moonlight" \
    "com.obsproject.Studio" \
    "io.typora.Typora" \
    "org.kde.krita" \
    "org.winehq.Wine" \
    "org.electronjs.Electron2.BaseApp" \
);

# 过滤函数
filter_list() {
    local SYNC_LIST_TMP+=( $(printf "%s\n" "${FLATHUB_REFS[@]}" | grep $1) );
    for item in "${SYNC_LIST_TMP[@]}"
    do
        SYNC_LIST[$item]=1;
    done
}

# 入口点
main() {
    # 获得当前Flathub Ref列表
    FLATHUB_REFS+=( $(ostree remote refs --repo=${REPO} flathub) );
    
    # 找出需要同步的软件包的完整包名
    for pat in "${PATTERNS[@]}"
    do
        filter_list $pat;
    done
    
    # 进行同步
    for item in "${!SYNC_LIST[@]}"
    do
        echo "Syncing: ${item}";
        ostree --repo=$REPO pull --mirror $item;
    done
}

main;
```

脚本运行完毕后：

```bash
# 若硬盘空间不大，也可尝试清除一段时间以前的Commit历史以节约空间；以7天为例
ostree --repo=./repo prune --keep-younger-than="7 day ago"
# 生成Summary
ostree summary --repo=./repo --update
flatpak build-update-repo ./repo
```

### 使Flathub镜像对外服务

- 使用Caddy自动配置HTTPS，并分发Flatpak Repo的文件：

```
abc.com

root * /home/abc/repo
file_server
```

- 随后编写`.flatpakrepo`文件，例如：

```text
[Flatpak Repo]
Title=Flathub Mirror
Url=https://abc.com/
Homepage=https://abc.com/
Comment=Flathub Mirror
Description=Flathub Mirror
Icon=
```

- 可以将`.flatpakrepo`文件保存在本地，也可保存在Flathub Mirror Repo下面，如：`https://abc.com/repo.flatpakrepo`
- 在需要使用Flathub镜像的Linux主机上，使用如下命令配置Flatpak：

```bash
flatpak remote-add --no-gpg-verify flathub-mirror https://abc.com/repo.flatpakrepo
```

- 随后即可使用Flathub Mirror。此时可以删除Flathub官方源。

也可以对Flathub Mirror进行GPG签名，可以参照[flatpak build-update-repo命令文档](https://docs.flatpak.org/en/latest/flatpak-command-reference.html#flatpak-build-update-repo)中的`--gpg-sign`和`--gpg-homedir`参数，并在`.flatpakrepo`文件中加入GPG字段。