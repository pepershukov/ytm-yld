#!/usr/bin/python
# -*- coding: utf-8 -*-


import main
import tabulate


table = []
counter = 1
for remote_song in main.json_data['entries']: # parsing through JSON data
    if remote_song: # checking current song for validity
        info = [counter, remote_song['title']]
        if 'creator' in remote_song.keys():
            info.append(remote_song['creator'])
        else:
            info.append('')
        if 'album' in remote_song.keys():
            info.append(remote_song['album'])
        else:
            info.append('')
    else:
        info = [counter, '', '', '']
    table.append(info)
    main.logwrite('Added entry #{}/{}'.format(counter,
                  len(main.json_data['entries'])))
    counter += 1

main.logwrite('Opening a text file...')
with open('{}/songs_info.txt'.format(main.path_song), 'w') as file:
    main.logwrite('Writing parsed data to text file...')
    file.write(tabulate.tabulate(table, ['', 'Title', 'Artist', 'Album'],
               tablefmt='presto'))