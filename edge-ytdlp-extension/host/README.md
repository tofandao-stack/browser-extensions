# YouTube to MP3 Native Host

The native application component that communicates between the browser extension and the local yt-dlp utility.

## Overview

This component runs as a native messaging host, bridging communication between the browser extension and the local yt-dlp command-line tool. It receives download requests from the browser and spawns the download script asynchronously.

## Files

- **native_host.py** - Main Python application that handles native messaging
- **download_youtube_mp3.sh** - Bash script that runs yt-dlp with configured options
- **youtube_mp3.json** - Native messaging manifest for browser registration
- **native_host.log** - Log file for host operations
- **yt_dlp.log** - Log file for yt-dlp operations

## System Requirements

- **OS**: Linux (required due to bash script and file paths)
- **Python**: 3.6+
- **yt-dlp**: Latest version
- **FFmpeg**: For audio conversion and metadata processing
- **Bash**: For running the download script

## Installation

### 1. Verify Dependencies

```bash
# Check Python version
python3 --version

# Install yt-dlp
pip install yt-dlp

# Install ffmpeg
sudo apt-get install ffmpeg
```

### 2. Register Native Manifest

The browser needs to know where to find the native host:

```bash
# For Edge
mkdir -p ~/.config/edge/NativeMessagingHosts
cp youtube_mp3.json ~/.config/edge/NativeMessagingHosts/

# For Chrome
mkdir -p ~/.config/google-chrome/NativeMessagingHosts
cp youtube_mp3.json ~/.config/google-chrome/NativeMessagingHosts/
```

### 3. Make Scripts Executable

```bash
chmod +x native_host.py
chmod +x download_youtube_mp3.sh
```

## Usage

The host is typically invoked automatically by the browser when the extension sends a native message. Direct invocation is not required for normal operation.

### Message Protocol

**Request**:
```json
{
  "action": "download",
  "url": "https://www.youtube.com/watch?v=..."
}
```

**Response**:
```json
{
  "ok": true,
  "started": true,
  "url": "https://www.youtube.com/watch?v=..."
}
```

## Configuration

### Download Directory

Edit `download_youtube_mp3.sh` to change where files are saved:

```bash
OUTDIR="${HOME}/path/to/music/directory"
```

### yt-dlp Options

Customize download behavior by editing `download_youtube_mp3.sh`:

```bash
yt-dlp \
  --cookies-from-browser edge \      # Use browser cookies
  --ignore-errors \                  # Continue on errors
  --no-playlist \                    # Don't download playlists
  --match-filter "duration < 1200" \ # Filter by duration
  -f "bestaudio/best" \              # Best audio quality
  -x --audio-format mp3 \            # Convert to MP3
  --audio-quality 0 \                # Highest quality
  --embed-metadata \                 # Add metadata
  --embed-thumbnail \                # Add album art
  # ... more options
```

## Logging

### Native Host Logs

Location: `$HOME/edge-ytdlp-extension/host/native_host.log`

Contains:
- Received messages (action, URL)
- Errors and exceptions
- Message timestamps

### Download Logs

Location: `$HOME/edge-ytdlp-extension/host/yt_dlp.log`

Contains:
- yt-dlp output and errors
- Download start/completion messages
- Progress information

### Viewing Logs

```bash
# Tail the native host log
tail -f ~/edge-ytdlp-extension/host/native_host.log

# Tail the download log
tail -f ~/edge-ytdlp-extension/host/yt_dlp.log
```

## Manifest File

The `youtube_mp3.json` file tells the browser where to find the native host:

```json
{
  "name": "youtube_mp3",
  "description": "Native host for sending YouTube URLs to local yt-dlp script",
  "path": "/full/path/to/native_host.py",
  "type": "stdio",
  "allowed_origins": [
    "chrome-extension://YOUR_EXTENSION_ID/*"
  ]
}
```

Update the `path` field to the full path of your `native_host.py` file, and set `allowed_origins` to your extension ID.

## Troubleshooting

### Extension Can't Find Host

- Verify the manifest file is installed in the correct directory
- Check that the `path` in the manifest points to the correct location
- Ensure `native_host.py` is executable: `chmod +x native_host.py`

### yt-dlp Fails

- Update yt-dlp: `pip install --upgrade yt-dlp`
- Verify ffmpeg is installed: `ffmpeg -version`
- Check the download log for specific errors

### Permissions Issues

- Ensure the output directory exists and is writable
- Check file permissions on the host and download scripts

### Message Not Received

- Verify the extension ID matches in the manifest
- Check browser console and native host logs
- Ensure native messaging is enabled in the browser

## Architecture

```
Browser Extension
        ↓
chrome.runtime.sendNativeMessage()
        ↓
native_host.py (reads stdin, writes stdout)
        ↓
subprocess.Popen() → download_youtube_mp3.sh
        ↓
yt-dlp
        ↓
MP3 file saved to OUTDIR
```

## Platform Support

- ✅ Linux (fully supported)
- ❌ Windows (paths need adjustment)
- ❌ macOS (paths need adjustment)

## Related Components

- **Browser Extension** - Provides the UI: `../extension/`
- **Main Project** - Overview and setup: `../README.md`
