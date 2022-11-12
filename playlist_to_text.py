#!/usr/bin/python
# -*- coding: utf-8 -*-


# Imports
import main
import tabulate
import codecs
import logging


# Core
table = []
for counter, song in enumerate(main.json_data, start=1): # parsing through JSON data
    if song: # checking current song for validity
        info = [counter, song['id'], song['title']]
        if 'creator' in song.keys():
            info.append(song['creator'])
        else:
            info.append('')
        if 'album' in song.keys():
            info.append(song['album'])
        else:
            info.append('')
    else:
        logging.warning(f'Song #{counter} is invalid on YouTube.com.')
        continue
    table.append(info)
    logging.debug(f"Added entry #{counter}/{len(main.json_data)}")

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
                                     ['', 'Title', 'YouTube ID', 'Artist', 'Album'],
                                     tablefmt='presto'))