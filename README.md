# **YouTube Music - 'Your Likes' Downloader**
## A downloader of your all-time favourite playlist for autonomous listening

**YouTube Music - 'Your Likes' Downloader** or else **ytm-yld**, is a **command-line/terminal utility** used to either download or parse your favourite songs from YouTube Music.

***

**Features:**
- Downloading of a whole playlist
- Downloading of a part of a playlist for newly added songs
- Deleting songs that have been removed from the playlist
- Downloading playlist metadata as a JSON formatted file
- Format the songs in the playlist to a text file
- Downloading only the songs that you want

**This project future plans/updates can be seen at the ['Plans' Project](https://github.com/pepershukov/ytm-yld/projects/1).**  

Instructions per version may differ, so **if you are looking for instructions on previous versions, look into a specific version tag accordingly.**

&nbsp;

## Download

**Current version: [v6.1.0](https://github.com/pepershukov/ytm-yld/releases/tag/v6.1.0)**

**The latest release of this application can be found [here](https://github.com/pepershukov/ytm-yld/releases/latest).**

# TODO: DOWNLOAD TABLE

&nbsp;

## Requirements

The requirements download/instructions are listed in the [`requirements.txt`](https://raw.githubusercontent.com/pepershukov/ytm-yld/main/requirements.txt) in addition to Python pip packages needed with this project.

### Software requirements
- ***YouTube.com* cookie as a "Netscape HTTP Cookie File"**
  - See [`requirements.txt`](https://raw.githubusercontent.com/pepershukov/ytm-yld/main/requirements.txt) for help.

_**[FFmpeg](https://ffmpeg.org/)** is no longer required as it is bundled with the executable._  _(Update: [#6.1.0+](https://github.com/pepershukov/ytm-yld/releases/tag/v6.1.0))_

### Hardware minimum requirements
_**Linux is no longer supported** due to the incosistencies present._ _(Update: [#6.1.0+](https://github.com/pepershukov/ytm-yld/releases/tag/v6.1.0))_
- **Operating System** - Windows 8+
- **RAM** - minimum 100MB usable
- **Architecture** - x86_64

&nbsp;

## Usage

```
ytm-yld (--help | -h) [--cookie <path>] (--output <folder path>) (--mode ...) (--json <path>) (--config <path>)

[...] - required arguments
(...) - optional arguments

If the following arguments are not passed, the application will request them when necessary.
If they fail to validate, the application will recursively ask for them until success.
Arguments:
    --help | -h     - shows this message and exits

    --cookie        - the absolute path to file of a YouTube.com cookie as a 'Netscape HTTP Cookie File'
    
    --output        - the absolute path to folder where you want your music (synced/downloaded)/playlist-to-text file
    
    --mode          - mode (t|d|s|m|j) to request for the application to complete
    
    --json          - the absolute path to an existing JSON playlist data file instead of downloading
    
    --config        - the absolute path to the config file containing section `ytm-yld`
                    - see https://github.com/pepershukov/ytm-yld#config for quickstart
```

**Make sure that the files within the output folder are desired for this application only. Otherwise, they could be at risk of deletion or corruption when 'downloading' or 'syncing'.**

*If you choose not to pass the arguments, you will have to enter the paths upon the application input request.*

_(Update: [#1.1.0+](https://github.com/pepershukov/ytm-yld/releases/tag/v1.1.0))_ **If the paths turn out to be invalid or non-existant, or the file formatting is wrong, ~the application will throw out an error~** _(Update: [#6.0.0+](https://github.com/pepershukov/ytm-yld/releases/tag/v6.0.0))_ **the application will ask for them recursively untill success.**

&nbsp;

## Quickstart

### Modes
You will be asked upon starting the application to select the mode of your choice.  
_(Update: [#2.0.0+](https://github.com/pepershukov/ytm-yld/releases/tag/v2.0.0))_ As there is **no 'all' mode**, you can **stack the modes together** with an input request; for example, if I would want to go through all the modes, I will write `tdsjm` _(order of items does not matter)_ as the mode of my choice. Similarly, if I would want two specific modes - download & sync - I will write `ds` _(again, order of items does not matter)_; and so on.

**There are currently five modes:**
- **Playlist-to-text (`t`)**
  - Saves the songs' information to a text file as a table
- **Download (`d`)**
  - Downloads the songs that the application finds not existing locally
- **Sync (`s`)** _(Update: [#2.0.0+](https://github.com/pepershukov/ytm-yld/releases/tag/v2.0.0))_
  - Deletes songs stored locally that have been removed from the playlist
- **JSON (metadata) (`j`)** _(Update: [#3.0.0+](https://github.com/pepershukov/ytm-yld/releases/tag/v3.0.0))_
  - Does not delete the JSON metadata of the playlist - mainly for advanced users to play around with it
- **Manual (`m`)** _(Update: [#4.0.0+](https://github.com/pepershukov/ytm-yld/releases/tag/v4.0.0))_
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
```
[ytm-yld]
cookie = 'absolute/path/to/cookie'
output = 'absolute/path/to/output'
mode = 'tdsjm'
json = 'absolute/path/to/json'
```