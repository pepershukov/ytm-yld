#!/usr/bin/python
# -*- coding: utf-8 -*-


# Imports
import main
import tabulate
import playlist_downloader


# Parsing the songs to output
table = []
counter = 1
for song in main.json_data['entries']: # parse through songs in playlist metadata
    if song: # if the song is valid on YouTube.com
        # song_info = [*counter*, *Title*, Author, Album]
        song_info = [counter, song['title']] # create a table of details for the song
        # song_info = [counter, Title, *Author*, Album]
        if 'creator' in song.keys():
            song_info.append(song['creator'])
        else: # if no author found in song metadata
            song_info.append('') # enter it as empty
        # song_info = [counter, Title, Author, *Album*]
        if 'album' in song.keys():
            song_info.append(song['album'])
        else: # if no album found in song metadata
            song_info.append('') # enter it as empty
    else:
        main.errorwrite('Song #{} \'{}\' is invalid on YouTube.com.'.format(counter, song['id']), 1)
        continue
    table.append(song_info)
    main.logwrite('Parsed entry #{}/{}.'.format(counter,
                  len(main.json_data['entries'])))
    counter += 1

# Output the songs and wait for user input
main.logwrite('Printing parsed entries to the user...')
print('\n\n{}\n'.format(tabulate.tabulate(table, headers=['', 'Title',
                         'Artist', 'Album'], tablefmt='presto')))
main.logwrite('Waiting for user input on the song choice...')
playlist_downloader.download_songs(manual=True,
                                   playlist_items=input('[INPUT] Enter the song numbers you wish to download (e.g. 1-5,12,7-9,10): '))