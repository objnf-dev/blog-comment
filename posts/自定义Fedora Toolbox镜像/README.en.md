---
type: page
title: Custom Fedora Toolbox Image
date: 2023-09-14 0:00
updated: 2023-09-14 0:00
categories: 自由探索
tags:
  - 容器
  - Linux
---

[Toolbox](https://github.com/containers/toolbox) can be seen as a wrapper for Podman, aiming to seamlessly integrate containers with the host operating system (Host OS). A similar tool to Toolbox is Distrobox. By sacrificing some container security features (such as port control, resource control, and file isolation), they achieve the following:

- User passthrough: Using the same user and home directory inside the container as the current Host user;
- Device passthrough: Directly accessing the Host's `/dev`, `/media`, etc.;
- Network passthrough: Directly using the Host network, providing a network experience identical to the host;
- Service passthrough: By directly utilizing the host's `/run/user/<uid>` and `/tmp` directories along with critical service sockets, it enables access to the host's display services (X11/Wayland), network services (Avahi), D-Bus, and systemd journal from within the container.

Therefore, Toolbox can be used to:

- **Serve as one of the software installation methods for immutable systems.** For example, Fedora Silverblue and Fedora CoreOS come pre-installed with Toolbox, while other immutable systems may have Distrobox pre-installed;
- Utilize images from other distributions to **seamlessly run programs designed for other distributions within the current one**. For instance, running a GUI program that only provides Ubuntu deb packages on Fedora;
- **Create a pseudo-root environment** when lacking root privileges on the Host. For example, even non-privileged Toolbox containers can use `sudo dnf install` to install software;
  - The image must have `sudo` package pre-installed, support the `sudo` and `wheel` groups to obtain root privileges, and enable the `NOPASSWD` option;
- Use different versions of images to achieve **"running old programs on new systems" or "running new programs on old systems"**, or to conduct compatibility testing for programs;
- Customizing the image enables **quick and consistent development environment setup**;

<!--more-->

## Create Your Own Toolbox Image

Any OCI-compliant container image can be used with Toolbox. In other words, you can build your own Toolbox image by following standard Docker image building methods.

The Fedora community continuously maintains the Fedora Toolbox image build files at [container/fedora-toolbox](https://src.fedoraproject.org/container/fedora-toolbox). Additionally, the community maintains Toolbox images for various mainstream distributions on GitHub at [toolbx-images/images](https://github.com/toolbx-images/images).

Taking the Fedora Toolbox image as an example, here is the official Dockerfile example:

```
# Use fedora:37 instead of fedora-toolbox:37
FROM registry.fedoraproject.org/fedora:37

# Image labels
ENV NAME=fedora-toolbox VERSION=37
LABEL com.github.containers.toolbox="true" \
      com.redhat.component="$NAME" \
      name="$NAME" \
      version="$VERSION" \
      usage="This image is meant to be used with the toolbox command" \
      summary="Base image for creating Fedora toolbox containers" \
      maintainer="Debarshi Ray <rishi@fedoraproject.org>"
 
COPY README.md /

# Make dnf install language files and documentation files for all languages when installing packages
RUN rm /etc/rpm/macros.image-language-conf
RUN sed -i '/tsflags=nodocs/d' /etc/dnf/dnf.conf

# [A] Install the complete core utilities (GNU Coreutils) including its language files
RUN dnf -y upgrade
RUN dnf -y swap coreutils-single coreutils-full
RUN dnf -y swap glibc-minimal-langpack glibc-all-langpacks

# [B] Completing languages and documentation through reinstallation
COPY missing-docs /
RUN dnf -y reinstall $(<missing-docs)
RUN rm /missing-docs

# [C] Install extra packages
COPY extra-packages /
RUN dnf -y install $(<extra-packages)
RUN rm /extra-packages

# [D] Ensure critical document files exist
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

Additionally, three extra files are required: `ensure-files`, `extra-packages`, and `missing-docs`.

To add or remove images in the Toolbox, you can directly modify the `extra-packages` file. When making changes, try to ensure that each line contains only the name of one software package. Alternatively, you can follow the `[C]` section in the aforementioned Dockerfile to use a custom file without modifying the `extra-packages` file.

For example,

```
COPY added-packages /
RUN dnf -y install $(<added-packages)
RUN rm /added-packages
```

and an example for `added-packages`,

```text
nodejs
npm
python3-pip
gcc
g++
```

### Adding Chinese Language Support to Toolbox Images

You can enable and set Chinese as the default display language for command-line/GUI programs within Toolbox by modifying the `LANG` variable, regenerating language files, and installing Chinese fonts.

1. Add language files: Add the following content before section `[B]` in the above Dockerfile example

```
# Chinese Language
RUN dnf install -y  glibc-locale-source glibc-langpack-zh langpacks-zh_CN
RUN localedef -c -i zh_CN -f UTF-8 zh_CN.UTF-8
```

2. Install fonts and IMEs: Add the following content before section `[C]` or `[D]` in the above Dockerfile example

```
# Install fonts and IMEs
RUN dnf install -y wqy-microhei-fonts wqy-zenhei-fonts fcitx5
```

3. Set the `LANG` environment variable: Add the following content at the end of the above Dockerfile example

```
# Set environment variables
ENV LANG zh_CN.UTF-8
```

## Using Toolbox Images

Taking the custom image tag `a.com/fedora-toolbox-customized:37` as an example:

1. Pull the custom image using `podman`

```bash
podman pull a.com/fedora-toolbox-customized:37
```

2. Use `toolbox` to create a container

```bash
# The container name can be specified arbitrarily
# When the host system is Fedora and the container is named fedora-toolbox-<host Fedora version>, this container is the default Toolbox container
toolbox create --image a.com/fedora-toolbox-customized:37 fedora-toolbox-37
```

3. Enter the container environment or execute specific programs within the container

```bash
# When the host has only one Toolbox container, it will directly enter that container
# When a Fedora system host has a default container, it will directly enter the default container
toolbox enter

# You can directly specify the command to be executed
toolbox run <command>

# When multiple Toolbox containers exist, you can specify which container to run using command parameters
toolbox enter <container_name>
toolbox run --container <container_name> <command>
```

## Delete Toolbox Container and Image

```bash
# Exit all windows currently using Toolbox CLI programs/GUI programs
# Stop the container
podman stop <container_name>

# Delete Container
toolbox rm <container_name>

# Delete Image
podman rmi a.com/fedora-toolbox-customized:37
```
