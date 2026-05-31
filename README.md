# YouTube Downloader

A lightweight YouTube video downloader built with Flask and yt-dlp.

## Features

* Download YouTube videos through a web interface
* Automatic video/audio merging (MP4)
* Video preview before download
* English / Chinese interface
* Automatic file cleanup after 1 hour
* Disk space protection
* Single download queue to prevent resource exhaustion
* Download timeout protection

## Requirements

* Python 3
* Flask
* yt-dlp
* ffmpeg

## Installation

### Install Flask

```bash
pip install Flask
```

### Install yt-dlp

```bash
python3 -m pip install -U yt-dlp
```

Verify installation:

```bash
yt-dlp --version
```

### Install ffmpeg

Debian / Ubuntu:

```bash
apt update
apt install -y ffmpeg
```

## Run

```bash
python3 server.py
```

Open your browser:

```text
http://SERVER_IP:5001
```

## Project Structure

```text
.
├── server.py
├── index.html
└── videos/
```

## Notes

* Only YouTube links are supported.
* Downloaded files are automatically removed after one hour.
* Only one download task can run at a time.
* A minimum of 1 GB free disk space is required.
* Downloads are automatically terminated after 30 minutes.

## Security Improvements

This project includes:

* Domain validation for YouTube URLs
* Download timeout protection
* Automatic cleanup of expired files
* Disk space checks before downloading

## License

MIT License
