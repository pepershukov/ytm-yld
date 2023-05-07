#!/usr/bin/python
# -*- coding: utf-8 -*-


# Imports
import main
import tabulate
import codecs
import logging


# Core
def generate_table():
    table = []
    for counter, song in enumerate(main.songs_data.values(), start=1): # parsing through JSON data
        options = main.song_options(song['id'])
        if not options['no-title'] or not options['no-artist']:
            remote_song_data = main.remote_songs_data[song['id']]
        info = [counter, song['id'], ''] if options['no-title'] else [counter, song['id'], remote_song_data['title']]
        if not options['no-artist']:
            artists = []
            for i in remote_song_data['author'].strip().split(', '):
                for artist in i.strip().split(' & '):
                    artists.append(artist)
            info.append(", ".join(artists))
        else:
            info.append('')
        if not options['no-album']:
            if 'album' in song.keys():
                info.append(song['album'])
            else:
                info.append(remote_song_data['title'])
        else:
            info.append('')
        table.append(info)
        logging.debug(f"Added entry #{counter}/{len(main.songs_data)}")
    return table

def write_file(table):
    
    logging.debug('Opening a text file...')
    try:
        with open(f"{main.path_song}/songs_info.txt", 'w') as file:
            logging.debug('Writing parsed data to text file...')
            file.write(tabulate.tabulate(table, 
                                        ['', 'YouTube ID', 'Title', 'Artist', 'Album'],
                                        tablefmt='presto'))
    except:
        with codecs.open(f"{main.path_song}/songs_info.txt", 'w', 'utf-16') as file:
            logging.debug('Writing parsed data to text file...')
            file.write(tabulate.tabulate(table, 
                                        ['', 'YouTube ID', 'Title', 'Artist', 'Album'],
                                        tablefmt='presto'))