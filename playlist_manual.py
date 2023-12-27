import main
import tabulate
import logging
import playlist_to_text

def choose_songs():
    table = playlist_to_text.generate_table()

    # Output the songs and wait for user input
    logging.debug('Printing parsed entries to the user...')
    print(f"\n\n{tabulate.tabulate(table, headers=['', 'YouTube ID', 'Title', 'Artist', 'Album'], tablefmt='presto')}\n")
    logging.debug('Waiting for user input on the song choice...')
    choice = main.loginput('Enter the song numbers you wish to download (e.g. 1-5,12,7-9,10)')

    # Get the URLs of the songs chosen
    logging.debug("Getting URLs of songs chosen...")
    song_numbers = []
    for part in choice.split(','):
        if '-' not in part:
            song_numbers.append(int(part)-1)
        else:
            for num in range(int(part.split('-')[0]), int(part.split('-')[1])+1):
                song_numbers.append(num-1)
    
    return [f"https://music.youtube.com/watch?v={main.songs_data[table[i][1]]['videoId']}" for i in song_numbers]