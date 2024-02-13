import mutagen.easyid3 # working with audio files
import PIL.Image
import mutagen.mp3
import mutagen.id3
import glob # working with files + core
import os
import main
import shutil
import logging
import ytmusicapi


def process_songs(max_song_num):
    for counter, full_mp3_file in enumerate(glob.glob(f"{main.path_temp}/*.mp3"), start=1): # parse through mp3 files and playlist metadata
        song_id = full_mp3_file.rsplit(os.sep, 1)[1][:full_mp3_file.rsplit(os.sep, 1)[1].find('.mp3')]
        song = main.songs_data[song_id]
        logging.info(f"Doing #{counter}/{max_song_num} [{song_id}]...")
        options = main.song_options(song_id)

        logging.debug('Opening mp3... [EasyID3]')
        mp3_file = mutagen.easyid3.EasyID3(full_mp3_file)
        if not options['no-title']:
            logging.debug("Setting song title...")
            mp3_file['title'] = song['title']
        if not options['no-artist']:
            logging.debug("Setting song artists...")
            mp3_file['artist'] = [i['name'] for i in song['artists']]
        if not options['no-album']:
            logging.debug("Setting album name...")
            mp3_file['album'] = song['album']['name'] if song['album'] else song['title']
        logging.debug("Saving mp3...")
        mp3_file.save()

        if not options['no-cover']:
            logging.debug("Opening thumbnail...")
            image = PIL.Image.open(f'{main.path_temp}/{song_id}.webp').convert('RGB')
            logging.debug("Cropping thumbnail...")
            image = image.crop((280, 0, 1000, 720))
            logging.debug("Saving thumbnail...")
            image.save(f"{main.path_temp}/{song_id}.jpg", 'jpeg')
            logging.debug("Opening mp3... [ID3]")
            song = mutagen.mp3.MP3(full_mp3_file, ID3=mutagen.id3.ID3)
            logging.debug("Adding album cover...")
            song.tags.add(mutagen.id3.APIC(mime='image/jpeg',
                                        type=3, desc=u'Cover',
                                        data=open(f"{main.path_temp}/{song_id}.jpg", 'rb').read()))
            logging.debug("Saving mp3...")
            song.save()

        if not options['no-lyrics']:
            logging.debug("Getting lyrics...")
            try:
                lyrics = ytmusicapi.YTMusic().get_lyrics(ytmusicapi.YTMusic().get_watch_playlist(song_id, limit=1)['lyrics'])['lyrics']
            except:
                logging.debug("No lyrics available for the song.")
            else:
                for enc in ('utf8','iso-8859-1','iso-8859-15','cp1252','cp1251','latin1'):
                    try:
                        lyrics = lyrics.decode(enc)
                    except:
                        pass
                    else:
                        logging.debug(f"Found decoder [{enc}]")
                        break
                logging.debug("Opening mp3... [ID3]")
                song = mutagen.mp3.MP3(full_mp3_file, ID3=mutagen.id3.ID3)
                logging.debug("Adding lyrics...")
                song.tags.add(mutagen.id3.USLT(encoding=3, text=lyrics))
                logging.debug("Saving mp3...")
                song.save()

        try:
            os.remove(f"{main.path_song}/{song_id}.mp3")
            logging.debug(f"Removed [{main.path_song}/{song_id}.mp3]")
        except:
            pass
        logging.debug('Moving song...')
        os.rename(full_mp3_file, f"{main.path_song}/{song_id}.mp3")
    
    logging.debug(f"Removing [{main.path_temp}]...")
    shutil.rmtree(main.path_temp, ignore_errors=True)
    logging.info("Finished [playlist_downloader]")


def download_songs(downloadurls = None):
    if downloadurls:
        logging.info("Finished [playlist_manual]")
    logging.info("Running [playlist_downloader]")

    # Preparing for download
    path_ffmpeg = main.path_ffmpeg
    logging.debug("Validating [ffmpeg] variable...")
    while not os.path.isdir(path_ffmpeg):
        logging.error("Absent, invalid or non-existant [ffmpeg] folder.")
        path_ffmpeg = main.loginput('Enter the absolute path to a ffmpeg bin folder')

    path_yt_dlp = main.path_yt_dlp
    logging.debug("Validating [yt-dlp] variable...")
    while not os.path.isfile(main.path_yt_dlp):
        logging.error("Absent, invalid or non-existant [yt-dlp] bin.")
        path_yt_dlp = main.loginput('Enter the absolute path to a yt-dlp bin file')
    
    # cleaning the temporary files if present
    logging.debug(f"Removing [{main.path_temp}]...")
    shutil.rmtree(main.path_temp, ignore_errors=True)
    logging.debug(f"Making [{main.path_temp}]...")
    os.makedirs(main.path_temp, exist_ok=True) # download folder
            
    # Downloader
    if not downloadurls:
        if not glob.glob(f"{main.path_song}/*.mp3"): # if no songs are present locally
            logging.info("Downloading all songs.")
            logging.debug("Getting URLs of songs...")
            ids = list(main.songs_data.keys())
            downloadurls = [f"https://music.youtube.com/watch?v={id}" for id in main.songs_data]

        else: # if some songs are present, udgrade to find more
            logging.info('Looking into which songs to download...')
            songs = [i.rsplit(os.sep, 1)[1][:i.rsplit(os.sep, 1)[1].find('.mp3')] for i in glob.glob(f"{main.path_song}/*.mp3")] # get all existing song ids
            logging.debug("Getting song IDs to download...")
            ids = [id for id in main.songs_data if id not in songs]
            logging.debug("Getting URLs to download...")
            downloadurls = [f"https://music.youtube.com/watch?v={id}" for id in ids]
            if len(ids) == 0:
                logging.info('No songs to download.')
                logging.debug(f"Removing [{main.path_temp}]...")
                shutil.rmtree(main.path_temp, ignore_errors=True)
                return
    
    logging.debug("Checking for updates... [yt-dlp]")
    for stdout in main.execute([path_yt_dlp, '-U']):
        print(stdout, end='')
    logging.info(f"Downloading {len(ids)} songs...\n{ids}")
    for stdout in main.execute([path_yt_dlp, '-i', '--write-thumbnail', '--no-warnings', '-x',
                           '--audio-format', 'mp3',
                           '--audio-quality', '0',
                           '--ffmpeg-location', path_ffmpeg,
                           '-f', 'ba*',
                           '-o', '%(id)s',
                           '--', *downloadurls], cwd=main.path_temp):
        print(stdout, end='')
    process_songs(len(downloadurls))