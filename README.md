# **YouTube Music - 'Your Likes' Downloader**
## A downloader of your all-time favourite playlist for autonomous listening

**YouTube Music - 'Your Likes' Downloader** or else **ytm-yld**, is a **command-line/terminal utility** used to either download or parse your favourite songs from YouTube Music.

**Features:**
- Downloading of a whole playlist
- Downloading of a part of a playlist for newly added songs
- Deleting songs that have been removed from the playlist
- Downloading playlist metadata as a JSON formatted file
- Format the songs in the playlist to a text file
- Downloading only the songs that you want

**This project future plans/updates can be seen at the ['Plans' Project](https://github.com/pepershukov/ytm-yld/projects/1).**  

Instructions per version may differ, so **if you are looking for instructions on previous versions, look into a specific version tag accordingly.**

## Download

**The latest release of this application can be found [here](https://github.com/pepershukov/ytm-yld/releases/latest).**

| Operating System | Link | Size | SHA256 |
|---|---|---|---|
| Linux | https://github.com/pepershukov/ytm-yld/releases/download/v5.0.2/ytm-yld_linux | 18.0MB (18899256) | F22D3AC49B31E50CDD639AA3CFC0F24701BABFE0CA6A3207854BE802CC7745FD |
| Windows | https://github.com/pepershukov/ytm-yld/releases/download/v5.0.2/ytm-yld_windows.exe | 14.5MB (15284474) | DE232992F86773DD39DD5AF8E14F9E7E278D76E5E7B1593B95DD3014A18E17B7 |

## Requirements

### Software requirements
- ***YouTube.com* cookie as a "Netscape HTTP Cookie File"**
  - *This application does not store/send the cookies for the use outside of this application.*
- ***FFmpeg* installed**
  - _(Update: [#1.1.0+](https://github.com/pepershukov/ytm-yld/releases/tag/v1.1.0))_ Only necessary if you are to download music from YouTube. If you want to simply parse the playlist into a text output or sync songs stored locally, FFmpeg is not required.

### Hardware minimum requirements
| Operating System | Linux                                                                                            | Windows                                                                                          |
|------------------|--------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------|
| RAM              | Minimum 100MB usable. Need more than 100MB if you have more than ~200 songs (500KB per one song) | Minimum 100MB usable. Need more than 100MB if you have more than ~500 songs (200KB per one song) |
| Architecture     | x86_64                                                                                           | x86_64                                                                                           |
| Other            | Internet access                                                                                  | Internet access                                                                                  |

The requirements download/instructions are listed in the [`requirements.txt`](https://raw.githubusercontent.com/pepershukov/ytm-yld/main/requirements.txt) in addition to Python pip packages needed with this project.

## Usage

```
ytm-yld (--help) [--cookie ...] (--ffmpeg ...) (--output ...) (--mode ...) (--json ...) (--config ...)

[...] - required arguments
(...) - optional arguments
Further information on requirements can be found in the README.md.
https://github.com/pepershukov/ytm-yld#readme

If the following arguments are not passed, the application will request them when necessary.
And if they fail to validate within the app, the application will throw an error.
Arguments:
    --help          - shows this message and exits

    --cookie        - the absolute path to file of a YouTube.com cookie as a 'Netscape HTTP Cookie File'

    --ffmpeg        - (Windows) the absolute path to FFmpeg folder
                    - (Linux) the absolute path to FFmpeg file binary
                    - only necessary if you are to select 'd' mode
    
    --output        - the absolute path to folder where you want your music(synced/downloaded)/playlist-to-text file
    
    --mode          - mode (t|d|s|m|j) to request for the application to complete
    
    --json          - the absolute path to an existing JSON playlist data file instead of downloading
    
    --config        - the absolute path to the config file containing section `ytm-yld`
                    - see https://github.com/pepershukov/ytm-yld#config for quickstart
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

## Config
You can pass the config file in the arguments under the `--config` tag instead of passing all other arguments you need. Config files otherwise could be used to automate the application start further or make its use easier. Further is a quickstart to the config file format.

- The application uses an `.ini`-like format
- All the variables regarding the application have to be under sector `ytm-yld`
  - The application will throw an error and exit if this fails
- The variable names are the same as argument tags
- The values of the variables must not be empty
- Not all variables have to be passed
  - You still can pass the arguments for variables that are not in the config file

Here is an **example** of a **full config file**:
```
[ytm-yld]
cookie = 'absolute/path/to/cookie'
ffmpeg = 'absolute/path/to/ffmpeg'
output = 'absolute/path/to/output'
mode = 'tdsjm'
json = 'absolute/path/to/json'
```

## Building an executable

This further guide is mainly for developers, trying to either test their code or to experiment with the results of their contribution to this project. It will show you how to build an executable out of a Python project.

1. Download and install [Python](https://python.org) _(if not already)_  
 1.1 **(Windows)** During install, make sure to check `Add Python x.x.x to PATH`. Otherwise, [add Python and scripts to PATH manually](https://datatofish.com/add-python-to-windows-path/).
2. Download and install [git-scm](https://git-scm.com/downloads) _(if not already)_
3. Run this command in the Terminal (copy & paste & Enter):
 >**Windows:**
 >```
 >git clone https://github.com/pepershukov/ytm-yld.git %userprofile%/Downloads/ytm-yld && ^
 >cd %userprofile%/Downloads/ytm-yld && ^
 >python -m pip install -U -r requirements.txt && ^
 >pyinstaller --name ytm-yld_windows --onefile --workpath ./temp --distpath ./ --hidden-import=yt_dlp.compat._legacy main.py && ^
 >rmdir /s /q temp && ^
 >del /s /q ytm-yld_windows.spec
 >```
 >**Linux:** 
 >```
 >git clone https://github.com/pepershukov/ytm-yld.git ~/Downloads/ytm-yld; \
 >cd ~/Downloads/ytm-yld; \
 >alias python='python3'; \
 >export PATH="$HOME/.local/bin:$PATH"; \
 >python -m pip install -U -r requirements.txt; \
 >pyinstaller --name ytm-yld_linux --onefile --workpath ./temp --distpath ./ --hidden-import=yt_dlp.compat._legacy main.py; \
 >rm -r temp; \
 >rm ytm-yld_linux.spec
 >```    
4. You will find your executable as `ytm-yld_linux` *(Linux)* or `ytm-yld_windows.exe` *(Windows)*
