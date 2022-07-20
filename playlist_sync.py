#!/usr/bin/python
# -*- coding: utf-8 -*-


# Imports
import main  # working with files + core
import glob
import os
import mutagen.easyid3  # working with audio metadata


# Core
for full_mp3_file in glob.glob('{}/*.mp3'.format(main.path_song)):  # parse through mp3 files
    for remote_song in main.json_data['entries']:  # parse through playlist metadata
        if remote_song:  # checks for song vaildation on YouTube
            main.logwrite("Checking '{}' with '{}'...".format(full_mp3_file,
                            remote_song['title']))
            local_song = mutagen.easyid3.EasyID3(full_mp3_file)  # open mp3 file

            # gather local song metadata
            local_song_data = [local_song['title'][0]]
            if 'artist' in local_song.keys():
                local_song_data.append(local_song['artist'])
            if 'album' in local_song.keys():
                local_song_data.append(local_song['album'][0])
            
            # gather remote song metadata
            remote_song_data = [remote_song['title']]
            if 'creator' in remote_song.keys():
                remote_song_data.append(remote_song['artist'].split(', '))
            if 'album' in remote_song.keys():
                remote_song_data.append(remote_song['album'])

            # compare the data...
            if local_song_data == remote_song_data:
                main.logwrite('Match found between "{}" and "{}". Continuing...'.format(local_song['title'
                                ][0], remote_song['title']))
                break
    else:
        main.logwrite("Match not found. Deleting '{}'...".format(full_mp3_file))
        os.remove(full_mp3_file)
else:
    main.errorwrite('Nothing to sync - no files.', 1)