---
type: post
title: Linux & Windows 小技巧（5）
date: 2023-09-14 0:00
updated: 2023-09-14 0:00
categories: 开发与代码
tags:
  - C
  - 现代编程语言
---

**文章内容：Edge、Chrome和Firefox的展台模式；Scoop的使用方法**

## Microsoft Edge 展台模式

在 [《小技巧（3）》](https://orig.zhouweitong.site/2023/09/14/linux-windows-tricks-03/#Windows-%E5%B1%95%E5%8F%B0%E6%A8%A1%E5%BC%8F) 中，我以 Microsoft Edge 为例简单描述了 Windows 操作系统级展台模式功能的设置方法。

对于操作系统级的“展台模式”，常用于以下场景：

- 商场电子展柜、企业宣传展板等；
- 数据看板大屏、监控系统大屏、比赛实况大屏等；
- 图书馆、办事处、机场等的公用电脑；

以上场景具有的共同特点是：需要应用保持全屏；限制用户只使用这个应用或访问特定网页；提供一定交互能力。

在绝大多数情况下，被展示的内容都可以用网页的形式（播放幻灯片、播放视频等也可以用网页实现）呈现。这种场景下，OS级展台模式功能的配置流程复杂、维护困难、可能导致操作系统不稳定等问题就显得有些大材小用了。

如果只是想临时启动 Edge 的展台模式，或是在运行 Edge 的同时运行其他程序，再或者是在 Linux 或 macOS 下启动展台模式，最简便的办法是直接使用命令行。

### 启动命令

Edge 是基于 Chromium 二次开发的浏览器。因此，与 Chromium 启动展台模式的命令类似。以百度为例启动展台模式：

```powershell
.\chrome.exe --kiosk 'https://www.baidu.com'
```

定位到 msedge.exe 所在路径，一般为：

```text
C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe
```

在该路径下启动 PowerShell，启动展台模式：

```powershell
.\msedge.exe --kiosk 'https://www.baidu.com' --edge-kiosk-type=fullscreen
```

