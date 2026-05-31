from flask import Flask, request, jsonify, send_file, send_from_directory
import os
import uuid
import subprocess
import threading
import time
import shutil
import re
from urllib.parse import urlparse

app = Flask(__name__)

VIDEO_DIR = "videos"
YTDLP = "yt-dlp"

FILE_EXPIRE = 3600  # 1小时删除
MIN_FREE_SPACE = 1024 * 1024 * 1024  # 最少需要1GB空闲

TASKS = {}
DOWNLOADING = False

if not os.path.exists(VIDEO_DIR):
    os.makedirs(VIDEO_DIR)

@app.route("/")
def home():
    return send_file("index.html")

def is_youtube_url(url):

    try:

        host = urlparse(url).hostname

        if not host:
            return False

        host = host.lower()

        return host in [
            "youtube.com",
            "www.youtube.com",
            "youtu.be",
            "www.youtu.be",
            "m.youtube.com"
        ]

    except:
        return False

# 检查磁盘空间
def check_disk_space():

    total, used, free = shutil.disk_usage("/")

    if free < MIN_FREE_SPACE:
        return False

    return True


# 创建任务
@app.route("/task", methods=["POST"])
def create_task():

    cleanup_once()

    global DOWNLOADING

    data = request.json
    url = data.get("url")

    if not url:
        return jsonify({"error": "no url"})

    if not is_youtube_url(url):
        return jsonify({"error": "invalid url"})

    if DOWNLOADING:
        return jsonify({
            "error": "busy",
            "message": "当前已经有下载任务正在进行"
        })

    if not check_disk_space():
        return jsonify({
            "error": "disk_full",
            "message": "服务器磁盘空间不足"
        })

    task_id = str(uuid.uuid4())

    TASKS[task_id] = {
        "status": "downloading",
        "file": None,
        "time": time.time()
    }

    DOWNLOADING = True

    thread = threading.Thread(target=download_video, args=(task_id, url))
    thread.daemon = True
    thread.start()

    return jsonify({"task": task_id})


# 查询任务
@app.route("/status/<task_id>")
def task_status(task_id):

    task = TASKS.get(task_id)

    if not task:
        return jsonify({"error": "task not found"})

    return jsonify(task)


# 下载视频
def download_video(task_id, url):

    global DOWNLOADING

    try:

        output = f"{VIDEO_DIR}/{task_id}.%(ext)s"

        cmd = [
            YTDLP,
            "--force-ipv4",
            "--no-playlist",
            "--concurrent-fragments", "3",
            "--throttled-rate", "100K",
            "-f", "bv*+ba/b",
            "--merge-output-format", "mp4",
            "-o", output,
            url
        ]

        subprocess.run(
            cmd,
            check=True,
            timeout=1800
        )

        TASKS[task_id]["status"] = "finished"
        for file in os.listdir(VIDEO_DIR):
            if file.startswith(task_id):
                TASKS[task_id]["file"] = file

    except Exception as e:

        TASKS[task_id]["status"] = "error"
        TASKS[task_id]["error"] = str(e)

    finally:

        DOWNLOADING = False


# 下载文件
@app.route("/videos/<path:filename>")
def videos(filename):
    return send_from_directory(VIDEO_DIR, filename)



def cleanup_once():

    now = time.time()

    for file in os.listdir(VIDEO_DIR):

        path = os.path.join(VIDEO_DIR, file)

        if os.path.isfile(path):

            if now - os.path.getmtime(path) > FILE_EXPIRE:
                os.remove(path)

@app.route("/recent")
def recent_downloads():

    try:

        result = subprocess.check_output(
            "journalctl -u ytdlp -n 200 | grep 'Extracting URL'",
            shell=True
        ).decode()

        videos = []

        for line in result.splitlines():

            m = re.search(r'(https://www\.youtube\.com/watch\?v=[\w-]+|https://youtu\.be/[\w-]+)', line)

            if m:
                videos.append(m.group(0))

        # 去重并保留顺序
        seen = set()
        unique = []

        for v in videos[::-1]:
            if v not in seen:
                unique.append(v)
                seen.add(v)

        return jsonify(unique[:10])

    except Exception:
        return jsonify([])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
