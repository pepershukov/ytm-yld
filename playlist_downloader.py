#!/usr/bin/python
# -*- coding: utf-8 -*-
import mutagen.easyid3  # working with audio files
import PIL.Image
import mutagen.mp3
import mutagen.id3
import glob  # working with files + core
import os
import main
import sys
import yt_dlp

if os.path.isdir(main.path_ffmpeg) and 'ffmpeg.exe' \
    in os.listdir(main.path_ffmpeg): # checks for FFmpeg binaries existence passed from arguments
    path_ffmpeg = main.path_ffmpeg # if valid, assign it to path_ffmpeg
else:
    path_ffmpeg = \
        input('[INPUT] Enter the absolute path to \'ffmpeg/bin\' folder: '
              ) # ask the user for FFmpeg binaries if they are not found
    if not (os.path.isdir(path_ffmpeg) and 'ffmpeg.exe'
            in os.listdir(path_ffmpeg)): # checks for FFmpeg binaries validity given by the user
        main.exit_on_error("'ffmpeg/bin' folder is invalid, non-existing or does not contain binaries of ffmpeg."
                           ) # if not valid, exit the application (can't continue)

# cleaning the temporary files if present
try:
    for temp_file in os.listdir(main.path_temp):
        main.logwrite('Removing "{}/{}"...'.format(main.path_temp,
                      temp_file))
        os.remove('{}/{}'.format(main.path_temp, temp_file))
    main.logwrite('Removing "{}"...'.format(main.path_temp))
    os.rmdir(main.path_temp)
except:
    main.logwrite("Couldn't remove the temporary directory. Continuing..."
                  )
main.logwrite('Making "{}"...'.format(main.path_temp))
os.mkdir(main.path_temp)

main.logwrite('Changing current working directory to "{}"...'.format(main.path_temp))
os.chdir(main.path_temp)

# New download system (through finding the last song in the dir)
if not glob.glob('{}/*.mp3'.format(main.path_song)): # if no songs are present locally
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
        ydl.download('https://music.youtube.com/playlist?list=LM') # downloading handler
else: # if some songs are present, udgrade to find more
    for max_song_num in range(len(main.json_data['entries'])): # loop for all songs in JSON file
        if main.json_data['entries'][max_song_num]: # check for song validity on YouTube.com
            for full_mp3_file in \
                glob.glob('{}/*.mp3'.format(main.path_song)): # open mp3 files one by one to compare
                local_song = mutagen.easyid3.EasyID3(full_mp3_file) # open mp3 file metadata
                data_song = main.json_data['entries'][max_song_num] # open YouTube file metadata
                # if the metadata is identical, cap max_song_num by breaking loop
                if 'creator' and 'album' in data_song.keys():
                    if local_song['title'][0] == data_song['title'] \
                        and local_song['artist'] == local_song['author'
                            ] == data_song['creator'].split(', ') \
                        and local_song['album'][0] == data_song['album'
                            ]:
                        break
                else:
                    if local_song['title'][0] == data_song['title'] \
                        and local_song['artist'] == local_song['author'
                            ] == '' and local_song['album'][0] \
                        == data_song['album']:
                        break
            # break loop again
            if 'creator' and 'album' in data_song.keys():
                if local_song['title'][0] == data_song['title'] \
                    and local_song['artist'] == local_song['author'] \
                    == data_song['creator'].split(', ') \
                    and local_song['album'][0] == data_song['album']:
                    break
            elif 'creator' in data_song.keys() and 'album' \
                not in data_song.keys(): 
                if local_song['title'][0] == data_song['title'] \
                    and local_song['artist'] == local_song['author'] \
                    == data_song['creator'].split(', ') \
                    and local_song['album'][0] == '':
                    break
            elif 'creator' not in data_song.keys() and 'album' \
                in data_song.keys():
                if local_song['title'][0] == data_song['title'] \
                    and local_song['artist'] == local_song['author'] \
                    == '' and local_song['album'][0] \
                    == data_song['album']:
                    break
            else:
                if local_song['title'][0] == data_song['title'] \
                    and local_song['artist'] == local_song['author'] \
                    == '' and local_song['album'][0] == '':
                    break
    if max_song_num == 0:
        main.logwrite('Changing current working directory to "{}"...'.format(main.path_main))
        os.chdir(main.path_main)
        main.logwrite('Removing "{}"...'.format(main.path_temp))
        os.rmdir(main.path_temp)
        main.logwrite('Removing "{}"...'.format(main.path_json))
        os.remove(main.path_json)
        main.exit_on_error('No songs to download.')
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
            ydl.download('https://music.youtube.com/playlist?list=LM') # download handler

# Old download system (through input)
""" option = input('full/part? (f/p): ')
if option == 'p':
    main.logwrite('Downloading fixed amount of songs...')
    os.system(yt-dlp --cookies="{}" --playlist-end={} --write-thumbnail -x --audio-format=mp3 --audio-quality=0 --ffmpeg-location="{}" --output="%(id)s.mp3" -- https://music.youtube.com/playlist?list=LM'.format(main.path_temp, main.path_cookie, input('Enter # of last song to download: '), main.path_ffmpeg))
elif option == 'f':
    main.logwrite('Downloading songs...')
    os.system(yt-dlp --cookies="{}" --write-thumbnail -x --audio-format=mp3 --audio-quality=0 --ffmpeg-location="{}" --output="%(id)s.mp3" -- https://music.youtube.com/playlist?list=LM'.format(main.path_temp, main.path_cookie, main.path_ffmpeg)) """

counter = 1
for full_mp3_file in glob.glob('{}/*.mp3'.format(main.path_temp)): # parse through mp3 files
    for remote_song in main.json_data['entries']: # parse through JSON data
        if remote_song:
            if '{}\\{}.mp3'.format(main.path_temp, remote_song['id']) \
                == full_mp3_file: # if data matches-
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
                    local_song['artist'] = remote_song['creator'
                            ].split(', ')
                    main.logwrite('Setting #{} MP3 metadata author...'.format(counter))
                    local_song['author'] = remote_song['creator'
                            ].split(', ')
                else:
                    main.logwrite('Creator not found - setting #{} MP3 metadata artist and author...'.format(counter))
                    (local_song['artist'], local_song['author']) = ('',
                            '')
                if 'album' in remote_song.keys():
                    main.logwrite('Setting #{} MP3 metadata album name...'.format(counter))
                    local_song['album'] = remote_song['album']
                else:
                    main.logwrite('Album not found - settings #{} MP3 metadata album name...'.format(counter))
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
                os.rename(full_mp3_file,
                          '{}/{}.mp3'.format(main.path_song,
                          remote_song['title']))

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