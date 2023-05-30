#!/usr/bin/python
# -*- coding: utf-8 -*-


# Imports
import mutagen.easyid3 # working with audio files
import PIL.Image
import mutagen.mp3
import mutagen.id3
import glob # working with files + core
import os
import main
import yt_dlp
import shutil
import logging
import ytmusicapi
import ctypes
import platform


# Song processing
def process_songs(max_song_num):
    for counter, full_mp3_file in enumerate(glob.glob(f"{main.path_temp}/*.mp3"), start=1): # parse through mp3 files and playlist metadata
        song_id = full_mp3_file.rsplit(os.sep, 1)[1][:full_mp3_file.rsplit(os.sep, 1)[1].find('.mp3')]
        song_data = main.songs_data[song_id]
        logging.debug(f"Doing #{counter}/{max_song_num} [{song_id}]...")
        options = main.song_options(song_id)

        if not options['no-title'] or not options['no-artist'] or not options['no-lyrics']:
            remote_song_data = main.remote_songs_data[song_id]

        logging.debug("Opening song... [EasyID3]")
        song = mutagen.easyid3.EasyID3(full_mp3_file)

        if not options['no-title']:
            logging.debug("Setting MP3 metadata title...")
            song['title'] = remote_song_data['title']

        if not options['no-artist']:
            logging.debug("Setting MP3 metadata artist...")
            artists = []
            for i in remote_song_data['author'].strip().split(', '):
                for artist in i.strip().split(' & '):
                    artists.append(artist)
            song['artist'] = artists

        if not options['no-album']:
            if 'album' in song_data.keys():
                logging.debug("Setting MP3 metadata album name...")
                song['album'] = song_data['album']
            else:
                song['album'] = remote_song_data['title']
        
        logging.debug("Saving MP3...")
        song.save()

        if not options['no-cover']:
            logging.debug("Opening thumbnail...")
            image = PIL.Image.open(f'{main.path_temp}/{song_id}.webp').convert('RGB')
            logging.debug("Cropping thumbnail...")
            image = image.crop((280, 0, 1000, 720))
            logging.debug("Saving thumbnail...")
            image.save(f"{main.path_temp}/{song_id}.jpg", 'jpeg')
            logging.debug("Opening MP3 metadata... [MP3]")
            song = mutagen.mp3.MP3(full_mp3_file, ID3=mutagen.id3.ID3)
            logging.debug("Adding album art to MP3 metadata...")
            song.tags.add(mutagen.id3.APIC(mime='image/jpeg',
                                        type=3, desc=u'Cover',
                                        data=open(f"{main.path_temp}/{song_id}.jpg", 'rb').read()))
            logging.debug("Saving MP3...")
            song.save()

        if not options['no-lyrics']:
            logging.debug("Getting lyrics...")
            try:
                lyrics = ytmusicapi.YTMusic().get_lyrics(ytmusicapi.YTMusic().get_watch_playlist(song_id)['lyrics'])['lyrics']
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
                logging.debug("Opening MP3 metadata... [MP3]")
                song = mutagen.mp3.MP3(full_mp3_file, ID3=mutagen.id3.ID3)
                logging.debug("Adding lyrics to MP3 metadata...")
                song.tags.add(mutagen.id3.USLT(encoding=3, text=lyrics))
                song.tags.add(mutagen.id3.SYLT(encoding=3, text=[(lyrics, 0)]))
                logging.debug("Saving MP3...")
                song.save()

        logging.debug(f"Moving [{song_id}]...")
        try:
            os.rename(full_mp3_file, f"{main.path_song}/{song_id}.mp3")
        except FileExistsError:
            os.remove(f"{main.path_song}/{song_id}.mp3")
            os.rename(full_mp3_file, f"{main.path_song}/{song_id}.mp3")

    logging.debug(f"Changing current working directory to [{main.path_main}]...")
    os.chdir(main.path_main)
    logging.debug(f"Removing [{main.path_temp}]...")
    shutil.rmtree(main.path_temp, ignore_errors=True)


