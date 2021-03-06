#!/usr/bin/python
# -*- coding: utf-8 -*-


# Imports
import mutagen.easyid3  # working with audio files
import PIL.Image
import mutagen.mp3
import mutagen.id3
import glob  # working with files + core
import os
import main
import yt_dlp
import itertools
import platform


# Song processing
def process_songs(max_song_num):
    counter = 1
    for (full_mp3_file, remote_song) in \
        itertools.product(glob.glob('{}/*.mp3'.format(main.path_temp)),
                        main.json_data['entries']):  # parse through mp3 files and playlist metadata
        if remote_song:  # checks for song validity on YouTube
            if '{}\\{}.mp3'.format(main.path_temp, remote_song['id']) == full_mp3_file \
                or '{}/{}.mp3'.format(main.path_temp, remote_song['id']) == full_mp3_file:  # if data matches-
                main.logwrite('Opening #{} thumbnail...'.format(counter))
                image = PIL.Image.open('{}/{}.webp'.format(main.path_temp,
                                    remote_song['id'])).convert('RGB')
                main.logwrite('Cropping #{} thumbnail...'.format(counter))
                image = image.crop((280, 0, 1000, 720))
                main.logwrite('Saving #{} thumbnail...'.format(counter))
                image.save('{}/{}.jpg'.format(main.path_temp,
                        remote_song['id']), 'jpeg')

                main.logwrite('Opening #{} song...'.format(counter))
                local_song = mutagen.easyid3.EasyID3(full_mp3_file)
                main.logwrite('Setting #{} MP3 metadata title...'.format(counter))
                local_song['title'] = remote_song['title']
                if 'creator' in remote_song.keys():
                    main.logwrite('Setting #{} MP3 metadata artist...'.format(counter))
                    local_song['artist'] = remote_song['creator'].split(', ')
                    main.logwrite('Setting #{} MP3 metadata author...'.format(counter))
                    local_song['author'] = remote_song['creator'].split(', ')
                else:
                    main.logwrite('Creator not found - setting #{} MP3 metadata artist and author...'.format(counter))
                    (local_song['artist'], local_song['author']) = ('', '')
                if 'album' in remote_song.keys():
                    main.logwrite('Setting #{} MP3 metadata album name...'.format(counter))
                    local_song['album'] = remote_song['album']
                else:
                    main.logwrite('Album not found - setting #{} MP3 metadata album name...'.format(counter))
                    local_song['album'] = ''
                main.logwrite('Saving #{} MP3...'.format(counter))
                local_song.save()

                main.logwrite('Opening #{} MP3\'s metadata...'.format(counter))
                local_song = mutagen.mp3.MP3(full_mp3_file,
                        ID3=mutagen.id3.ID3)
                main.logwrite('Adding album art to #{} MP3 metadata...'.format(counter))
                local_song.tags.add(mutagen.id3.APIC(mime='image/jpeg',
                                    type=3, desc=u'Cover',
                                    data=open('{}/{}.jpg'.format(main.path_temp,
                                    remote_song['id']), 'rb').read()))
                main.logwrite('Saving #{} MP3...'.format(counter))
                local_song.save()

                main.logwrite('Moving #{} ({}) song to "{}"...'.format(counter,
                            remote_song['title'], main.path_song))
                try:
                    os.rename(full_mp3_file, '{}/{}.mp3'.format(main.path_song,
                        remote_song['title']))
                except OSError: # if there are unallowed characters in the name
                    remove_char = '\\/:"?*<>|'
                    title_list = list(remote_song['title'])
                    for title_index, char in itertools.product(range(len(title_list)), remove_char):
                        if title_list[title_index] == char:
                            title_list[title_index] = '-'
                    new_title = ''
                    for char in title_list:
                        new_title += char
                    os.rename(full_mp3_file, '{}/{}.mp3'.format(main.path_song,
                        new_title))
                
                main.logwrite('Converted song #{}/{}.'.format(counter,
                            max_song_num))
                counter += 1

    main.logwrite("Changing current working directory to '{}'".format(main.path_main))
    os.chdir(main.path_main)
    for temp_file in os.listdir(main.path_temp):
        main.logwrite('Removing "{}/{}"...'.format(main.path_temp,
                    temp_file))
        os.remove('{}/{}'.format(main.path_temp, temp_file))
    main.logwrite('Removing "{}"...'.format(main.path_temp))
    os.rmdir(main.path_temp)


