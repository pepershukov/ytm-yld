#!/usr/bin/python
# -*- coding: utf-8 -*-


# Imports
import datetime
import os
import sys
import yt_dlp
import json
import codecs
import platform
import configparser
import logging
import tempfile
import signal
import shutil


if (platform.system() != 'Linux') and (platform.system() != 'Windows'):
    raise Exception("""Your system is not supported.
Please report this message with your system details via an Issue on the project\'s GitHub page, and possible I will try to bundle an app for it:
https://github.com/pepershukov/ytm-yld/issues""")

if '--help' in sys.argv or '-h' in sys.argv: # print help message and exit
    if platform.system() == 'Windows':
        print("""ytm-yld_windows.exe (--help|-h) [--cookie <path>] (--output <folder path>) (--mode ...) (--json <path>) (--config <path>)

[...] - required arguments
(...) - optional arguments
Further information on requirements can be found in the README.md.
https://github.com/pepershukov/ytm-yld#readme

If the following arguments are not passed, the application will request them when necessary.
And if they fail to validate within the app, the application will throw an error.
Arguments:
    --help | -h     - shows this message and exits

    --cookie        - the absolute path to file of a YouTube.com cookie as a 'Netscape HTTP Cookie File'
    
    --output        - the absolute path to folder where you want your music(synced/downloaded)/playlist-to-text file
    
    --mode          - mode (t|d|s|m|j) to request for the application to complete

    --json          - the absolute path to an existing JSON playlist data file instead of downloading

    --config        - the absolute path to the config file containing section `ytm-yld`
                    - see https://github.com/pepershukov/ytm-yld#config for quickstart""")
    elif platform.system() == 'Linux':
        print("""ytm-yld_linux (--help|-h) [--cookie <path>] (--ffmpeg <path>) (--output <folder path>) (--mode ...) (--json <path>) (--config <path>)

[...] - required arguments
(...) - optional arguments
Further information on requirements can be found in the README.md.
https://github.com/pepershukov/ytm-yld#readme

If the following arguments are not passed, the application will request them when necessary.
And if they fail to validate within the app, the application will throw an error.
Arguments:
    --help | -h     - shows this message and exits

    --cookie        - the absolute path to file of a YouTube.com cookie as a 'Netscape HTTP Cookie File'

    --ffmpeg        - the absolute path to FFmpeg file binary
                    - only necessary if you are to select 'd' mode

    --output        - the absolute path to folder where you want your music(synced/downloaded)/playlist-to-text file

    --mode          - mode (t|d|s|m|j) to request for the application to complete

    --json          - the absolute path to an existing JSON playlist data file instead of downloading

    --config        - the absolute path to the config file containing section `ytm-yld`
                    - see https://github.com/pepershukov/ytm-yld#config for quickstart""")
    sys.exit()


# Initialization
if __name__ == '__main__':
    # remove temp log file
    try:
        os.remove(f"{tempfile.gettempdir()}/ytm-yld.log.txt")
    except FileNotFoundError:
        pass

logger = logging.getLogger() # ininitiate logging
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("[%(datetime)s] [%(levelname)s] [%(module)s %(lineno)d] %(message)s")
old_factory = logging.getLogRecordFactory()
def record_factory(*args, **kwargs):
    record = old_factory(*args, **kwargs)
    record.datetime = str(datetime.datetime.now())
    return record
logging.setLogRecordFactory(record_factory)

fh = logging.FileHandler(f"{tempfile.gettempdir()}/ytm-yld.log.txt") # add handler to file
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)
sh = logging.StreamHandler() # add handler to STDOUT
sh.setLevel(logging.DEBUG)
sh.setFormatter(formatter)
logger.addHandler(sh)

