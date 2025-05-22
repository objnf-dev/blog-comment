---
type: post
title: Hexo新姿势！
date: 2023-09-13 0:00
updated: 2023-09-13 0:00
categories: 自由探索
tags:
  - 工具
  - hexo
---

Hexo的插件真是个好东西！一开始部署博客的时候并没有太在意插件的问题，毕竟觉得博客主题自带的插件挺全面的，足够使用了。但是用久了总是会腻，就想着静态博客能不能整一些新操作，即使只是添加点小功能。于是就翻了翻 Hexo 的插件目录，挑了些比较有用的插件，拿出来做个总结，同时也是为了方便以后使用做的一个简单记录。

## 管理员界面

插件是`hexo-admin`，效果是一个类似CodiMD编辑页面的“管理控制台”，可以实时编辑预览Markdown文章，修改tag，从剪贴板粘贴图片到文章等操作。注意：仅用于`hexo s`状态下的博客实例。

## 文章加密

插件是`hexo-blog-encrypt`，使用前须在站点配置文件加入以下内容：

```yaml
encrypt:
    enable: true
```

随后在文章的开头部分加入`password:`字段设置密码即可。

同时，配合`abstract:`字段和`message:`字段可以设置对无密码人的提示信息。同时注意不要设置toc。

## 中英文自动空格

插件为`hexo-filter-auto-spacing`，`npm install --save`之后就可以用，无需手动设置。

<!--more-->

## 插入行内JS/CSS/图片

插件为`hexo-filter-inline-assets`。

站点设置：

```yaml
inline_assets:
    enabled: true
    limit: 100000
```

随后引入：

```html
<link rel="stylesheet" href="css/main.css?__inline=true">
<script src="myscript.js?__inline=true"></script>
```

## 插入 ASCIInema 终端短视频

插件为`hexo-filter-asciinema`，作用是允许向博客文章内插入[ASCIInema](https://asciinema.org/)平台的视频。

站点设置：

```yaml
asciinema:
    enable: true
```

随后演示机安装asciinema，`sudo apt install asciinema`，并对asciinema进行授权，`asciinema auth`。浏览器打开程序给出的链接，登入账号、查收验证邮件，即可成功启用。使用`asciinema rec`开始录制。由于该网站被墙，因此可以在录制结束后按`<Ctrl+C>`保存至本地，并在本地引用。

使用实例：

```
[@asciinema](./tmplqth0fkw-ascii.cast)
```

## 快速上标

插件为`hexo-filter-sup`，站点设置：

```yaml
sup:
    markup: '^'
```

使用实例：

```
x^2^+5=10
```

## 文本提示

插件为`hexo-tag-hint`。
使用实例：

```
大家好，这个博客用了{% hint 'Hexo' '一个静态博客框架' %}。
```

注意字符串中有单引号的时候加反斜线转义。

## H5视频

插件为`hexo-tag-html5video`。
使用实例：

```
{% html5video '100%' '250px' 'video/mp4' %}
    {% asset_path 2.5_CG_Live_01_mux.mp4 %}
{% endhtml5video %}
```

第一行三个参数必须带上，不然默认`video/webm`。

## 统一ID

插件为`hexo-uuid`，作用是给每一个页面自动生成一个UUID字段。你可以拿这个字段做些别的事情，比如将其设置为博文链接什么的。

## 二维码

插件为`hexo-tag-qrcode`。
使用实例：

```
{% qrcode "https://www.baidu.com" title:"扫扫看！" 扫我 %}
```

## 下拉抽屉

插件为`hexo-tag-details`。
使用实例：

```
{% details mode:close 怎样才能订阅你博客的更新？ %}
    订阅RSS啊！
{% enddetails %}
```

## SoundCloud

插件为`hexo-tag-soundcloud`。
使用实例：

```
{% soundcloud https://soundcloud.com/kawaii-music-192471320/ost-weathering-with-you-theme-song-grand-escape-radwimps-feattoko-miura %}
```

当然，不加链接加Track ID也是可以的。

## 脚注

插件为`hexo-footnotes`。
使用实例：

```
我真的喜欢读《三体》[^1]

[^1]: 作者为 刘慈欣。
```

支持多行注释和Markdown注释。

## PDF 文件

插件为`hexo-pdf`。
使用实例：

```
（Modeling Singing F0 With Neural Network Driven Transition-Sustain Models - By Kanru Hua）

{% pdf./Modeling-Singing-F0-With-Neural-Network-Driven-Transition-Sustain-Models.pdf %}
```

## MPlayer

插入本地MP3文件。插件为`hexo-tag-mplayer`。
使用实例：

```
{% mplayer %}
    playlist: [
        {
            name: 'm_sys_title_intro',
            artist: 'Arknights',
            src: './m_sys_title_intro.mp3'
        },
        {},
    ],
    autoplay: false,
    volume: 0.75,
    playmode: "listloop",
    big: false,
    dark: false
{% endmplayer %}
```

## 文字上标

插件是`hexo-ruby-character`，需要在Linux环境下编译npm包。

示例：`{% ruby Chocolate | Vanilla %}` ，也可方便的给汉字注音，例如：`{% ruby 鬼魅魍魉 | 鬼魅魍魉 %}`，又或者是恶搞，类似： `{% ruby 精彩节目 | 前方高能 %}`，同时也适用于其他语言，譬如：`{% ruby 噓 | うそ %} だの？`

## HTML 标签

插件为`hexo-tag-htmltag`，使用：

```markdown
{% htmlTag button type="button" data-submit data-action="add" aria-controls="calc"%}
Add 10
{% endhtmlTag %}
```

等效HTML代码：

```html
<button type="button" data-submit data-action="add" aria-controls="calc">Add 10</button>
```
