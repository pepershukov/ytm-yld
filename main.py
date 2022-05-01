# Usage: python <path to script> [ffmpeg/bin folder] [YouTube cookie]
# Requirements:
# 1. ffmpeg: https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z
# 2. YouTube.com cookie as a "Netscape HTTP Cookie File": https://github.com/ytdl-org/youtube-dl/blob/master/README.md#how-do-i-pass-cookies-to-youtube-dl

import datetime, os, sys, yt_dlp, json, codecs

def logwrite(string):
    print('[LOG] {}'.format(string))
    with open('{}/log.txt'.format(path_main), 'a') as file:
        file.write('[{}] {}\n'.format(datetime.datetime.now(), string))   

try:
    path_ffmpeg = sys.argv[1]
except IndexError:
    path_ffmpeg = input('[INPUT] Enter the "ffmpeg/bin" folder (default: "C:/Program Files/ffmped/bin"): ')
try:
    path_cookie = sys.argv[2]
except IndexError:
    path_cookie = input('[INPUT] Enter the YouTube.com "Netscape HTTP Cookie File": ')
path_song = '{}/Music'.format(os.path.expanduser('~'))
path_temp = '{}/Music/temp'.format(os.path.expanduser('~'))
path_json = '{}/metadata.json'.format(os.path.abspath(os.path.dirname(__file__)))
path_main = os.path.abspath(os.path.dirname(__file__))

if __name__ == "__main__":
    try:
        logwrite('Removing a log file...')
        os.remove('{}/log.txt'.format(path_main))
    except FileNotFoundError:
        pass
    
    mode = input('playlist-to-text/donwload/both? (t/d/b): ')

    os.chdir(path_main)
    logwrite('Downloading a JSON metadata playlist file...')
    # os.system('cd "{}" & yt-dlp --cookies="{}" -i -J -- https://music.youtube.com/playlist?list=LM > metadata.json'.format(path_main, path_cookie))
    yt_options = {'cookiefile': path_cookie, 'no_warnings': True, 'dump_single_json': True, 'ignoreerrors': True}
    with yt_dlp.YoutubeDL(yt_options) as ydl:
        with open(path_json, 'w') as file:
            json.dump(ydl.sanitize_info(ydl.extract_info('https://music.youtube.com/playlist?list=LM', download=False)), file)

logwrite('Opening a JSON metadata playlist file...')
try:
    with open(path_json, 'r') as file:
        logwrite('Loading dictionary from JSON file...')
        json_data = json.load(file)
except:
    with codecs.open(path_json, 'r', 'utf-16') as file:
        logwrite('Loading dictionary from JSON file...')
        json_data = json.load(file)

if __name__ == "__main__":
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