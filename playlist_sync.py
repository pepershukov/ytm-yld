#!/usr/bin/python
# -*- coding: utf-8 -*-


# Imports
import main  # working with files + core
import glob
import os
import mutagen.easyid3  # working with audio metadata


# Core
for full_mp3_file in glob.glob('{}/*.mp3'.format(main.path_song)):  # parse through mp3 files
    for song_info in main.json_data['entries']:  # parse through playlist metadata
        if song_info:  # checks for song vaildation on YouTube
            main.logwrite("Checking '{}' with '{}'...".format(full_mp3_file,
                            song_info['title']))
            local_song = mutagen.easyid3.EasyID3(full_mp3_file)  # open mp3 file

            # compare the data...
            if not 'artist' in local_song.keys() and not 'album' \
                in local_song.keys():
                if local_song['title'][0] == song_info['title']:
                    main.logwrite('Match found between "{}" and "{}". Continuing...'.format(local_song['title'
                            ][0], song_info['title']))
                    break
            elif not 'artist' in local_song.keys() and 'album' \
                in local_song.keys():
                if local_song['title'][0] == song_info['title'] \
                    and local_song['album'][0] == song_info['album']:
                    main.logwrite('Match found between "{}" and "{}". Continuing...'.format(local_song['title'
                            ][0], song_info['title']))
                    break
            elif 'artist' in local_song.keys() and not 'album' \
                in local_song.keys():
                if local_song['title'][0] == song_info['title'] \
                    and not local_song['artist'] \
                    == local_song['author'] == song_info['creator'].split(', '):
                    main.logwrite('Match found between "{}" and "{}". Continuing...'.format(local_song['title'
                            ][0], song_info['title']))
                    break
            else:
                if local_song['title'][0] == song_info['title'] \
                    and local_song['artist'] == local_song['author'
                        ] == song_info['creator'].split(', ') \
                    and local_song['album'][0] == song_info['album']:
                    main.logwrite('Match found between "{}" and "{}". Continuing...'.format(local_song['title'
                            ][0], song_info['title']))
                    break
    else:
        main.logwrite("Match not found. Deleting '{}'...".format(full_mp3_file))
        os.remove(full_mp3_file)
else:
    main.logwrite('Nothing to sync - no files. Continuing...')