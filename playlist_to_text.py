import main, tabulate

table = []
counter = 1
for remote_song in main.json_data['entries']:
    if remote_song:
        table.append([remote_song['title'], remote_song['creator'], remote_song['album']])
        main.logwrite('Added entry #{}/{}'.format(counter, len(main.json_data['entries'])))
    counter += 1

main.logwrite('Opening a text file...')
with open('{}/songs_info.txt'.format(main.path_main), 'w') as file:
    main.logwrite('Writing parsed data to text file...')
    file.write(tabulate.tabulate(table, ['Title', 'Artist', 'Album'], tablefmt='grid'))