def download_songs(manual = False, playlist_items = ''):
    # Preparing for download
    # checking for FFmpeg validity
    continue_ok = True
    if platform.system() == 'Windows':
        if os.path.exists(main.path_ffmpeg) and \
            os.path.exists('{}/ffmpeg.exe'.format(main.path_ffmpeg)):  # checks for FFmpeg binaries existence passed from arguments
            path_ffmpeg = main.path_ffmpeg  # if valid, assign it to path_ffmpeg_
        else:
            main.errorwrite("'FFmpeg/bin' folder is invalid, non-existing or does not contain binaries of FFmpeg.", 1
                            ) # if not valid, continue for the user to correct the mistake
            path_ffmpeg = input('[INPUT] Enter the absolute path to \'FFmpeg/bin\' folder: '
                                ) # ask the user for FFmpeg binaries if they are not found
            if not (os.path.exists(path_ffmpeg) and \
                os.path.exists('{}/ffmpeg.exe'.format(path_ffmpeg))):  # checks for FFmpeg binaries validity given by the user
                main.errorwrite("'FFmpeg/bin' folder is invalid, non-existing or does not contain binaries of FFmpeg.", 1
                                ) # if not valid after both tries, try to exit later
                continue_ok = False
    elif platform.system() == 'Linux':
        if os.path.exists(main.path_ffmpeg): # check if FFmpeg binary exists from arguments
            path_ffmpeg = main.path_ffmpeg # if valid, assign to path_ffmpeg_
        else:
            main.errorwrite("'FFmpeg' folder is non-existant.", 1
                            ) # if not valid, continue for the user to correct the mistake
            path_ffmpeg = input('[INPUT] Enter the absolute path to \'FFmpeg\' binary: '
                                ) # ask the user for an FFmpeg binary
            if not os.path.exists(path_ffmpeg): # check the FFmpeg binary for existance given by the user
                main.errorwrite("'FFmpeg' binary is non-existant.", 1) # if not valid after both tries try to exit later
                continue_ok = False
                
    # cleaning the temporary files if present
    try:
        for temp_file in os.listdir(main.path_temp):
            main.logwrite('Removing "{}/{}"...'.format(main.path_temp,
                        temp_file))
            os.remove('{}/{}'.format(main.path_temp, temp_file))
        main.logwrite('Removing "{}"...'.format(main.path_temp))
        os.rmdir(main.path_temp)
    except:
        main.errorwrite("Couldn't remove the temporary directory. Continuing...", 1
                        )

    if continue_ok: # if FFmpeg binary exists, continue with downloading
        main.logwrite('Making "{}"...'.format(main.path_temp))
        os.makedirs(main.path_temp, exist_ok=True) # download folder

        main.logwrite('Changing current working directory to "{}"...'.format(main.path_temp))
        os.chdir(main.path_temp)


        # Downloader
        if not manual:
            if not glob.glob('{}/*.mp3'.format(main.path_song)):  # if no songs are present locally
                max_song_num = len(main.json_data['entries'])
                main.logwrite('Downloading all ({}) songs...'.format(len(main.json_data['entries'
                            ])))

                # os.system(yt-dlp --cookies="{}" --write-thumbnail -x --audio-format=mp3 --audio-quality=0 --ffmpeg-location="{}" --output="%(id)s.mp3" -- https://music.youtube.com/playlist?list=LM'.format(main.path_temp, main.path_cookie, path_ffmpeg))
                with yt_dlp.YoutubeDL({
                    'ignoreerrors': True,
                    'cookiefile': main.path_cookie,
                    'nowarnings': True,
                    'writethumbnail': True,
                    'ffmpeg_location': path_ffmpeg,
                    'outtmpl': '%(id)s',
                    'postprocessors': [{'key': 'FFmpegExtractAudio',
                                    'preferredcodec': 'mp3'}],
                    }) as ydl:
                    ydl.download('https://music.youtube.com/playlist?list=LM')  # downloading handler
                process_songs(max_song_num)

            else: # if some songs are present, udgrade to find more
                # os.system(yt-dlp --cookies="{}" --playlist-end={} --write-thumbnail -x --audio-format=mp3 --audio-quality=0 --ffmpeg-location="{}" --output="%(id)s.mp3" -- https://music.youtube.com/playlist?list=LM'.format(main.path_temp, main.path_cookie, input('Enter # of last song to download: '), main.path_ffmpeg))

                # find how many songs needed to download more...
                for (max_song_num, full_mp3_file) in \
                    itertools.product(range(len(main.json_data['entries'])),
                                    glob.glob('{}/*.mp3'.format(main.path_song))):  # iterate through (length of playlist, songs stored locally)
                    if main.json_data['entries'][max_song_num]:  # check for song validity on YouTube.com
                        local_song = mutagen.easyid3.EasyID3(full_mp3_file)  # open mp3 file metadata
                        data_song = main.json_data['entries'][max_song_num]  # open YouTube file metadata

                        # if the metadata is identical, cap max_song_num by breaking loop
                        if 'creator' and 'album' in data_song.keys():
                            if local_song['title'][0] == data_song['title'] \
                                and local_song['artist'] == local_song['author'] \
                                == data_song['creator'].split(', ') \
                                and local_song['album'][0] == data_song['album']:
                                break
                        else:
                            if local_song['title'][0] == data_song['title'] \
                                and local_song['artist'] == local_song['author'] \
                                == '' and local_song['album'][0] \
                                == data_song['album']:
                                break
                
                if max_song_num == 0:  # if there are no new songs to download, exit applciation
                    main.logwrite('Changing current working directory to "{}"...'.format(main.path_main))
                    os.chdir(main.path_main)
                    main.logwrite('Removing "{}"...'.format(main.path_temp))
                    os.rmdir(main.path_temp)
                    main.logwrite('Removing "{}"...'.format(main.path_json))
                    os.remove(main.path_json)
                    main.errorwrite('No songs to download.', 1)
                else:
                    main.logwrite('Downloading {} songs...'.format(max_song_num))
                    # os.system(yt-dlp --cookies="{}" --playlist-end={} --write-thumbnail -x --audio-format=mp3 --audio-quality=0 --ffmpeg-location="{}" --output="%(id)s.mp3" -- https://music.youtube.com/playlist?list=LM'.format(main.path_temp, main.path_cookie, max_song_num, path_ffmpeg))
                    with yt_dlp.YoutubeDL({
                        'playlistend': max_song_num,
                        'ignoreerrors': True,
                        'cookiefile': main.path_cookie,
                        'nowarnings': True,
                        'writethumbnail': True,
                        'ffmpeg_location': path_ffmpeg,
                        'outtmpl': '%(id)s',
                        'postprocessors': [{'key': 'FFmpegExtractAudio',
                                        'preferredcodec': 'mp3'}],
                        }) as ydl:
                        ydl.download('https://music.youtube.com/playlist?list=LM')  # download handler
                    process_songs(max_song_num)

        else: # if called by the playlist_manual module
            max_song_num = 0
            for nums in playlist_items.split(','):
                if '-' in nums:
                    max_song_num += (int(nums.split('-')[1]) - int(nums.split('-')[0]) + 1)
                else:
                    max_song_num += 1

            main.logwrite('Downloading {} songs...'.format(max_song_num))
            with yt_dlp.YoutubeDL({
                        'playlist_items': playlist_items,
                        'ignoreerrors': True,
                        'cookiefile': main.path_cookie,
                        'nowarnings': True,
                        'writethumbnail': True,
                        'ffmpeg_location': path_ffmpeg,
                        'outtmpl': '%(id)s',
                        'postprocessors': [{'key': 'FFmpegExtractAudio',
                                        'preferredcodec': 'mp3'}],
                        }) as ydl:
                        ydl.download('https://music.youtube.com/playlist?list=LM')  # download handler
            process_songs(max_song_num)
    
    else: # if FFmpeg binary is not found
        main.errorwrite('Cannot continue downloading as FFmpeg binary is non existant.', 1)