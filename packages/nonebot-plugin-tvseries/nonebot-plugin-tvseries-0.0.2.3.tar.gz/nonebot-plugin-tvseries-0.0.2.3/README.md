# nonebot-plugin-tvseries

获取美剧

# 安装

## 环境(dockerfile)

```
ENV TZ=Asia/Shanghai
ENV LANG zh_CN.UTF-8
ENV LANGUAGE zh_CN.UTF-8
ENV LC_ALL zh_CN.UTF-8
ENV TZ Asia/Shanghai
ENV DEBIAN_FRONTEND noninteractive
```

## 本体

`pip install nonebot-plugin-tvseries`

## 依赖

```bash
apt install -y locales locales-all fonts-noto

apt-get install -y libnss3-dev libxss1 libasound2 libxrandr2 \
    libatk1.0-0 libgtk-3-0 libgbm-dev libxshmfence1

playwright install chromium && playwright install-deps
```

# 使用

`剧集` `tvseries`

# 有问题 提issue 最好pr
