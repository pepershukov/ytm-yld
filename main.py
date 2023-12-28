import datetime
import os
import json
import codecs
import configparser
import logging
import tempfile
import signal
import shutil
import time
import inspect
import argparse
import ytmusicapi
import requests
import subprocess

version = 'v9.0.0'
start = time.perf_counter() # time variable for benchmarking


argparser = argparse.ArgumentParser(prog='ytm-yld',
                                    description="A command-line downloader of YouTube Music - 'Your Likes' playlist",
                                    epilog="If some fail to validate, the application will recursively ask for them until success.",
                                    add_help=True,
                                    allow_abbrev=False)
argparser.add_argument('--version', '-v', action='version', version=version)
argparser.add_argument('--update', '-u', action='store_const', const=True, dest="update", help='check for update and exit')

general_group = argparser.add_argument_group("General options")
general_group.add_argument('--config', action='store', nargs='?', default='', type=str, metavar='file', dest='path_config', help="absolute path to config file containing sector 'ytm-yld'")
general_group.add_argument('--headers', action='store', nargs='?', default='', type=str, metavar='file', dest='path_headers', help="absolute path to file of YT headers")
general_group.add_argument('--yt-dlp', action='store', nargs='?', default='', type=str, metavar='file', dest='path_yt_dlp', help="absolute path to yt-dlp bin")
general_group.add_argument('--ffmpeg', action='store', nargs='?', default='', type=str, metavar='folder', dest='path_ffmpeg', help="absolute path to folder of ffmpeg and ffprobe bin")
general_group.add_argument('--output', action='store', nargs='?', default='', type=str, metavar='folder', dest='path_song', help="absolute path to folder where you want your music synced/download/playlist-to-text file")
general_group.add_argument('--mode', action='store', nargs='*', choices=['t', 'd', 's', 'm', 'j'], default='', type=str, metavar='...', dest='mode', help="mode (t|d|s|m|j) to request for the application to complete")
general_group.add_argument('--json', action='store', nargs='?', default='', type=str, metavar='file', dest='path_json', help="absolute path to existing JSON playlist metadata file instead of downloading")

music_group = argparser.add_argument_group("Music options", "For these, it can act as a global parameter for all songs if no specific IDs are passed.")
music_group.add_argument('--no-title', action='store', nargs='?', type=str, const="true", default="", metavar='id,id', dest='no_title', help="whether to include the title of the songs or not")
music_group.add_argument('--no-artist', action='store', nargs='?', type=str, const="true", default="", metavar='id,id', dest='no_artist', help="whether to include the artist of the songs or not")
music_group.add_argument('--no-album', action='store', nargs='?', type=str, const="true", default="", metavar='id,id', dest='no_album', help="whether to include the album name of the songs or not")
music_group.add_argument('--no-cover', action='store', nargs='?', type=str, const="true", default="", metavar='id,id', dest='no_cover', help="whether to include the album art/cover of the songs or not")
music_group.add_argument('--no-lyrics', action='store', nargs='?', type=str, const="true", default="", metavar='id,id', dest='no_lyrics', help="whether to include the lyrics of the songs or not")


def exit_handler(signal=None, frame=None):
    logging.info('Interrupted. Cleaning up...')
    try:
        logging.debug(f"Removing [{path_temp}]...")
        shutil.rmtree(path_temp, ignore_errors=True)
    except:
        pass
    
    if 'j' not in mode:
        logging.debug(f"Removing [{path_json}]...")
        try:
            os.remove(path_json)
        except:
            pass
    
    logging.info(f'Execution time: {time.perf_counter() - start} seconds')
    os._exit(0)
signal.signal(signal.SIGINT, exit_handler) # start exit_handler

def execute(cmd, **kwargs):
    cwd = kwargs['cwd'] if 'cwd' in kwargs else None
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True, cwd=cwd)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line 
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

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
    sh.setLevel(logging.INFO)
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
    logging.debug("Checking for updates...")
    latest_version = requests.get("https://api.github.com/repos/pepershukov/ytm-yld/releases/latest").json()['tag_name']
    if latest_version != version:
        logging.info(f"An update is available [{version} -> {latest_version}]. You can look at the latest release and download here:\nhttps://github.com/pepershukov/ytm-yld/releases/latest")
    else:
        logging.info(f"You are running the latest version [{version}].")
    os._exit(0)

path_config = args.path_config
if path_config:
    logging.debug('Reading the config file...')
    config = configparser.ConfigParser()
    config.read(path_config)
    config = config['ytm-yld']
else:
    config = {}
logging.info("Setting paths and variables...")
logging.debug("Setting [yt-dlp] variable...")
path_yt_dlp = config['yt-dlp'] if 'yt-dlp' in config and args.path_yt_dlp == '' else args.path_yt_dlp
logging.debug("Setting [ffmpeg] variable...")
path_ffmpeg = config['ffmpeg'] if 'ffmpeg' in config and args.path_ffmpeg == '' else args.path_ffmpeg
logging.debug("Setting [headers] variable...")
path_headers = config['headers'] if 'headers' in config and args.path_headers == '' else args.path_headers
logging.debug("Setting [output] variable...")
path_song = config['output'] if 'output' in config and args.path_song == '' else args.path_song
logging.debug("Setting [json] variable...")
path_json = config['json'] if 'json' in config and args.path_json == '' else args.path_json
logging.debug("Setting [mode] variable...")
mode = config['mode'] if 'mode' in config and args.mode == '' else args.mode
logging.debug("Setting [no-title] variable...")
no_title = (str(config['no-title']).lower() if config['no-title'].lower() == 'true' else json.loads(config['no-title'])) if 'no-title' in config and args.no_title.split(',') == [''] else args.no_title.split(',')
logging.debug("Setting [no-artist] variable...")
no_artist = (str(config['no-artist']).lower() if config['no-artist'].lower() == 'true' else json.loads(config['no-artist'])) if 'no-artist' in config and args.no_artist.split(',') == [''] else args.no_artist.split(',')
logging.debug("Setting [no-album] variable...")
no_album = (str(config['no-album']).lower() if config['no-album'].lower() == 'true' else json.loads(config['no-album'])) if 'no-album' in config and args.no_album.split(',') == [''] else args.no_album.split(',')
logging.debug("Setting [no-cover] variable...")
no_cover = (str(config['no-cover']).lower() if config['no-cover'].lower() == 'true' else json.loads(config['no-cover'])) if 'no-cover' in config and args.no_cover.split(',') == [''] else args.no_cover.split(',')
logging.debug("Setting [no-lyrics] variable...")
no_lyrics = (str(config['no-lyrics']).lower() if config['no-lyrics'].lower() == 'true' else json.loads(config['no-lyrics'])) if 'no-lyrics' in config and args.no_lyrics.split(',') == [''] else args.no_lyrics.split(',')

