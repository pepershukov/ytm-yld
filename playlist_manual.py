#!/usr/bin/python
# -*- coding: utf-8 -*-


# Imports
import main
import tabulate
import logging

def choose_songs():
    table = []
    for counter, song in enumerate(main.songs_data.values(), start=1): # parse through songs in playlist metadata
        remote_song_data = main.remote_songs_data[song['id']]
        song_info = [counter, song['id'], remote_song_data['title']] # create a table of details for the song

        artists = []
        for i in remote_song_data['author'].strip().split(', '):
            for artist in i.strip().split(' & '):
                artists.append(artist)
        song_info.append(", ".join(artists))

        if 'album' in song.keys():
            song_info.append(song['album'])
        else:
            song_info.append(remote_song_data['title'])

        table.append(song_info)
        logging.debug(f"Parsed entry #{counter}/{len(main.songs_data)}.")

    # Output the songs and wait for user input
    logging.debug('Printing parsed entries to the user...')
    print(f"\n\n{tabulate.tabulate(table, headers=['', 'YouTube ID', 'Title', 'Artist', 'Album'], tablefmt='presto')}\n")
    logging.debug('Waiting for user input on the song choice...')
    return main.loginput('Enter the song numbers you wish to download (e.g. 1-5,12,7-9,10)')