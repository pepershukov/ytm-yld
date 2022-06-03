# **YouTube Music - 'Your Likes' Downloader**
## A downloader of your all-time favourite playlist for autonomous listening

***YouTube Music - 'Your Likes' Downloader*** or else ***ytm-yl-downloader***, is a **command-line/terminal utility** used to either download or parse your favourite songs from YouTube. *Therefore, because it is a command-line utility, there is **no graphical user interface.***

**Features:**
- Downloading of a whole playlist
- Downloading of a part of a playlist for newly added songs
- Deleting songs that have been removed from the playlist
- Format the songs in the playlist to a text file

**This project future plans/updates can be seen at the ['Plans' Project](https://github.com/pepershukov/ytm-yl-downloader/projects/1).**  

Instructions per version may differ, so **if you are looking for instructions on previous versions, look into a specific version tag accordingly.**

## Requirements

- ***YouTube.com* cookie as a "Netscape HTTP Cookie File"**
  >In order to extract cookies from browser use any conforming browser extension for exporting cookies. For example, [Get cookies.txt](https://chrome.google.com/webstore/detail/get-cookiestxt/bgaddhkoddajcdgocldbbfleckgcbcid/) (for Chrome) or [cookies.txt](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/) (for Firefox).  
  >Note that the cookies file must be in Mozilla/Netscape format and the first line of the cookies file must be either `# HTTP Cookie File` or `# Netscape HTTP Cookie File`. Make sure you have correct [newline format](https://en.wikipedia.org/wiki/Newline) in the cookies file and convert newlines if necessary to correspond with your OS, namely `CRLF` (`\r\n`) for Windows and `LF` (`\n`) for Unix and Unix-like systems (Linux, macOS, etc.).
  - *This application does not store/send the cookies for the use outside of this application.*
- ***FFmpeg* installed**
  - _(Update: [#1.1.0+](https://github.com/pepershukov/ytm-yl-downloader/releases/tag/v1.1.0))_ _**Only necessary if you are to download music from YouTube. If you want to simply parse the playlist into a text output or sync songs stored locally, FFmpeg is not required.**_
  - The latest *FFmpeg* package for installation can be found [here](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z).

## Usage

_(Update: [#1.1.0+](https://github.com/pepershukov/ytm-yl-downloader/releases/tag/v1.1.0))_ - Reordered terms
```
ytm-yl-downloader.exe [cookie] <ffmpeg> 

[...] - required arguments
<...> - optional arguments
Further information on requirements can be found in the README.md.

Arguments:
    cookie      the absolute path to file of a YouTube.com cookie as a "Netscape HTTP Cookie File"
    ffmpeg      the absolute path to folder of the binaries of FFmpeg
```
*If you choose not to pass the arguments, you will have to enter the paths upon the application input request.*

_(Update: [#1.1.0+](https://github.com/pepershukov/ytm-yl-downloader/releases/tag/v1.1.0))_ **If the paths turn out to be invalid or non-existant, or the file formatting is wrong, the application will throw out an error.**

## Quickstart

You will be asked upon starting the application to select the mode of your choice.  
_(Update: [#2.0.0+](https://github.com/pepershukov/ytm-yl-downloader/releases/tag/v2.0.0))_ As there is **no 'all' mode**, you can **stack the modes together** with an input request; for example, if I would want to go through all the modes, I will write `tds` _(order of items does not matter)_ as the mode of my choice. Similarly, if I would want two specific modes - download & sync - I will write `ds` _(again, order of items does not matter)_; and so on.

**There are currently three modes:**
- **Playlist-to-text only (`t`)**
  - Saves the songs' information to a text file as a table
- **Download only (`d`)**
  - Downloads the songs that the application finds not existing locally
- **Sync only (`s`)** _(Update: [#2.0.0+](https://github.com/pepershukov/ytm-yl-downloader/releases/tag/v2.0.0))_
  - Deletes songs stored locally that have been removed from the playlist