logging.debug("Setting [main] variable...")
path_main = os.path.abspath(os.path.dirname(__file__))
logging.debug("Setting [log] variable...")
path_log = f"{tempfile.gettempdir()}/ytm-yld.log.txt"

if path_headers:
    logging.debug("Validating [header] variable...")
    while not os.path.isfile(path_headers):
        logging.error("Invalid or non-existant headers file.")
        path_headers = loginput("Enter the absolute path to a YT headers file")

if not path_song:
    logging.debug("Setting [output] variable...")
    path_song = f"{os.path.expanduser('~')}/Music/ytm-yld"
    logging.debug("Setting [temp] variable...")
    path_temp = f"{os.path.expanduser('~')}/Music/ytm-yld/temp"
else:
    logging.debug("Validating [output] variable...")
    while not os.path.isdir(path_song):
        logging.error("Invalid or non-existant [output] folder.")
        path_song = loginput("Enter the absolute path to an [output] folder")
    logging.debug("Setting [temp] variable...")
    path_temp = f"{path_song}/temp"

if not path_json:
    json_arg = False
    logging.debug("Setting [json] variable...")
    path_json = f"{path_song}/songs.json"
else:
    logging.debug("Validating [json] variable...")
    while not os.path.isfile(path_json):
        logging.error("Invalid or non-existant JSON songs file.")
        path_json = loginput("Enter the absolute path to a JSON songs file")
    json_arg = True

def song_options(song_id):
    options = {}
    logging.debug(f"Loading [{song_id}] options...")
    options['no-title'] = True if song_id in no_title or "true" in no_title else False
    options['no-artist'] = True if song_id in no_artist or "true" in no_artist else False
    options['no-album'] = True if song_id in no_album or "true" in no_album else False
    options['no-cover'] = True if song_id in no_cover or "true" in no_cover else False
    options['no-lyrics'] = True if song_id in no_lyrics or "true" in no_lyrics else False
    logging.debug(options)
    return options


# Main programm
if __name__ == '__main__':
    logging.debug("Making [output] folder...")
    os.makedirs(path_song, exist_ok=True)

    logging.debug("Validating [mode] variable... (args)")
    while not ('t' in mode or 'd' in mode or 's' in mode or 'm' in mode or 'j' in mode):
        if len(mode) != 0:
            logging.error(f"Unknown mode [{mode}] chosen. Please select from [t|d|s|m|j].")
        else:
            logging.error(f"No mode chosen. Please select from [t|d|s|m|j].")
        mode = loginput('playlist-to-text/donwload/sync/manual/json? [t|d|s|m|j]')
    
    if not json_arg:
        logging.info('Logging in...')
        if not path_headers:
            logging.debug("Setting [headers] variable...")
            path_headers = f"{path_song}/headers.json"
            logging.debug("Running OAuth...")
            ytmusicapi.setup_oauth(filepath=path_headers)
        
        ytmusic = ytmusicapi.YTMusic(path_headers)
        with codecs.open(path_json, 'w', 'utf-16') as file:
            logging.debug('Getting playlist data...')
            json.dump(ytmusic.get_liked_songs(limit=None), file)

logging.debug('Opening a JSON metadata playlist file...')
with codecs.open(path_json, 'r', 'utf-16') as file:
    logging.debug('Loading dictionary from JSON songs file...')
    json_data = json.load(file)
songs_data = {i['videoId'] : i for i in json_data['tracks'] if i}

if __name__ == '__main__':
    if 't' in mode:
        import playlist_to_text
        logging.info("Running [playlist_to_text]")
        playlist_to_text.write_file(playlist_to_text.generate_table())
        logging.info("Finished [playlist_to_text]")
    if 's' in mode:
        import playlist_sync
        logging.info("Running [playlist_sync]")
        playlist_sync.sync()
        logging.info("Finished [playlist_sync]")
    if songs_data: # check if there are liked songs
        if 'm' in mode:
            import playlist_manual
            import playlist_downloader
            logging.debug("Running [playlist_manual]")
            playlist_downloader.download_songs(playlist_manual.choose_songs())
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

    logging.info(f'Execution finished. Execution time: {time.perf_counter() - start} seconds')
    logging.info(f"The log file is at [{path_log}].")
    if 'j' in mode:
        logging.info(f"Your playlist metadata as a JSON formatted file is available in [{path_json}].")
    if 't' in mode:
        logging.info(f"Your parsed playlist information is available in [{path_song}/songs.txt].")       
    if songs_data: # check if there are liked songs
        if 's' in mode:
            logging.info(f"Your songs have been synchronised in [{path_song}].")
        if 'm' in mode or 'd' in mode:
            logging.info(f"Your downloaded songs are available in [{path_song}].")