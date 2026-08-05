# YouTube to MP3 Browser Extension

The browser extension component that provides the UI for downloading YouTube videos as MP3s.

## Overview

This extension adds a toolbar button to Edge/Chrome browsers. Clicking the button on any YouTube video initiates a download via the native host application.

## Files

- **manifest.json** - Extension configuration and permissions
- **background.js** - Service worker that handles user interactions and native messaging

## How It Works

1. User clicks the extension icon while on a YouTube page
2. The background script validates that the current URL is a YouTube domain
3. If valid, it sends a native message to the host application with the video URL
4. The host application receives the message and queues the download
5. Download progress is logged to the browser console

## Permissions

The extension requires:

- **activeTab** - To access the current tab URL
- **nativeMessaging** - To communicate with the native host
- **Host permissions** - Access to youtube.com, youtu.be, and music.youtube.com

## Installation

See the parent project's [README.md](../README.md) for installation instructions.

## Development

### Structure

```javascript
// The extension communicates via:
chrome.runtime.sendNativeMessage(HOST_NAME, {
  action: "download",
  url: url
});
```

### Debugging

Open the Extensions page and click "Service Worker" under this extension to view console logs.

### Manifest v3

This extension uses Manifest v3 (the latest standard) and requires a modern browser.

## Testing

To test the extension locally:

1. Load the extension in developer mode
2. Navigate to a YouTube video
3. Click the extension icon
4. Check the browser console and native host logs for messages

## Related Components

- **Native Host** - The Python application that receives messages: `../host/`
- **Download Script** - The bash script that runs yt-dlp: `../host/download_youtube_mp3.sh`
