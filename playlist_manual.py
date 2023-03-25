#!/usr/bin/python
# -*- coding: utf-8 -*-


# Imports
import main
import tabulate
import playlist_downloader
import logging

# Parsing the songs to output
table = []
for counter, song in enumerate(main.songs_data, start=1): # parse through songs in playlist metadata
    if song: # if the song is valid on YouTube.com
        song_info = [counter, song['title'], song['id']] # create a table of details for the song
        if 'creator' in song.keys():
            song_info.append(song['creator'])
        else: # if no author found in song metadata
            song_info.append('') # enter it as empty
        if 'album' in song.keys():
            song_info.append(song['album'])
        else: # if no album found in song metadata
            song_info.append('') # enter it as empty
    else:
        logging.warning(f"Song #{counter} '{song['id']}' is invalid on YouTube.com.")
        continue
    table.append(song_info)
    logging.debug(f"Parsed entry #{counter}/{len(main.songs_data)}.")

# Output the songs and wait for user input
logging.debug('Printing parsed entries to the user...')
print(f"\n\n{tabulate.tabulate(table, headers=['', 'Title', 'YouTube ID', 'Artist', 'Album'], tablefmt='presto')}\n")
logging.debug('Waiting for user input on the song choice...')
playlist_downloader.download_songs(manual=True,
                                   playlist_items=main.loginput('Enter the song numbers you wish to download (e.g. 1-5,12,7-9,10)'))