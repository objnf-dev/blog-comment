---
type: page
title: PHP 7.3 及其插件编译
date: 2023-09-12 0:00
updated: 2023-09-12 0:00
categories: 开发与代码
tags:
  - PHP
  - 编译
---

今后文章会同步更新在[我的 CSDN 博客](https://blog.csdn.net/weixin_44911246)，但是还是以这个自己拿阿里云服务器搭建的网站为主的。不过CSDN有个好处是可以被国内的搜索引擎抓取到，嗯，省得我做搜索引擎优化了啊。

如果有人只想看完整写完的文章的话，也请左拐 CSDN，或者[这里](https://www.zhouweitong.site/tags/完成编写/)。主站开了七牛云加速，顺便做了 Google 、 Bing 和百度等的搜索引擎收录。最近身体欠佳。原定的学习计划和博客更新计划也不出意外的咕了。没有办法。健康是第一要务。等待过后慢慢去补吧。

## 编译 PHP

### 安装必要环境

包含编译器，和编译需要的库。所有的编译操作均在 Ubuntu 19.04 下进行。

```bash
sudo apt-get update
sudo apt install -y gcc g++ cmake make libxml2-dev libbz2-dev libcurl4-gnutls-dev libzip-dev libwebp-dev libpng-dev libjpeg-dev libxpm-dev libfreetype6-dev
```

### 下载源码

你可以 clone GitHub 上的代码：

```bash
git clone https://github.com/php/php-src.git
```

当然也可以到 [php.net](https://www.php.net/downloads.php) 下载源码并解压：

```bash
wget https://www.php.net/distributions/php-7.3.7.tar.gz
tar -xvzf php-7.3.7.tar.gz
rm php-7.3.7.tar.gz
cd php-7.3.7/
```

### 开始编译

首先读取插件列表（插件列表没有修改的时候可跳过此步骤）：

```bash
./buildconf --force
```

<!--more-->

然后进行基本配置：

```bash
mkdir phpbin
./configure \
            --prefix=~/Document/phpbin \ # 是非程序文件 install 的位置
            --exec-prefix=~/Document/phpbin \ # 是程序文件 install 的位置
            --enable-fpm \
            --enable-cli \
            --enable-embed=shared \
            --enable-phpdbg \
            --enable-phpdbg-webhelper \
            --enable-phpdbg-debug \
            --enable-debug \
            --enable-bcmath \
            --enable-calendar \
            --enable-exif \
            --enable-ftp \
            --enable-intl \
            --enable-mbstring \
            --with-curl \
            --enable-embedded-mysqli \
            --enable-pcntl \
            --enable-shmop \
            --enable-soap \
            --enable-sockets \
            --enable-sysvmsg \
            --enable-sysvsem \
            --enable-sysvshm \
            --enable-wddx \
            --enable-zip \
            --with-zlib \
            --with-zlib-dir \
            --with-pcre-jit \
            --with-pcre-regex \
            --with-iconv \
            --enable-mysqlnd \
            --enable-pdo \
            --enable-hash \
            --enable-ctype \
            --enable-json \
            --enable-session \
            --enable-xml \
            --enable-libxml \
            --enable-simplexml \
            --enable-fileinfo \
            --with-openssl \
            --with-gd \
            --with-webp-dir \
            --with-jpeg-dir \
            --with-png-dir \
            --with-xpm-dir
```

随后手动修改`Makefile`，手动将`CFLAGS_CLEAN`改成如下内容：

```makefile
CFLAGS_CLEAN = -I/usr/include -g -O0 -Wall $(PROF_FLAGS)
```

最后，开始多线程编译：

```bash
make all -j8
make install
```

php 程序主文件在  `~/Document/phpbin/bin/php` 处。

## 生成插件

生成插件需使用刚刚编译好的php可执行文件。当然你也可以额外在系统中安装一套php（环境）以备不时之需。

```bash
sudo apt install -y apache2 php7 php-xdebug mysql-server mysql-client
```

随后到php源码文件夹、ext文件夹下，运行

```bash
php ./ext_skel.php --ext hello_obj
```

如果已知插件应用的平台的话，可以加上`--onlyunix`或 `--onlywindows` 避免生成其他平台的config文件。

在`config.m4`文件中，注意前面的编译命令部分，如果你的插件是独立的，取消掉下面两行的注释（`dnl`）：

```text
PHP_ARG_ENABLE(hello_obj, whether to enable hello_obj support,
[  --enable-hello_obj          Enable hello_obj support], no)
```

但是如果你的插件依赖了其他插件的代码（头文件等），你需要保持上面两行的注释并取消下面两行的注释：

```text
PHP_ARG_WITH(hello_obj, for hello_obj support,
[  --with-hello_obj             Include hello_obj support])
```

注意，不同段的注释要保证对齐。

## 编译插件

最常见的两种方法：重新编译php本体和使用phpize单独编译插件。

编译php本体的办法很简单，即在`./configure`步骤处看情况加入`--enable-hello_obj`或 `--with-hello_obj` 参数即可。这种情况下，当没有php.ini配置文件时，插件是默认启用的，利用

```bash
php -r "phpinfo();"
```

命令可以查看phpinfo()输出信息。

用phpize的话，请注意使用 **你编译PHP时prefix指定的目录下的phpize（~/Document/phpbin/bin/phpize）**，保证版本一致。

`cd`到插件源码所在的目录，运行`phpsize`，会生成编译所需文件。

随后执行

```bash
./configure --with-php-config=<php-config bin>
```

其中php-config bin 为 **你编译PHP时prefix指定的目录下的php-config（~/Document/phpbin/bin/php-config）**。

编译并安装。

```bash
make
make install
```

.so文件会自动复制到插件文件夹。在php.ini中加载插件即可。

```ini
extension=hello_obj.so
```

当然，你也可以用phpize编译安装Xdebug等外置php插件。