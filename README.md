# **YTMusic - 'Your Likes' Downloader**
## A downloader of your all-time favourite playlist for offline listening

**YTMusic - 'Your Likes' Downloader** or else **ytm-yld**, is a **command-line/terminal utility** used to either download or parse your favourite songs from YouTube Music.
***
**Features:**
- Downloading of a whole playlist
- Downloading newly liked songs
- Deleting songs that have been unliked
- Downloading playlist metadata as a JSON file
- Export songs titles/artists/albums into a txt files
- Downloading only the songs that you want
- Downloading lyrics for songs
- Excluding certain elements of song data from saving, e.g album covers

Instructions per version may differ, so **if you are looking for instructions on previous versions, look into a specific version tag or commit accordingly.**

&nbsp;

## Download
  
**The latest release and its notes can be found [here](https://github.com/pepershukov/ytm-yld/releases/latest).**

| **OS** | **Download** | **Size** | **SHA216** |
|---|---|---|---|
| Windows | https://github.com/pepershukov/ytm-yld/releases/download/v9.0.0/ytm-yld_win.exe | 11MB (11516476) | E09753E8CD965943F5C1F4DB8D9E1966F027FF6CBD792CFB1BBB7EB1D29CE580 |

&nbsp;

## Requirements
The requirements download are listed in the [`requirements.txt`](https://github.com/pepershukov/ytm-yld/blob/main/requirements.txt) in addition to Python pip packages needed with this project.

### Software requirements
They are **only necessary if you are to download music**. For other parts of the app, you don't need them.
- **[FFmpeg and FFprobe](https://ffmpeg.org/download.html)** binaries in one folder
- **[yt-dlp](https://github.com/yt-dlp/yt-dlp/releases/latest)** binary

***YouTube.com*** cookie is not needed anymore as `ytmusicapi` handles OAuth. _([9.0.0+](https://github.com/pepershukov/ytm-yld/releases/tag/v9.0.0))_

### Hardware minimum requirements
- **Operating System** - Windows 8+
- **Architecture** - x86_64

&nbsp;

## Usage
```
usage: ytm-yld [-h] [--version] [--update] [--config [file]] [--headers [file]] [--yt-dlp [file]]
               [--ffmpeg [folder]] [--output [folder]] [--mode [... ...]] [--json [file]] [--no-title [id,id]]
               [--no-artist [id,id]] [--no-album [id,id]] [--no-cover [id,id]] [--no-lyrics [id,id]]

options:
  -h, --help           show this help message and exit
  --version, -v        show program's version number and exit
  --update, -u         check for update and exit

General options:
  --config [file]      absolute path to config file containing sector 'ytm-yld'
  --headers [file]     absolute path to file of YT headers
  --yt-dlp [file]      absolute path to yt-dlp bin
  --ffmpeg [folder]    absolute path to folder of ffmpeg and ffprobe bin
  --output [folder]    absolute path to folder where you want your music synced/download/playlist-to-text file
  --mode [... ...]     mode (t|d|s|m|j) to request for the application to complete
  --json [file]        absolute path to existing JSON playlist metadata file instead of downloading

Music options:
  For these, it can act as a global parameter for all songs if no specific IDs are passed.

  --no-title [id,id]   whether to include the title of the songs or not
  --no-artist [id,id]  whether to include the artist of the songs or not
  --no-album [id,id]   whether to include the album name of the songs or not
  --no-cover [id,id]   whether to include the album art/cover of the songs or not
  --no-lyrics [id,id]  whether to include the lyrics of the songs or not
```

**Make sure that the files within the output folder don't have names like ones used by this app, as they could be deleted.**

If you choose not to pass the arguments, you will have to enter the paths upon the application input request.

_([1.1.0+](https://github.com/pepershukov/ytm-yld/releases/tag/v1.1.0))_ **If the paths turn out to be invalid or non-existant, or the file formatting is wrong, ~the application will throw out an error~** _([6.0.0+](https://github.com/pepershukov/ytm-yld/releases/tag/v6.0.0))_ **the application will ask for them recursively until success.**

&nbsp;

## Quickstart
### Authentication (OAuth) _([9.0.0+](https://github.com/pepershukov/ytm-yld/releases/tag/v9.0.0))_
On first run, without the `--headers` arg, you will be asked to login. After that, the header is saved to the `output` folder and the headers can be used again until their expiry.

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
  - Does not delete the JSON metadata of the playlist - mainly for devs to debug/inspect
- **Manual (`m`)** _([4.0.0+](https://github.com/pepershukov/ytm-yld/releases/tag/v4.0.0))_
  - Gives a choice of songs to download to the user - therefore you have to input songs you want to download manually

### Config
You can pass the config file under the `--config` argument.

- The application uses an `.ini`-like format
- All the variables regarding the application have to be under sector `ytm-yld`
  - The application will throw an error and exit if this fails
- The values of the variables must not be empty
- Not all variables have to be passed
  - You still can pass the arguments if your need, straight to the executable

Here is an **example** of a **full config file**:
``` ini
[ytm-yld]
ffmpeg = absolute/path/to/ffmpeg
yt-dlp = absolute/path/to/yt_dlp.exe
headers = absolute/path/to/headers.json
output = absolute/path/to/output
mode = tdsjm
json = absolute/path/to/songs.json

# These options have two ways
# 1. Selecting 'true' - choosing it globally for all songs
# 2. Selecting IDs in a list - MUST put DOUBLE SPEECH-MARKS!!
no-title = ["1-iKwZKc7Ok"]
no-artist = ["1-iKwZKc7Ok", "FXovf5dsRTw"]
no-album = true
no-cover = TRUE
no-lyrics = True
```
