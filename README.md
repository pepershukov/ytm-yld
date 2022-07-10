# **YouTube Music - 'Your Likes' Downloader**
## A downloader of your all-time favourite playlist for autonomous listening

***YouTube Music - 'Your Likes' Downloader*** or else ***ytm-yld***, is a **command-line/terminal utility** used to either download or parse your favourite songs from YouTube. *Therefore, because it is a command-line utility, there is **no graphical user interface.***

**Features:**
- Downloading of a whole playlist
- Downloading of a part of a playlist for newly added songs
- Deleting songs that have been removed from the playlist
- Downloading playlist metadata as a JSON formatted file
- Format the songs in the playlist to a text file
- Downloading only the songs that you want

**This project future plans/updates can be seen at the ['Plans' Project](https://github.com/pepershukov/ytm-yld/projects/1).**  

Instructions per version may differ, so **if you are looking for instructions on previous versions, look into a specific version tag accordingly.**

The latest patch notes of this application can be found [here](https://github.com/pepershukov/ytm-yld/releases/latest) and the latest version of the application to download can be found [here](https://github.com/pepershukov/ytm-yld/releases/latest/download/ytm-yld.exe).

## Requirements

- ***YouTube.com* cookie as a "Netscape HTTP Cookie File"**
  - *This application does not store/send the cookies for the use outside of this application.*
- ***FFmpeg* installed**
  - _(Update: [#1.1.0+](https://github.com/pepershukov/ytm-yld/releases/tag/v1.1.0))_ **Only necessary if you are to download music from YouTube. If you want to simply parse the playlist into a text output or sync songs stored locally, FFmpeg is not required.**

The requirements download/instructions are listed in the [`requirements.txt`](https://raw.githubusercontent.com/pepershukov/ytm-yld/main/requirements.txt) in addition to Python pip packages needed with this project.

## Usage

```
ytm-yld (--help) [--cookie ...] (--ffmpeg ...) (--output ...) (--mode ...) (--json ...)

[...] - required arguments
(...) - optional arguments
Further information on requirements can be found in the README.md.
https://github.com/pepershukov/ytm-yld#readme

If the following arguments are not passed, the application will request them when necessary.
And if they fail to validate within the app, the application will throw an error.
Arguments:
    --help          • shows this message and exits

    --cookie        • the absolute path to file of a YouTube.com cookie as a "Netscape HTTP Cookie File"

    --ffmpeg        • the absolute path to folder of the binaries of FFmpeg
                    • only necessary if you are to select 'd' mode
    
    --output        • the absolute path to folder where you want your music downloaded
                    • only necessary if you are to select 'd' mode
    
    --mode          • mode (t|d|s|m|j) to request for the application to complete
    
    --json          • the absolute path to an existing JSON playlist data file instead of downloading
```
*If you choose not to pass the arguments, you will have to enter the paths upon the application input request.*

_(Update: [#1.1.0+](https://github.com/pepershukov/ytm-yld/releases/tag/v1.1.0))_ **If the paths turn out to be invalid or non-existant, or the file formatting is wrong, the application will throw out an error.**

## Quickstart

You will be asked upon starting the application to select the mode of your choice.  
_(Update: [#2.0.0+](https://github.com/pepershukov/ytm-yld/releases/tag/v2.0.0))_ As there is **no 'all' mode**, you can **stack the modes together** with an input request; for example, if I would want to go through all the modes, I will write `tdsjm` _(order of items does not matter)_ as the mode of my choice. Similarly, if I would want two specific modes - download & sync - I will write `ds` _(again, order of items does not matter)_; and so on.

**There are currently four modes:**
- **Playlist-to-text (`t`)**
  - Saves the songs' information to a text file as a table
- **Download (`d`)**
  - Downloads the songs that the application finds not existing locally
- **Sync (`s`)** _(Update: [#2.0.0+](https://github.com/pepershukov/ytm-yld/releases/tag/v2.0.0))_
  - Deletes songs stored locally that have been removed from the playlist
- **JSON (`j`)** _(Update: [#3.0.0+](https://github.com/pepershukov/ytm-yld/releases/tag/v3.0.0))_
  - Does not delete the JSON metadata of the playlist - mainly for advanced users to play around with it
- **Manual (`m`)** _(Update: [#4.0.0+](https://github.com/pepershukov/ytm-yld/releases/tag/v4.0.0))_
  - Gives a choice of songs to download to the user - therefore you have to input songs you want to download manually

## Building an executable

This further guide is mainly for developers, trying to either test their code or to experiment with the results of their contribution to this project. It will show you how to build an executable out of a Python project.

1. Download and install [Python](https://python.org) _(if not already)_  
 1.1 **(Windows)** During install, make sure to check `Add Python x.x.x to PATH`. Otherwise, [add Python and scripts to PATH manually](https://datatofish.com/add-python-to-windows-path/).
2. Download and install [git-scm](https://git-scm.com/downloads) _(if not already)_
3. Run this command in the Terminal (copy & paste):
 >**Windows:**
 >```
 >git clone https://github.com/pepershukov/ytm-yld.git %userprofile%/Downloads/ytm-yld && ^
 >cd %userprofile%/Downloads/ytm-yld && ^
 >python -m pip install -U -r requirements.txt && ^
 >pyinstaller --name ytm-yld --onefile --workpath ./temp --distpath ./ --hidden-import=yt_dlp.compat._legacy main.py && ^
 >rmdir /s /q temp && ^
 >del /s /q ytm-yld.spec
 >```
 >**Linux:** 
 >```
 >git clone https://github.com/pepershukov/ytm-yld.git ~/Downloads/ytm-yld; \
 >cd ~/Downloads/ytm-yld; \
 >alias python='python3'; \
 >python -m pip install -U -r requirements.txt; \
 >export PATH="$HOME/.local/bin:$PATH"; \
 >pyinstaller --name ytm-yld --onefile --workpath ./temp --distpath ./ --hidden-import=yt_dlp.compat._legacy main.py; rm -r temp; \
 >rm ytm-yld.spec
 >```    
4. You will find your executable as `ytm-yld` *(Linux)* or `ytm-yld.exe` *(Windows)*
