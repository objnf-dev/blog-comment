---
type: page
title: 准备工作与K8s部署
date: 2024-01-07 0:00
updated: 2024-01-07 0:00
---

## 准备工作

- Linux操作系统 
  - Ubuntu、Debian、CentOS、Fedora、RHEL、openSUSE/SLES 等主流Linux发行版
  - Fedora CoreOS、VMware Photon OS等“容器专用”OS
- 足够的RAM和存储：物理机部署时推荐只运行K8s相关程序
- Internet连接，或能够访问特定registry（需要提前搭好registry并在registry中添加K8s组件镜像）
- 物理机之间的网络联通（Worker访问Control的API、Worker与Worker之间的网络甚至存储共享）
- 安装好部署工具 见下文
- 安装好CRI-O标准兼容的容器工具，docker、podman、containerd等均可 
  - podman：绝对开源，无服务（无daemon），很适用于Rootless Container模式（低权限），仅支持Linux容器
  - docker：最主流，有商业版，传统daemon模式（需要root/管理员权限），支持Linux容器和Windows容器
  - containerd：最基础，绝对开源，最标准，是K8s、K3s等默认的CRI-O容器工具，支持Linux容器和Windows容器
- 可以使用带GUI的容器工具 
  - Podman Desktop
  - Docker Desktop
  - Rancher Desktop