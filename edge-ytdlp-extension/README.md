# YouTube to MP3 Edge Extension

A browser extension that integrates with yt-dlp to download YouTube videos as MP3 files directly from the browser.

## Overview

This project consists of two components:

- **Extension** - A browser extension (Edge/Chrome compatible) that adds a toolbar button
- **Host** - A native application that communicates with the browser extension to run yt-dlp

## Prerequisites

Before installing this project, ensure you have the following:

### System Requirements
- **Operating System**: Linux (required for the native host component)
- **Browser**: Microsoft Edge or Chromium-based browser (Chrome, Brave, etc.)

### Required Software
- **Python 3.6+** - Core requirement for the native host
  ```bash
  python3 --version  # Check if installed
  ```

- **yt-dlp** - YouTube downloader tool
  ```bash
  pip install yt-dlp
  ```

- **FFmpeg** - For audio conversion and metadata processing
  ```bash
  # For Debian/Ubuntu
  sudo apt-get install ffmpeg
  
  # For Fedora/RHEL
  sudo dnf install ffmpeg
  
  # For Arch
  sudo pacman -S ffmpeg
  ```

### Required Directories
- Music library directory (default: `$HOME/Music/library/`)
- Project installation directory (default: `$HOME/edge-ytdlp-extension/`)

## Installation

### 1. Clone or Extract the Project

```bash
# Clone the repository
git clone <repository-url>
cd browser-extensions/edge-ytdlp-extension

# Or if you have it in ~/edge-ytdlp-extension, ensure it's there
```

### 2. Verify Prerequisites

```bash
# Check Python version
python3 --version

# Check if yt-dlp is installed
yt-dlp --version

# Check if ffmpeg is installed
ffmpeg -version
```

Install any missing dependencies using the commands in the Prerequisites section.

### 3. Update Configuration Files

Edit the native messaging manifest to include your system's paths:

```bash
# Find the full path to native_host.py
FULL_PATH=$(pwd)/host/native_host.py
echo "Full path: $FULL_PATH"

# Edit the manifest and replace REPLACE_WITH_FULL_PATH_TO_NATIVE_HOST_PY with the path
nano host/youtube_mp3.json
```

Update `download_youtube_mp3.sh` if you want to use different directories:

```bash
# Edit the output and log directories if needed
nano host/download_youtube_mp3.sh
```

### 4. Make Scripts Executable

```bash
chmod +x host/native_host.py
chmod +x host/download_youtube_mp3.sh
```

### 5. Register the Native Host

The native messaging manifest must be registered with your browser:

```bash
# For Edge
mkdir -p ~/.config/edge/NativeMessagingHosts
cp host/youtube_mp3.json ~/.config/edge/NativeMessagingHosts/

# For Chrome
mkdir -p ~/.config/google-chrome/NativeMessagingHosts
cp host/youtube_mp3.json ~/.config/google-chrome/NativeMessagingHosts/

# For Chromium
mkdir -p ~/.config/chromium/NativeMessagingHosts
cp host/youtube_mp3.json ~/.config/chromium/NativeMessagingHosts/
```

### 6. Create Output Directory

```bash
mkdir -p ~/Music/library
```

### 7. Load the Extension in Your Browser

1. Open your browser and navigate to the extensions page:
   - **Edge**: `edge://extensions/`
   - **Chrome**: `chrome://extensions/`
   - **Chromium**: `chromium://extensions/`

2. Enable "Developer mode" (toggle in top-right corner)

3. Click "Load unpacked"

4. Select the `extension` directory from this project

5. Note the Extension ID (displayed on the extension card) - you'll need this for the manifest

6. Update the `allowed_origins` in `host/youtube_mp3.json`:
   ```json
   "allowed_origins": [
     "chrome-extension://YOUR_EXTENSION_ID/*"
   ]
   ```

7. Re-copy the manifest to the NativeMessagingHosts directory

## Usage

1. Navigate to any YouTube video:
   - youtube.com
   - youtu.be
   - music.youtube.com

2. Click the extension icon in your browser toolbar

3. The video will be queued for download as MP3

4. Check `~/Music/library/` for the downloaded file

Downloads are organized by playlist title with embedded metadata (artist, album, artwork).

## Project Structure

