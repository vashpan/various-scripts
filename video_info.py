#!/usr/bin/env python3

# list video files under given paths together with codec, resolution, length, bitrate and size

import argparse
import json
import os
import shutil
import subprocess
import sys

VIDEO_EXTENSIONS = {
    ".3gp",
    ".avi",
    ".flv",
    ".m4v",
    ".mkv",
    ".mov",
    ".mp4",
    ".mpeg",
    ".mpg",
    ".mts",
    ".m2ts",
    ".ts",
    ".webm",
    ".wmv",
}


def human_readable_size(num):
    if num < 1024:
        return f"{num}B"
    elif num < 1024**2:
        return f"{num / 1024:.1f}K"
    elif num < 1024**3:
        return f"{num / 1024**2:.1f}M"
    else:
        return f"{num / 1024**3:.1f}G"


def human_readable_duration(num):
    total_seconds = max(0, int(round(num)))
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if hours > 0:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    return f"{minutes}:{seconds:02d}"


def human_readable_bitrate(num):
    if num < 0:
        return "?"
    elif num < 1000:
        return f"{num}bps"
    elif num < 1000**2:
        return f"{num / 1000:.1f}Kbps"
    elif num < 1000**3:
        return f"{num / 1000**2:.1f}Mbps"
    else:
        return f"{num / 1000**3:.1f}Gbps"


def update_processing_status(message, previous_length=0):
    if not sys.stderr.isatty():
        return 0

    sys.stderr.write("\r" + message.ljust(previous_length))
    sys.stderr.flush()
    return len(message)


def clear_processing_status(length):
    if not sys.stderr.isatty() or length <= 0:
        return

    sys.stderr.write("\r" + (" " * length) + "\r")
    sys.stderr.flush()


def find_ffprobe():
    return shutil.which("ffprobe")


def is_video_file(path):
    if os.path.basename(path).startswith("._"):
        return False

    _, ext = os.path.splitext(path)
    return ext.lower() in VIDEO_EXTENSIONS


def iter_video_files(paths):
    video_files = []

    for path in paths:
        expanded_path = os.path.expanduser(path)

        if not os.path.exists(expanded_path):
            print(f"warning: path does not exist: {path}", file=sys.stderr)
            continue

        if os.path.isfile(expanded_path):
            if is_video_file(expanded_path):
                video_files.append(expanded_path)
            continue

        for root, dirs, files in os.walk(expanded_path):
            dirs.sort()
            for filename in sorted(files):
                full_path = os.path.join(root, filename)
                if is_video_file(full_path):
                    video_files.append(full_path)

    return sorted(video_files)


def probe_video(ffprobe_path, path):
    cmd = [
        ffprobe_path,
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=codec_name,width,height,bit_rate:format=duration,bit_rate",
        "-of",
        "json",
        path,
    ]

    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    if result.returncode != 0:
        return "error", "?", "ffprobe failed", -1, "?", -1

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        return "error", "?", "invalid output", -1, "?", -1

    streams = data.get("streams", [])
    if not streams:
        return "error", "?", "no video stream", -1, "?", -1

    stream = streams[0]
    codec = stream.get("codec_name") or "unknown"
    width = stream.get("width")
    height = stream.get("height")
    resolution = f"{width}x{height}" if width and height else "?"
    duration_text = "?"
    duration_seconds = -1
    bitrate_text = "?"
    bitrate_value = -1

    duration = data.get("format", {}).get("duration")
    if duration is not None:
        try:
            duration_seconds = float(duration)
        except (TypeError, ValueError):
            duration_text = "invalid duration"
        else:
            duration_text = human_readable_duration(duration_seconds)

    bitrate = data.get("format", {}).get("bit_rate")
    if bitrate is None:
        bitrate = stream.get("bit_rate")
    if bitrate is not None:
        try:
            bitrate_value = int(bitrate)
        except (TypeError, ValueError):
            bitrate_text = "invalid bitrate"
        else:
            bitrate_text = human_readable_bitrate(bitrate_value)

    return codec, resolution, duration_text, duration_seconds, bitrate_text, bitrate_value


def print_table(rows):
    headers = ("path", "codec", "resolution", "length", "bitrate", "size")
    widths = [len(header) for header in headers]

    for row in rows:
        values = (
            row["path"],
            row["codec"],
            row["resolution"],
            row["length_text"],
            row["bitrate_text"],
            row["size_text"],
        )
        for i, value in enumerate(values):
            widths[i] = max(widths[i], len(value))

    header_line = "  ".join(header.ljust(widths[i]) for i, header in enumerate(headers))
    separator_line = "  ".join("-" * widths[i] for i in range(len(headers)))

    print(header_line)
    print(separator_line)

    for row in rows:
        values = (
            row["path"],
            row["codec"],
            row["resolution"],
            row["length_text"],
            row["bitrate_text"],
            row["size_text"],
        )
        print("  ".join(value.ljust(widths[i]) for i, value in enumerate(values)))


def sort_rows(rows, sort_key, reverse):
    if sort_key == "path":
        key_func = lambda row: row["path"].lower()
    elif sort_key == "codec":
        key_func = lambda row: row["codec"].lower()
    elif sort_key == "resolution":
        key_func = lambda row: (row["width"] * row["height"], row["width"], row["height"])
    elif sort_key == "length":
        key_func = lambda row: row["length_seconds"]
    elif sort_key == "bitrate":
        key_func = lambda row: row["bitrate_value"]
    else:
        key_func = lambda row: row["size_bytes"]

    return sorted(rows, key=key_func, reverse=reverse)


def main():
    parser = argparse.ArgumentParser(
        description="list video files under given paths together with codec, resolution, length, bitrate and size"
    )
    parser.add_argument("paths", nargs="+", help="file or directory paths to scan")
    parser.add_argument(
        "--sort",
        choices=["path", "codec", "resolution", "length", "bitrate", "size"],
        default="path",
        help="sort output by selected column",
    )
    parser.add_argument(
        "--reverse",
        action="store_true",
        help="reverse sort order",
    )
    args = parser.parse_args()

    ffprobe_path = find_ffprobe()
    if ffprobe_path is None:
        print("ffprobe not found in PATH", file=sys.stderr)
        print("install ffmpeg/ffprobe or add ffprobe to PATH and try again", file=sys.stderr)
        exit(1)

    video_files = iter_video_files(args.paths)
    if not video_files:
        print("no video files found")
        return

    rows = []
    status_length = 0

    for path in video_files:
        status_length = update_processing_status(
            f"Processing video: {os.path.basename(path) or path}",
            status_length,
        )
        codec, resolution, length_text, length_seconds, bitrate_text, bitrate_value = probe_video(
            ffprobe_path, path
        )
        width = 0
        height = 0
        if "x" in resolution:
            width_text, height_text = resolution.split("x", 1)
            if width_text.isdigit() and height_text.isdigit():
                width = int(width_text)
                height = int(height_text)

        try:
            size_bytes = os.path.getsize(path)
        except OSError as e:
            size_bytes = -1
            size_text = f"error: {e}"
        else:
            size_text = human_readable_size(size_bytes)

        rows.append(
            {
                "path": path,
                "codec": codec,
                "resolution": resolution,
                "width": width,
                "height": height,
                "length_seconds": length_seconds,
                "length_text": length_text,
                "bitrate_value": bitrate_value,
                "bitrate_text": bitrate_text,
                "size_bytes": size_bytes,
                "size_text": size_text,
            }
        )

    clear_processing_status(status_length)
    rows = sort_rows(rows, args.sort, args.reverse)
    print_table(rows)


if __name__ == "__main__":
    main()
