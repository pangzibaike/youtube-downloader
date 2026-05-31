# YouTube 下载器

一个基于 Flask 和 yt-dlp 的轻量级 YouTube 视频下载站。

English Version: [README_EN.md](README_EN.md)

## 功能

* Web 页面下载 YouTube 视频
* 自动合并音视频（MP4）
* 下载前显示视频预览图
* 中英文界面切换
* 文件自动过期清理（1小时）
* 磁盘空间保护
* 单任务队列，避免资源耗尽
* 下载超时保护（30分钟）

## 环境要求

* Python 3
* Flask
* yt-dlp
* ffmpeg

## 安装

### 安装 Flask

```bash
pip install Flask
```

### 安装 yt-dlp

```bash
python3 -m pip install -U yt-dlp
```

验证安装：

```bash
yt-dlp --version
```

### 安装 ffmpeg

Debian / Ubuntu：

```bash
apt update
apt install -y ffmpeg
```

## 运行

```bash
python3 server.py
```

浏览器访问：

```text
http://服务器IP:5001
```

## 项目结构

```text
.
├── server.py
├── index.html
└── videos/
```

## 注意事项

* 仅支持 YouTube 视频链接
* 下载文件 1 小时后自动删除
* 同时只允许一个下载任务
* 需要至少 1GB 可用磁盘空间
* 下载超过 30 分钟自动终止

## 安全特性

* YouTube 域名校验
* 下载超时保护
* 自动清理过期文件
* 下载前检查磁盘空间

## License

MIT License
