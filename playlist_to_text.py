import main
import tabulate
import codecs
import logging

def generate_table():
    table = []
    for counter, song in enumerate(main.songs_data.values(), start=1): # parsing through JSON data
        logging.debug("Getting song options...")
        options = main.song_options(song['videoId'])
        logging.debug("Getting song data...")
        song = main.songs_data[song["videoId"]]

        logging.debug("Getting title...")
        info = [counter, song['id'], ''] if options['no-title'] else [counter, song['videoId'], song['title']]

        if not options['no-artist']:
            logging.debug("Setting artists...")
            info.append(", ".join([i['name'] for i in song['artists']]))
        else:
            info.append('')

        if not options['no-album']:
            logging.debug("Setting album name...")
            if song['album']:
                info.append(song['album']['name'])
            else:
                info.append(song['title'])
        else:
            info.append('')
        
        table.append(info)
        logging.debug(f"Added entry #{counter}/{len(main.songs_data)}")
    return table

def write_file(table):
    logging.debug('Opening a text file...')
    with codecs.open(f"{main.path_song}/songs.txt", 'w', 'utf-16') as file:
        logging.debug('Writing parsed data to text file...')
        file.write(tabulate.tabulate(table, 
                                    ['', 'YouTube ID', 'Title', 'Artist', 'Album'],
                                    tablefmt='presto'))