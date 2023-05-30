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
import time
import inspect
import argparse
import ytmusicapi
import git

start = time.perf_counter() # time variable for benchmarking

if platform.system() != 'Windows':
    raise Exception("""Your system is not supported.
Please report this message with your system details via an Issue on the project\'s GitHub page, and possible I will try to bundle an app for it:
https://github.com/pepershukov/ytm-yld/issues""")



# Initialization
argparser = argparse.ArgumentParser(prog='ytm-yld',
                                    description="A command-line downloader of YouTube Music - 'Your Likes' playlist",
                                    epilog="If some fail to validate, the application will recursively ask for them until success.",
                                    add_help=True,
                                    allow_abbrev=False)
argparser.add_argument('--version', '-v', action='version', version='v8.0.1')
argparser.add_argument('--update', '-u', action='store_const', const=True, dest="update", help='check for update and exit')

general_group = argparser.add_argument_group("General options")
general_group.add_argument('--config', action='store', nargs='?', default='', type=str, metavar='file', dest='path_config', help="absolute path to config file containing sector 'ytm-yld'")
general_group.add_argument('--cookie', action='store', nargs='?', default='', type=str, metavar='file', dest='path_cookie', help="absolute path to YouTube.com cookie as a 'Netscape HTTP Cookie File'")
general_group.add_argument('--output', action='store', nargs='?', default='', type=str, metavar='folder', dest='path_song', help="absolute path to folder where you want your music synced/download/playlist-to-text file")
general_group.add_argument('--mode', action='store', nargs='*', choices=['t', 'd', 's', 'm', 'j'], default='', type=str, metavar='...', dest='mode', help="mode (t|d|s|m|j) to request for the application to complete")
general_group.add_argument('--json', action='store', nargs='?', default='', type=str, metavar='file', dest='path_json', help="absolute path to existing JSON playlist metadata file instead of downloading")
general_group.add_argument('--songs-json', action='store', nargs='?', default='', type=str, metavar='file', dest='path_songs_json', help="absolute path to existing JSON songs metadata file instead of downloading")

music_group = argparser.add_argument_group("Music metadata options", "For these, it can act as a global parameter for all songs if no specific IDs are passed.")
music_group.add_argument('--no-title', action='store', nargs='?', type=str, const="true", default="", metavar='id,id...', dest='no_title', help="whether to include the title of the songs or not")
music_group.add_argument('--no-artist', action='store', nargs='?', type=str, const="true", default="", metavar='id,id...', dest='no_artist', help="whether to include the artist of the songs or not")
music_group.add_argument('--no-album', action='store', nargs='?', type=str, const="true", default="", metavar='id,id...', dest='no_album', help="whether to include the album name of the songs or not")
music_group.add_argument('--no-cover', action='store', nargs='?', type=str, const="true", default="", metavar='id,id...', dest='no_cover', help="whether to include the album art/cover of the songs or not")
music_group.add_argument('--no-lyrics', action='store', nargs='?', type=str, const="true", default="", metavar='id,id...', dest='no_lyrics', help="whether to include the lyrics of the songs or not")


def exit_handler(signal=None, frame=None):
    logging.info('Interrupted. Cleaning up...')
    # cleaning temporary files
    try:
        logging.debug(f"Changing current working directory to [{path_main}]...")
        os.chdir(path_main)
        logging.debug(f"Removing [{path_temp}]...")
        shutil.rmtree(path_temp, ignore_errors=True)
    except:
        pass
    
    # cleaning metadata.json
    if 'j' not in mode:
        logging.debug(f"Removing [{path_json}]...")
        try:
            os.remove(path_json)
        except:
            pass
        logging.debug(f"Removing [{path_songs_json}]...")
        try:
            os.remove(path_songs_json)
        except:
            pass
    
    logging.debug(f'Execution time: {time.perf_counter() - start} seconds')
    os._exit(0)
signal.signal(signal.SIGINT, exit_handler) # start exit_handler


# Logging + custom input 
if __name__ == '__main__':
    # remove temp log file
    try:
        os.remove(f"{tempfile.gettempdir()}/ytm-yld.log.txt")
    except FileNotFoundError:
        pass

    logger = logging.getLogger() # main logger
    logger.propagate = False
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

def loginput(inputstr): # custom input log
    with open(f"{tempfile.gettempdir()}/ytm-yld.log.txt", 'a') as file:
        stack = inspect.stack()[1]
        record = f"[{datetime.datetime.now()}] [INPUT] [{str(inspect.getmodule(stack[0]).__name__).replace('_', '')} {stack[2]}] {inputstr}"
        result = input(f"{record}:\n> ")
        file.write(f"{record}\n[{datetime.datetime.now()}] [INPUT RECIEVED] [{str(inspect.getmodule(stack[0]).__name__).replace('_', '')} {stack[2]}] {result}\n")
        return result


logging.debug('Loading command-line arguments...')
args = argparser.parse_args()