# Paths
if '--config' in sys.argv:
    logging.debug('Looking into a config file...')
    config = configparser.ConfigParser()
    config.read(sys.argv[sys.argv.index('--config') + 1])
    config = config['ytm-yld']

    logging.debug("Looking into the 'output' parameter...")
    if 'output' in config:
        logging.debug("Setting the 'output' variable... (config)")
        path_song = config['output']
        path_temp = f"{config['output']}/temp"
    else:
        path_song = ''
        path_temp = ''

    logging.debug("Looking into the 'json' parameter...")
    if 'json' in config:
        logging.debug("Setting the 'json' variable... (config)")
        path_json = config['json']
        sys.argv.append('--json')
    else:
        path_json = ''

    logging.debug("Looking into the 'ffmpeg' parameter...")
    if 'ffmpeg' in config:
        logging.debug("Setting the 'ffmpeg' variable... (config)")
        path_ffmpeg = config['ffmpeg']
    else:
        path_ffmpeg = ''

    logging.debug("Looking into the 'cookie' parameter...")
    if 'cookie' in config:
        logging.debug("Setting the 'cookie' variable... (config)")
        path_cookie = config['cookie']
    else:
        path_cookie = ''

    logging.debug("Looking into the 'mode' parameter...")
    if 'mode' in config:
        logging.debug("Setting the 'mode' variable... (config)")
        mode = config['mode']
    else:
        mode = ''

else:
    path_song = ''
    path_temp = ''
    path_json = ''
    path_ffmpeg = ''
    path_cookie = ''
    mode = ''

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

path_main = os.path.abspath(os.path.dirname(__file__))
path_log = f"{tempfile.gettempdir()}/ytm-yld.log.txt"

logging.debug("Setting the 'ffmpeg' variable... (args)")
if platform.system() == 'Linux':
    if not path_ffmpeg:
        if '--ffmpeg' in sys.argv: # if FFmpeg folder passed in arguments
            path_ffmpeg = sys.argv[sys.argv.index('--ffmpeg') + 1]
        else:
            logging.warning('FFmpeg path not passed in args.') # if not passed, handle an error
elif platform.system() == 'Windows':
    path_ffmpeg = resource_path('ffmpeg/')

logging.debug("Setting the 'output' variable... (args)")
if not path_song:
    if '--output' in sys.argv: # if output folder passed in arguments
        # apply the output path passed in arguments to global variables
        path_song = sys.argv[sys.argv.index('--output') + 1]
        path_temp = f"{path_song}/temp"
    else: # otherwise, apply default paths
        path_song = f"{os.path.expanduser('~')}/Music/ytm-yld"
        path_temp = f"{os.path.expanduser('~')}/Music/ytm-yld/temp"

logging.debug("Setting the 'json' variable... (args)")
if not path_json:
    if '--json' in sys.argv: # if JSON playlist metadata passed in arguments
        path_json = sys.argv[sys.argv.index('--json') + 1]
    else:
        path_json = f"{path_song}/metadata.json"

logging.debug("Setting the 'cookie' variable... (args)")
if not path_cookie:
    if '--cookie' in sys.argv:
        path_cookie = sys.argv[sys.argv.index('--cookie') + 1]  # gets YouTube.com cookie path from arguments
while True:
    if os.path.isfile(path_cookie): # checks if cookie file is existing
        try:
            file = open(path_cookie, 'r')
        except:
            file = codecs.open(path_cookie, 'r', 'utf-16')
        data = file.readlines()[0]
        file.close()
        if not ('# Netscape HTTP Cookie File' in data \
                or '# HTTP Cookie File' in data): # checks for vaild formatting of a cookie file as depicted by yt-dlp
            logging.error("Invalid formatting of a YouTube.com cookie file. Look into 'requirements.txt' under 'YouTube cookie' for instructions.")
            logging.debug('Asking for new cookie path...')
            path_cookie = input('[INPUT] Enter the absolute path to YouTube.com "Netscape HTTP Cookie File":\n> ')
            continue
        else:
            break
    else:
        logging.error('Invalid or non-existant YouTube.com cookie file path.')
        logging.debug('Asking for new cookie path...')
        path_cookie = input('[INPUT] Enter the absolute path to YouTube.com "Netscape HTTP Cookie File":\n> ')
        continue

