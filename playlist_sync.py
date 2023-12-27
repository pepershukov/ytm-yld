import main
import glob
import os
import logging

def sync():
    if not glob.glob(f"{main.path_song}/*.mp3"):
        logging.info('Nothing to sync - no files.')
        return

    for full_mp3_file in glob.glob(f'{main.path_song}/*.mp3'): # parse through mp3 files
        logging.debug("Getting song ID...")
        song_id = full_mp3_file.rsplit(os.sep, 1)[1][:full_mp3_file.rsplit(os.sep, 1)[1].find('.mp3')]
        if song_id in main.songs_data:
            logging.debug(f"[{song_id}] is still liked.")
        else:
            logging.info(f"[{song_id}] is not liked. Removing...")
            os.remove(full_mp3_file)