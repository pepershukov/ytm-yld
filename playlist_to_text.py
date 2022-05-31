#!/usr/bin/python
# -*- coding: utf-8 -*-
import main
import tabulate

table = []
counter = 1
for remote_song in main.json_data['entries']: # parsing through JSON data
    if remote_song: # checking current song for validity
        table.append([remote_song['title'], remote_song['creator'],
                     remote_song['album']]) # add its [title, creator, album] to table
        main.logwrite('Added entry #{}/{}'.format(counter,
                      len(main.json_data['entries'])))
    counter += 1

main.logwrite('Opening a text file...')
with open('{}/songs_info.txt'.format(main.path_main), 'w') as file:
    main.logwrite('Writing parsed data to text file...')
    file.write(tabulate.tabulate(table, ['Title', 'Artist', 'Album'],
               tablefmt='grid'))