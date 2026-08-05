#!/usr/bin/env bash
set -euo pipefail

URL="${1:-}"
# Configure these paths for your system
OUTDIR="${HOME}/Music/library"
LOGFILE="${HOME}/edge-ytdlp-extension/host/yt_dlp.log"

if [[ -z "$URL" ]]; then
    echo "$(date -Is) ERROR: URL missing" >> "$LOGFILE"
    exit 1
fi

mkdir -p "$OUTDIR"

echo "$(date -Is) START download: $URL" >> "$LOGFILE"

yt-dlp \
  --cookies-from-browser edge \
  --ignore-errors \
  --no-playlist \
  --match-filter "duration < 1200" \
  -f "bestaudio/best" \
  -x --audio-format mp3 \
  --audio-quality 0 \
  --embed-metadata \
  --embed-thumbnail \
  --convert-thumbnails jpg \
  --postprocessor-args "FFmpegThumbnailsConvertor:-vf scale=500:500:force_original_aspect_ratio=decrease,pad=500:500:(ow-iw)/2:(oh-ih)/2" \
  --parse-metadata "title:(?s)(?P<meta_artist>.+?) - (?P<meta_title>.+)" \
  --parse-metadata "channel:(?s)(?P<meta_album>.+)" \
  -o "$OUTDIR/%(playlist_title)s/%(title)s.%(ext)s" \
  "$URL" >> "$LOGFILE" 2>&1

echo "$(date -Is) DONE download: $URL" >> "$LOGFILE"
