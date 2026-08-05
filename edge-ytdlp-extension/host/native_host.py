#!/usr/bin/env python3
import json
import os
import struct
import subprocess
import sys

SCRIPT_PATH = os.path.expanduser("~/edge-ytdlp-extension/host/download_youtube_mp3.sh")
LOG_FILE = os.path.expanduser("~/edge-ytdlp-extension/host/native_host.log")
# Note: Update SCRIPT_PATH if you clone this project to a different location


def log(msg: str) -> None:
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")


def read_message():
    raw_length = sys.stdin.buffer.read(4)
    if len(raw_length) == 0:
        return None
    if len(raw_length) != 4:
        raise RuntimeError("Invalid message length header")

    message_length = struct.unpack("<I", raw_length)[0]
    message = sys.stdin.buffer.read(message_length).decode("utf-8")
    return json.loads(message)


def send_message(message):
    encoded = json.dumps(message).encode("utf-8")
    sys.stdout.buffer.write(struct.pack("<I", len(encoded)))
    sys.stdout.buffer.write(encoded)
    sys.stdout.buffer.flush()


def main():
    try:
        msg = read_message()
        if msg is None:
          return

        url = msg.get("url", "")
        action = msg.get("action", "")

        log(f"received action={action} url={url}")

        if action != "download" or not url:
            send_message({"ok": False, "error": "invalid_request"})
            return

        subprocess.Popen(
            [SCRIPT_PATH, url],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )

        send_message({"ok": True, "started": True, "url": url})

    except Exception as e:
        log(f"error: {e}")
        send_message({"ok": False, "error": str(e)})


if __name__ == "__main__":
    main()
