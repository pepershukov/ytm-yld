# **YTMusic - 'Your Likes' Downloader**
## A downloader of your all-time favourite playlist for autonomous listening

**YTMusic - 'Your Likes' Downloader** or else **ytm-yld**, is a **command-line/terminal utility** used to either download or parse your favourite songs from YouTube Music.

***

**Features:**
- Downloading of a whole playlist
- Downloading of a part of a playlist for newly added songs
- Deleting songs that have been removed from the playlist
- Downloading playlist metadata as a JSON formatted file
- Format the songs in the playlist to a text file
- Downloading only the songs that you want
- Downloading lyrics for songs
- Excluding certain elements of song data from saving

Instructions per version may differ, so **if you are looking for instructions on previous versions, look into a specific version tag or commit accordingly.**

&nbsp;

## Download

**Current version: [v8.0.2](https://github.com/pepershukov/ytm-yld/releases/tag/v8.0.2)**

**The latest release of this application can be found [here](https://github.com/pepershukov/ytm-yld/releases/latest).**

| **Operating System** | **Download Link** | **Size** | **Hash - SHA216** |
|:---:|:---:|:---:|:---:|
| Windows | https://github.com/pepershukov/ytm-yld/releases/download/v8.0.2/ytm-yld_win.exe | 47.5MB (49868710) | 6D2AA9BEC512F5626BBAE4CD80EBD4F853974D5E71DA4476DB63147347B9550C |

&nbsp;

## Requirements

The requirements download/instructions are listed in the [`requirements.txt`](https://github.com/pepershukov/ytm-yld/blob/main/requirements.txt) in addition to Python pip packages needed with this project.

### Software requirements
- ***YouTube.com* cookie as a "Netscape HTTP Cookie File"**
  - See [`requirements.txt`](https://raw.githubusercontent.com/pepershukov/ytm-yld/main/requirements.txt) for help.

_**[FFmpeg](https://ffmpeg.org/)** is no longer required as it is bundled with the executable._  _([7.0.0+](https://github.com/pepershukov/ytm-yld/releases/tag/v7.0.0))_

### Hardware minimum requirements
_**Linux is no longer supported** due to the inconsistencies present._ _([7.0.0+](https://github.com/pepershukov/ytm-yld/releases/tag/v7.0.0))_
- **Operating System** - Windows 8+
- **RAM** - minimum 100MB usable
- **Architecture** - x86_64

&nbsp;

## Usage

```
usage: ytm-yld [-h] [--version] [--update] [--config [file]] [--cookie [file]] [--output [folder]] [--mode [... ...]]
               [--json [file]] [--songs-json [file]] [--no-title [id,id...]] [--no-artist [id,id...]] [--no-album [id,id...]]
               [--no-cover [id,id...]] [--no-lyrics [id,id...]]

A command-line downloader of YouTube Music - 'Your Likes' playlist

options:
  -h, --help            show this help message and exit
  --version, -v         show program's version number and exit
  --update, -u          check for update and exit

General options:
  --config [file]       absolute path to config file containing sector 'ytm-yld'
  --cookie [file]       absolute path to YouTube.com cookie as a 'Netscape HTTP Cookie File'
  --output [folder]     absolute path to folder where you want your music synced/download/playlist-to-text file
  --mode [... ...]      mode (t|d|s|m|j) to request for the application to complete
  --json [file]         absolute path to existing JSON playlist metadata file instead of downloading
  --songs-json [file]   absolute path to existing JSON songs metadata file instead of downloading

Music metadata options:
  For these, it can act as a global parameter for all songs if no specific IDs are passed.

  --no-title [id,id...]
                        whether to include the title of the songs or not
  --no-artist [id,id...]
                        whether to include the artist of the songs or not
  --no-album [id,id...]
                        whether to include the album name of the songs or not
  --no-cover [id,id...]
                        whether to include the album art/cover of the songs or not
  --no-lyrics [id,id...]
                        whether to include the lyrics of the songs or not
```

**Make sure that the files within the output folder are desired for this application only. Otherwise, they could be at risk of deletion or corruption when 'downloading' or 'syncing'.**

If you choose not to pass the arguments, you will have to enter the paths upon the application input request.

_([1.1.0+](https://github.com/pepershukov/ytm-yld/releases/tag/v1.1.0))_ **If the paths turn out to be invalid or non-existant, or the file formatting is wrong, ~the application will throw out an error~** _([6.0.0+](https://github.com/pepershukov/ytm-yld/releases/tag/v6.0.0))_ **the application will ask for them recursively until success.**

&nbsp;

## Quickstart

### Modes
You will be asked upon starting the application to select the mode of your choice.

**There are currently five modes:**
- **Playlist-to-text (`t`)**
  - Saves the songs' information to a text file as a table
- **Download (`d`)**
  - Downloads the songs that the application finds not existing locally
- **Sync (`s`)** _([2.0.0+](https://github.com/pepershukov/ytm-yld/releases/tag/v2.0.0))_
  - Deletes songs stored locally that have been removed from the playlist
- **JSON (metadata) (`j`)** _([3.0.0+](https://github.com/pepershukov/ytm-yld/releases/tag/v3.0.0))_
  - Does not delete the JSON metadata of the playlist - mainly for advanced users to play around with it
- **Manual (`m`)** _([4.0.0+](https://github.com/pepershukov/ytm-yld/releases/tag/v4.0.0))_
  - Gives a choice of songs to download to the user - therefore you have to input songs you want to download manually

### Config
You can pass the config file in the arguments under the `--config` argument instead of passing all other arguments you need. Config files otherwise could be used to automate the application start further or make its use easier. Below is a quickstart to the config file format.

- The application uses an `.ini`-like format
- All the variables regarding the application have to be under sector `ytm-yld`
  - The application will throw an error and exit if this fails
- The variable names are the same as argument tags
- The values of the variables must not be empty
- Not all variables have to be passed
  - You still can pass the arguments for variables that are not in the config file

Here is an **example** of a **full config file**:
``` ini
[ytm-yld]
cookie = absolute/path/to/cookie
output = absolute/path/to/output
mode = tdsjm
json = absolute/path/to/json
songs-json = absolute/path/to/json

# The music metadata options have two variants of working
# 1. Selecting 'true' - choosing it globally for all songs
# 2. Selecting IDs in a list - MUST put DOUBLE SPEECH-MARKS!! - choosing songs seperately 
no-title = ["1-iKwZKc7Ok"]
no-artist = ["1-iKwZKc7Ok", "FXovf5dsRTw"]
no-album = true
no-cover = TRUE
no-lyrics = True
```