if args.update == True:
    latest_version = git.cmd.Git().ls_remote('https://github.com/pepershukov/ytm-yld', sort='-v:refname', tags=True).split('\n')[0].split('/')[-1].replace('^{}', '')
    if latest_version != 'v8.0.1':
        logging.info(f"An update is available [v8.0.1 -> {latest_version}]. You can look at the latest release and download here:\nhttps://github.com/pepershukov/ytm-yld/releases/latest")
    else:
        logging.info("You are running the latest version.")
    os._exit(0)

logging.debug('Setting paths and variables...')
logging.debug("Setting [config] variable... (args)")
path_config = args.path_config
logging.debug("Setting [cookie] variable... (args)")
path_cookie = args.path_cookie
logging.debug("Setting [output] variable... (args)")
path_song = args.path_song
logging.debug("Setting [mode] variable... (args)")
mode = args.mode
logging.debug("Setting [json] variable... (args)")
path_json = args.path_json
logging.debug("Setting [songs-json] variable... (args)")
path_songs_json = args.path_songs_json
logging.debug("Setting [no-title] variable... (args)")
no_title = args.no_title.split(',')
logging.debug("Setting [no-artist] variable... (args)")
no_artist = args.no_artist.split(',')
logging.debug("Setting [no-album] variable... (args)")
no_album = args.no_album.split(',')
logging.debug("Setting [no-cover] variable... (args)")
no_cover = args.no_cover.split(',')
logging.debug("Setting [no-lyrics] variable... (args)")
no_lyrics = args.no_lyrics.split(',')
if path_config:
    logging.debug('Setting a config file...')
    config = configparser.ConfigParser()
    config.read(path_config)
    config = config['ytm-yld']
    for param in config.keys():
        if 'output' == param and path_song == '':
            logging.debug("Setting [output] variable... (config)")
            path_song = config['output']
        elif 'json' == param and path_json == '':
            logging.debug("Setting [json] variable... (config)")
            path_json = config['json']
        elif 'songs-json' == param and path_songs_json == '':
            logging.debug("Setting [songs-json] variable... (config)")
            path_songs_json = config['songs-json']
        elif 'cookie' == param and path_cookie == '':
            logging.debug("Setting [cookie] variable... (config)")
            path_cookie = config['cookie']
        elif 'mode' == param and mode == '':
            logging.debug("Setting [mode] variable... (config)")
            mode = config['mode']
        elif 'no-title' == param and no_title == ['']:
            logging.debug("Setting [no-title] variable... (config)")
            no_title = str(config['no-title']).lower() if config['no-title'].lower() == 'true' else json.loads(config['no-title'])
        elif 'no-artist' == param and no_artist == ['']:
            logging.debug("Setting [no-artist] variable... (config)")
            no_artist = str(config['no-artist']).lower() if config['no-artist'].lower() == 'true' else json.loads(config['no-artist'])
        elif 'no-album' == param and no_album == ['']:
            logging.debug("Setting [no-album] variable... (config)")
            no_album = str(config['no-album']).lower() if config['no-album'].lower() == 'true' else json.loads(config['no-album'])
        elif 'no-cover' == param and no_cover == ['']:
            logging.debug("Setting [no-cover] variable... (config)")
            no_cover = str(config['no-cover']).lower() if config['no-cover'].lower() == 'true' else json.loads(config['no-cover'])
        elif 'no-lyrics' == param and no_lyrics == ['']:
            logging.debug("Setting [no-lyrics] variable... (config)")
            no_lyrics = str(config['no-lyrics']).lower() if config['no-lyrics'].lower() == 'true' else json.loads(config['no-lyrics'])


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

path_main = os.path.abspath(os.path.dirname(__file__))
path_log = f"{tempfile.gettempdir()}/ytm-yld.log.txt"
if platform.system() == 'Windows':
    path_ffmpeg = resource_path('ffmpeg/')

if not path_song:
    path_song = f"{os.path.expanduser('~')}/Music/ytm-yld"
    path_temp = f"{os.path.expanduser('~')}/Music/ytm-yld/_temp"
else:
    logging.debug("Validating [output] variable...")
    while True:
        if not os.path.isdir(path_song):
            logging.error("Invalid or non-existant [output] folder.")
            loginput("Enter the absolute path to an [output] folder")
        else:
            break
    path_temp = f"{path_song}/_temp"

logging.debug("Validating [json] variable...")
if not path_json:
    json_arg = False
    path_json = f"{path_song}/metadata.json"
else:
    while True:
        if not os.path.isfile(path_json):
            logging.error("Invalid or non-existant JSON playlist metadata file.")
            path_json = loginput("Enter the absolute path to a JSON playlist metadata file")
        else:
            break
    json_arg = True

logging.debug("Validating [songs-json] variable...")
if not path_songs_json:
    songs_json_arg = False
    path_songs_json = f"{path_song}/songs_metadata.json"