def download_songs(playlist_items = ''):
    # Preparing for download    
    # cleaning the temporary files if present
    logging.debug(f"Removing [{main.path_temp}]...")
    shutil.rmtree(main.path_temp, ignore_errors=True)
    logging.debug(f"Making [{main.path_temp}]...")
    os.makedirs(main.path_temp, exist_ok=True) # download folder
    logging.debug(f"Applying [hidden] to [{main.path_temp}] ...")
    if platform.system() == 'Windows':
        ctypes.windll.kernel32.SetFileAttributesW.argtypes = (ctypes.c_wchar_p, ctypes.c_uint32)
        ctypes.windll.kernel32.SetFileAttributesW(main.path_temp, 0x02)

    logging.debug(f"Changing current working directory to [{main.path_temp}]...")
    os.chdir(main.path_temp)

            
    # Downloader
    if not playlist_items:
        if not glob.glob(f"{main.path_song}/*.mp3"): # if no songs are present locally
            max_song_num = len(main.songs_data)
            logging.info(f"Downloading all [{len(main.songs_data)}] songs...")
            with yt_dlp.YoutubeDL({
                'extract_audio': True,
                'audio_format': 'mp3',
                'ignoreerrors': True,
                'cookiefile': main.path_cookie,
                'nowarnings': True,
                'writethumbnail': True,
                'ffmpeg_location': main.path_ffmpeg,
                'outtmpl': '%(id)s',
                'postprocessors': [{'key': 'FFmpegExtractAudio',
                                    'preferredcodec': 'mp3'}]}) as ydl:
                ydl.download('https://music.youtube.com/playlist?list=LM') # downloading handler
            process_songs(max_song_num)

        else: # if some songs are present, udgrade to find more
            logging.debug('Looking into which songs to download...')
            songs = [i.rsplit(os.sep, 1)[1][:i.rsplit(os.sep, 1)[1].find('.mp3')] for i in glob.glob(f"{main.path_song}/*.mp3")] # get all existing song ids
            downloadurls = [f"https://music.youtube.com/watch?v={id}" for id in main.songs_data if id not in songs]
            
            if len(downloadurls) == 0: # if there are no new songs to download, exit applciation
                logging.debug(f"Changing current working directory to [{main.path_main}]...")
                os.chdir(main.path_main)
                logging.debug(f"Removing [{main.path_temp}]...")
                shutil.rmtree(main.path_temp, ignore_errors=True)
                return

            else:
                logging.info(f"Downloading {len(downloadurls)} songs...")
                with yt_dlp.YoutubeDL({
                    'extract_audio': True,
                    'audio_format': 'mp3',
                    'ignoreerrors': True,
                    'cookiefile': main.path_cookie,
                    'nowarnings': True,
                    'writethumbnail': True,
                    'ffmpeg_location': main.path_ffmpeg,
                    'outtmpl': '%(id)s',
                    'postprocessors': [{'key': 'FFmpegExtractAudio',
                                        'preferredcodec': 'mp3'}]}) as ydl:
                    ydl.download(downloadurls) # download handler
                process_songs(len(downloadurls))

    else: # if called by the playlist_manual module
        max_song_num = 0
        for nums in playlist_items.split(','):
            if '-' in nums: # if it's # of songs from x to(-) y
                max_song_num += (int(nums.split('-')[1]) - int(nums.split('-')[0]) + 1) # find the amount of songs
            else:
                max_song_num += 1

        logging.info(f"Downloading {max_song_num} songs...")
        with yt_dlp.YoutubeDL({
                    'playlist_items': playlist_items,
                    'extract_audio': True,
                    'audio_format': 'mp3',
                    'ignoreerrors': True,
                    'cookiefile': main.path_cookie,
                    'nowarnings': True,
                    'writethumbnail': True,
                    'ffmpeg_location': main.path_ffmpeg,
                    'outtmpl': '%(id)s',
                    'postprocessors': [{'key': 'FFmpegExtractAudio',
                                    'preferredcodec': 'mp3'}]}) as ydl:
                    ydl.download('https://music.youtube.com/playlist?list=LM') # download handler
        process_songs(max_song_num)