```
edge-ytdlp-extension/
├── extension/                      # Browser extension files
│   ├── manifest.json               # Extension configuration
│   ├── background.js               # Background script
│   └── README.md                   # Extension documentation
├── host/                           # Native host files
│   ├── native_host.py              # Python host application
│   ├── download_youtube_mp3.sh     # Download script
│   ├── youtube_mp3.json            # Native messaging manifest
│   ├── README.md                   # Host documentation
│   ├── native_host.log             # Host operation logs
│   └── yt_dlp.log                  # yt-dlp operation logs
└── README.md                       # This file
```

## Architecture

### Browser Extension → Native Host Communication

```
User clicks extension icon on YouTube page
    ↓
background.js validates URL and sends native message
    ↓
native_host.py receives message via stdin
    ↓
Spawns download_youtube_mp3.sh in background process
    ↓
download_youtube_mp3.sh runs yt-dlp
    ↓
FFmpeg converts to MP3 and embeds metadata
    ↓
MP3 file saved to ~/Music/library/
```

## Configuration

### Download Output Directory

Default: `$HOME/Music/library/`

To change, edit `host/download_youtube_mp3.sh`:

```bash
OUTDIR="${HOME}/path/to/your/music"
```

### Download Options

Customize download behavior in `host/download_youtube_mp3.sh`. Key options:

- `--audio-format mp3` - Output format
- `--audio-quality 0` - Best quality (0 = highest)
- `--match-filter "duration < 1200"` - Skip videos longer than 20 minutes
- `-f "bestaudio/best"` - Audio quality selection
- `--embed-metadata` - Add metadata to file
- `--embed-thumbnail` - Add album art

See [yt-dlp documentation](https://github.com/yt-dlp/yt-dlp#usage-and-options) for all available options.

## Logging

### Extension Console
- Open browser Developer Tools (F12)
- Go to "Application" → "Service Workers"
- Click the service worker under this extension
- View console logs

### Native Host Logs
- Location: `$HOME/edge-ytdlp-extension/host/native_host.log`
- Contains: Messages received, errors, timestamps

### Download Logs
- Location: `$HOME/edge-ytdlp-extension/host/yt_dlp.log`
- Contains: yt-dlp output, download progress, errors

### View Logs

```bash
# Watch native host logs in real-time
tail -f ~/edge-ytdlp-extension/host/native_host.log

# Watch download logs in real-time
tail -f ~/edge-ytdlp-extension/host/yt_dlp.log

# View combined recent activity
tail -20 ~/edge-ytdlp-extension/host/*.log
```

## Troubleshooting

### Extension doesn't appear in toolbar
- Check `edge://extensions/` or `chrome://extensions/`
- Look for error messages on the extension card
- Try disabling and re-enabling the extension

### Native host not found error
- Verify manifest is in correct directory: `~/.config/edge/NativeMessagingHosts/`
- Verify the `path` field in manifest points to correct location
- Ensure `native_host.py` is executable: `chmod +x host/native_host.py`
- Restart the browser after manifest changes

### yt-dlp "not found" error
- Install yt-dlp: `pip install yt-dlp`
- Verify it's in PATH: `which yt-dlp`
- Update to latest version: `pip install --upgrade yt-dlp`

### FFmpeg errors
- Install ffmpeg: `sudo apt-get install ffmpeg`
- Verify it's installed: `ffmpeg -version`

### Downloads fail silently
- Check `~/edge-ytdlp-extension/host/yt_dlp.log` for errors
- Verify output directory exists: `mkdir -p ~/Music/library`
- Check disk space: `df -h ~`

### Extension can't find native host after fresh install
- Verify manifest extension ID matches your loaded extension
- Update `allowed_origins` in manifest to match your extension ID
- Re-copy manifest to NativeMessagingHosts directory
- Restart browser completely (close all windows)

## Supported Domains

- ✅ youtube.com
- ✅ youtu.be
- ✅ music.youtube.com

## Platform Support

- ✅ Linux (fully supported)
- ⚠️ Windows (requires path adjustments and WSL for bash)
- ⚠️ macOS (requires path adjustments)

## Related Documentation

- [Extension Component](extension/README.md)
- [Native Host Component](host/README.md)
- [yt-dlp Documentation](https://github.com/yt-dlp/yt-dlp)
- [Chrome Native Messaging](https://developer.chrome.com/docs/apps/nativeMessaging/)

## License

See LICENSE file in the repository root.