# Exit handler
def exit_handler(signal=None, frame=None):
    logging.info('Interrupted. Cleaning up...')
    # cleaning temporary files
    logging.debug(f"Changing current working directory to '{path_main}'")
    os.chdir(path_main)
    logging.debug(f"Removing '{path_temp}'...")
    shutil.rmtree(path_temp, ignore_errors=True)

    # cleaning metadata.json
    if '--json' not in sys.argv:
        logging.debug(f"Removing '{path_json}'...")
        try:
            os.remove(path_json)
        except:
            pass
    
    os._exit(0)
signal.signal(signal.SIGINT, exit_handler)

# Main programm
if __name__ == '__main__':
    os.makedirs(path_song, exist_ok=True)
    logging.debug(f"Made \"{path_song}\".")

    logging.debug("Setting the 'mode' variable... (args)")
    if not mode:
        if '--mode' in sys.argv:
            mode = sys.argv[sys.argv.index('--mode') + 1]
    while not ('t' in mode or 'd' in mode or 's' in mode or 'm' in mode or 'j' in mode):
        logging.error(f"Unknown mode '{mode}' chosen. Please select from (t|d|s|m|j).")
        logging.debug('Asking for a new mode...')
        mode = input('[INPUT] playlist-to-text/donwload/sync/manual/json? (t|d|s|m|j):\n> ')

    logging.debug(f"Changing current working directory to '{path_main}'...")
    os.chdir(path_main)
    logging.debug('Downloading a JSON metadata playlist file...')

    if '--json' not in sys.argv:
        with yt_dlp.YoutubeDL({
            'cookiefile': path_cookie,
            'no_warnings': True,
            'dump_single_json': True,
            'ignoreerrors': True,
            }) as ydl:
            try:
                with open(path_json, 'w') as file:
                    json.dump(ydl.sanitize_info(ydl.extract_info('https://music.youtube.com/playlist?list=LM', download=False)), file)  # writing playlist data to JSON file
            except:
                with codecs.open(path_json, 'w', 'utf-16') as file:
                    json.dump(ydl.sanitize_info(ydl.extract_info('https://music.youtube.com/playlist?list=LM', download=False)), file)

logging.debug('Opening a JSON metadata playlist file...')
try:
    with open(path_json, 'r') as file:
        logging.debug('Loading dictionary from JSON file...')
        json_data = json.load(file)
except:
    with codecs.open(path_json, 'r', 'utf-16') as file:
        logging.debug('Loading dictionary from JSON file...')
        json_data = json.load(file)
json_data = json_data['entries']
songs_data = {i['id']:i for i in json_data if i}

if __name__ == '__main__':
    if 't' in mode:
        import playlist_to_text
    if 's' in mode:
        import playlist_sync
        playlist_sync.sync()
    if json_data: # check if there are liked songs
        if 'm' in mode and 'd' in mode:
            logging.info("Cannot execute 'download' mode - 'manual' mode chosen also.")
            import playlist_manual
        else:
            if 'd' in mode:
                import playlist_downloader
                playlist_downloader.download_songs()
            if 'm' in mode:
                import playlist_manual
    else:
        logging.warning("No songs to download.")
    if 'j' not in mode:
        logging.debug(f"Removing '{path_json}'...")
        try:
            os.remove(path_json)
        except:
            pass

    print('\n')
    logging.info('Execution finished.')
    logging.info(f"The log file is at '{path_log}'.")

    if 'j' in mode:
        logging.info(f"Your playlist metadata as a JSON formatted file is available in '{path_json}'.")
    if 't' in mode:
        logging.info(f"Your parsed playlist information is available in '{path_song}/songs_info.txt'.")
    if json_data: # check if there are liked songs
        if 's' in mode:
            logging.info(f"Your songs have been synchronised in '{path_song}'.")
        if 'm' in mode or 'd' in mode:
            logging.info(f"Your downloaded songs are available in '{path_song}'.")