else:
    while True:
        if not os.path.isfile(path_songs_json):
            logging.error("Invalid or non-existant JSON songs metadata file.")
            path_songs_json = loginput("Enter the absolute path to a JSON songs metadata file")
        else:
            break
    songs_json_arg = True

logging.debug("Validating [cookie] variable...")
while True:
    if not path_cookie:
        path_cookie = loginput('Enter the absolute path to YouTube.com "Netscape HTTP Cookie File"')
        continue
    
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
            path_cookie = loginput('Enter the absolute path to YouTube.com "Netscape HTTP Cookie File"')
            continue
        else:
            break
    else:
        logging.error('Invalid or non-existant YouTube.com cookie file path.')
        path_cookie = loginput('Enter the absolute path to YouTube.com "Netscape HTTP Cookie File"')
        continue

def song_options(song_id):
    options = {}
    options['no-title'] = True if song_id in no_title or "true" in no_title else False
    options['no-artist'] = True if song_id in no_artist or "true" in no_artist else False
    options['no-album'] = True if song_id in no_album or "true" in no_album else False
    options['no-cover'] = True if song_id in no_cover or "true" in no_cover else False
    options['no-lyrics'] = True if song_id in no_lyrics or "true" in no_lyrics else False
    return options



# Main programm
if __name__ == '__main__':
    os.makedirs(path_song, exist_ok=True)
    logging.debug(f"Made [{path_song}].")

    logging.debug("Validating [mode] variable... (args)")
    while not ('t' in mode or 'd' in mode or 's' in mode or 'm' in mode or 'j' in mode):
        if len(mode) != 0:
            logging.error(f"Unknown mode [{mode}] chosen. Please select from [t|d|s|m|j].")
        else:
            logging.error(f"No mode chosen. Please select from [t|d|s|m|j].")
        mode = loginput('playlist-to-text/donwload/sync/manual/json? [t|d|s|m|j]')

    logging.debug(f"Changing current working directory to [{path_main}]...")
    os.chdir(path_main)
    if not json_arg:
        logging.debug('Downloading a JSON metadata playlist file...')
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
        logging.debug('Loading dictionary from JSON playlist metadata file...')
        json_data = json.load(file)
except:
    with codecs.open(path_json, 'r', 'utf-16') as file:
        logging.debug('Loading dictionary from JSON playlist metadata file...')
        json_data = json.load(file)
songs_data = {i['id'] : i for i in json_data['entries'] if i}

if __name__ == '__main__':
    logging.debug("Downloading songs metadata...")
    if not songs_json_arg:
        remote_songs_data = {}
        for counter, song in enumerate(songs_data, start=1):
            logging.debug(f"Doing #{counter}/{len(songs_data)}...")
            remote_songs_data[song] = ytmusicapi.YTMusic().get_song(song)
        try:
            with open(path_songs_json, 'w') as file:
                json.dump(remote_songs_data, file)
        except:
            with codecs.open(path_songs_json, 'w', 'utf-16') as file:
                json.dump(remote_songs_data, file)

if __name__ != '__main__':
    logging.debug("Opening a JSON songs metadata file...")
    try:
        with open(path_songs_json, 'r') as file:
            logging.debug("Loading dictionary from JSON songs metadata file...")
            remote_songs_data = json.load(file)
    except:
        with codecs.open(path_songs_json, 'r', 'utf-16') as file:
            logging.debug("Loading dictionary from JSON songs metadata file...")
            remote_songs_data = json.load(file)
    remote_songs_data = {i : remote_songs_data[i]['videoDetails'] for i in remote_songs_data}


if __name__ == '__main__':
    if 't' in mode:
        import playlist_to_text
        playlist_to_text.write_file(playlist_to_text.generate_table())
    if 's' in mode:
        import playlist_sync
        playlist_sync.sync()
    if songs_data: # check if there are liked songs
        if 'm' in mode:
            import playlist_manual
            import playlist_downloader
            playlist_downloader.download_songs(playlist_items=playlist_manual.choose_songs())
        elif 'd' in mode:
                import playlist_downloader
                playlist_downloader.download_songs()
    else:
        logging.warning("No songs to download.")
    if 'j' not in mode:
        try:
            logging.debug(f"Removing [{path_json}]...")
            os.remove(path_json)
        except:
            pass
        try:
            logging.debug(f"Removing [{path_songs_json}]...")
            os.remove(path_songs_json)
        except:
            pass
    
    print('\n')
    logging.info(f'Execution finished. Execution time: {time.perf_counter() - start} seconds')
    logging.info(f"The log file is at [{path_log}].")
    if 'j' in mode:
        logging.info(f"Your playlist metadata as a JSON formatted file is available in [{path_json}].")
    if 't' in mode:
        logging.info(f"Your parsed playlist information is available in [{path_song}/songs_info.txt].")       
    if json_data: # check if there are liked songs
        if 's' in mode:
            logging.info(f"Your songs have been synchronised in [{path_song}].")
        if 'm' in mode or 'd' in mode:
            logging.info(f"Your downloaded songs are available in [{path_song}].")