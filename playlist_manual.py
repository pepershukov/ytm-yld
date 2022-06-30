import main, tabulate, playlist_downloader

table = []
counter = 1
for song in main.json_data['entries']:
    if song:
        song_info = [counter, song['title']]
        if 'creator' in song.keys():
            song_info.append(song['creator'])
        else:
            song_info.append('')
        if 'album' in song.keys():
            song_info.append(song['album'])
        else:
            song_info.append('')
    else:
        song_info = [counter, '', '', '']
    table.append(song_info)
    main.logwrite('Parsed entry #{}/{}.'.format(counter, len(main.json_data['entries'])))
    counter += 1

main.logwrite('Printing parsed entries to the user...')
print('\n\n{}\n'.format(tabulate.tabulate(table, headers=['', 'Title', 'Artist', 'Album'], tablefmt='presto')))
main.logwrite('Waiting for user input on the song choice...')
playlist_downloader.download_songs(manual=True, playlist_items=input('[INPUT] Enter the song numbers you wish to download (e.g. 1-5,12,7-9,10): '))