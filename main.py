#!/usr/bin/python
# -*- coding: utf-8 -*-

# Usage: python <path to script> [YouTube cookie] [ffmpeg/bin folder]
# Requirements:
# 1. ffmpeg: https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z
# 2. YouTube.com cookie: "Netscape HTTP Cookie File": https://github.com/ytdl-org/youtube-dl/blob/master/README.md#how-do-i-pass-cookies-to-youtube-dl


# Imports
import datetime
import os
import sys
import yt_dlp
import json
import codecs


# Handlers
log_count = 1  # counter of log/error attempts

def logwrite(string):
    print ('[LOG] {}'.format(string))  # prints LOG stdout
    with open('{}/log.txt'.format(path_main), 'a') as file:
        file.write('[#{}] [LOG] [{}] {}\n'.format(log_count,
                   datetime.datetime.now(), string))  # writes stdout to file as LOG
    log_count += 1

def exit_on_error(string):
    print ('[ERROR] {} Exiting...'.format(string))  # prints ERROR stdout
    with open('{}/log.txt'.format(path_main), 'a') as file:
        file.write('[#{}] [ERROR] [{}] {}\n'.format(log_count,
                   datetime.datetime.now(), string))  # writes stdout to file as ERROR
    log_count += 1
    sys.exit()  # exits app


# Paths
try:
    path_ffmpeg = sys.argv[2]  # gets FFmpeg path from arguments
except IndexError:
    pass  # if not passed, handle an error

try:
    path_cookie = sys.argv[1]  # gets YouTube.com cookie path from arguments
except IndexError:
    path_cookie = \
        input('[INPUT] Enter the absolute path to YouTube.com "Netscape HTTP Cookie File": '
              )

                # if not passed, ask the user for one

if os.path.isfile(path_cookie):  # checks if cookie file is existing
    with open(path_cookie, 'r') as file:
        if not '# Netscape HTTP Cookie File' in file.readlines()[0] \
            or '# HTTP Cookie File' in file.readlines()[0]:  # checks for vaild formatting of a cookie file as depicted by yt-dlp
            exit_on_error('Invalid formatting of a YouTube.com cookie file. Look into \'README.md\' under \'Requirements\' for instructions.'
                          )
else:
    exit_on_error('Invalid or non-existant YouTube.com cookie file path.'
                  )

path_song = '{}/Music'.format(os.path.expanduser('~'))
path_temp = '{}/Music/temp'.format(os.path.expanduser('~'))
path_json = \
    '{}/metadata.json'.format(os.path.abspath(os.path.dirname(__file__)))
path_main = os.path.abspath(os.path.dirname(__file__))


# Main programm
if __name__ == '__main__':
    try:
        logwrite('Removing a log file...')
        os.remove('{}/log.txt'.format(path_main))
    except FileNotFoundError:
        pass

    mode = input('[INPUT] playlist-to-text/donwload/both? (t/d/b): ')

    os.chdir(path_main)
    logwrite('Downloading a JSON metadata playlist file...')

    # os.system('cd "{}" & yt-dlp --cookies="{}" -i -J -- https://music.youtube.com/playlist?list=LM > metadata.json'.format(path_main, path_cookie))

    with yt_dlp.YoutubeDL({
        'cookiefile': path_cookie,
        'no_warnings': True,
        'dump_single_json': True,
        'ignoreerrors': True,
        }) as ydl:
        with open(path_json, 'w') as file:
            json.dump(ydl.sanitize_info(ydl.extract_info('https://music.youtube.com/playlist?list=LM'
                      , download=False)), file)  # writing playlist data to JSON file

logwrite('Opening a JSON metadata playlist file...')
try:
    with open(path_json, 'r') as file:
        logwrite('Loading dictionary from JSON file...')
        json_data = json.load(file)
except:
    with codecs.open(path_json, 'r', 'utf-16') as file:
        logwrite('Loading dictionary from JSON file...')
        json_data = json.load(file)

if __name__ == '__main__':
    if mode == 't':
        logwrite('Parse only mode chosen.')
        import playlist_to_text
    elif mode == 'd':
        logwrite('Download only mode chosen.')
        import playlist_downloader
    elif mode == 'b':
        logwrite('Parse & Download mode chosen.')
        import playlist_to_text
        import playlist_downloader

    logwrite('Removing "{}"...'.format(path_json))
    os.remove(path_json)

    logwrite('Execution finished.')
    if mode == 't':
        logwrite('You can find your parsed songs at "{}/songs_info.txt".'.format(path_main))
    elif mode == 'd':
        logwrite('You can find your downloaded songs at "{}".'.format(path_song))
    elif mode == 'b':
        logwrite('You can find your parsed songs at "{}/songs_info.txt".'.format(path_main))
        logwrite('You can find your downloaded songs at "{}".'.format(path_song))