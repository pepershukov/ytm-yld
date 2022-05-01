# **YouTube Music - 'Your Likes' Downloader**
## A downloader of a playlist for autonomous listening to your favourite songs

***YouTube Music - 'Your Likes' Downloader*** or else ***ytm-yl-downloader***, is a command-line/terminal utility used to either download or parse your favourite songs from YouTube. *Therefore, because it is a command-line utility, there is **no graphical user interface.***

**Features:**
- Downloading of a whole playlist
- Downloading of a part of a playlist for newly added songs
- Format the songs in the playlist to a text file

**Plans:**
- Syncing songs that have been removed from the playlist

## Requirements

- **YouTube.com cookie as a "Netscape HTTP Cookie File"**
  >In order to extract cookies from browser use any conforming browser extension for exporting cookies. For example, [Get cookies.txt](https://chrome.google.com/webstore/detail/get-cookiestxt/bgaddhkoddajcdgocldbbfleckgcbcid/) (for Chrome) or [cookies.txt](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/) (for Firefox).  
  > Note that the cookies file must be in Mozilla/Netscape format and the first line of the cookies file must be either `# HTTP Cookie File` or `# Netscape HTTP Cookie File`. Make sure you have correct [newline format](https://en.wikipedia.org/wiki/Newline) in the cookies file and convert newlines if necessary to correspond with your OS, namely `CRLF` (`\r\n`) for Windows and `LF` (`\n`) for Unix and Unix-like systems (Linux, macOS, etc.).
  - *This application does not store/send the cookies for the use outside of this application.*
- **FFmpeg installed**
  - The latest *FFmpeg* package for installation can be found [here](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z).

## Usage

```
ytm-yl-downloader.exe [ffmpeg] [cookie]  
  
Arguments:
    ffmpeg      the absolute path to folder of the binaries of FFmpeg installation (by default, installed in 'C:/Program Files/ffmpeg/bin' in Windows)
    cookie      the absolute path to file of a YouTube.com cookie as a "Netscape HTTP Cookie File"
```
*If you choose not to pass the arguments, you will have to enter the paths upon the application input request.*

If the paths turn out to be wrong/misspelt, `yt-dlp` (`youtube-dl`) will throw out an error.

## Quickstart

You will be asked upon starting the application to select the mode of your choice. 

**There are currently three modes:**
- Playlist-to-text (`t`)
- Download only (`d`)
- Both (`b`)

**Playlist-to text (`t`)** will save the songs' information to a text file as a table  
**Download only (`d`)** will download the songs that the application finds not existing locally  
**Both (`b`)** is a combination of the two modes above
