import asyncio
import re
import time
from threading import Thread
import spotipy
from telethon import TelegramClient
from telethon.tl.functions.account import UpdateProfileRequest


def updateBio(client, message):
    print(f'Successfuly set up new bio. {message}')
    client(UpdateProfileRequest(
        about=message
    ))


def getSeconds(length):
    seconds = str((int)(length / 1000) % 60)
    return f'0{seconds}' if len(seconds) == 1 else seconds


def getSourse(spotify_object, url, type):
    print(url)
    id = re.search('(playlist\/|album\/|playlists\/)([\w+\d+]+)', url)

    return spotify_object.playlist(id.group(2))


def fetch_bio():
    global playlist
    while True:
        current = spotify_object.currently_playing()
        artist_name = current['item']['artists'][0]['name']
        song_name = current['item']['name']

        try:
            playlist_url = current['context']['external_urls']['spotify']

            playlist = getSourse(spotify_object, playlist_url)['name']
        except:
            playlist = current['item']['album']['name']

        length = current['item']['duration_ms']
        progress = current['progress_ms']
        time_left = (length - progress) / 1000
        minutes = (int)(progress / (1000 * 60)) % 60
        seconds = getSeconds(progress)
        seconds = f'0{seconds}' if len(seconds) == 1 else seconds
        length_minutes = (int)(length / (1000 * 60)) % 60
        length_seconds = getSeconds(length)
        time_progress = f'{minutes}:{seconds}/{length_minutes}:{length_seconds}'
        full_str = f'🎵{artist_name} - {song_name} {time_progress} | {playlist}'
        if (len(full_str) > 70):
            song_name = re.split('[\/\(-]', song_name)[0].strip()
        full_str = f'🎵{artist_name} - {song_name} {time_progress} | {playlist}'
        if (len(full_str) > 70):
            full_str = f'🎵{artist_name} - {song_name} | {playlist}'
        if (len(full_str) > 70):
            full_str = f'🎵{artist_name} - {song_name} {time_progress}'

        print(time_left, full_str, len(full_str))
        updateBio(client, full_str)
        time.sleep(min(time_left, 60))


def main():
    global spotify_object, client
    spotipy_client_id = 'SPOTIPY CLIENT ID'
    spotipy_secret = 'SPOTIPY SECRET'
    spotipy_redirect_uri = 'SPOTIPY REDIRECT URI'  # e.g. www.google.com
    scope = 'user-read-currently-playing'  # spotipy scope, user-read-currently-playing show currently playing song
    api_id = 'TELEGRAM API ID'
    api_hash = 'TELEGRAM API HASH'
    oauth_object = spotipy.SpotifyOAuth(client_id=spotipy_client_id,
                                        client_secret=spotipy_secret,
                                        redirect_uri=spotipy_redirect_uri,
                                        scope=scope)
    print(scope, oauth_object)
    token_dict = oauth_object.get_cached_token()
    token = token_dict['access_token']
    print(token)
    # spotify object
    spotify_object = spotipy.Spotify(auth=token)
    client = TelegramClient('SpotyBot', api_id, api_hash)
    client.start()
    t = Thread(fetch_bio())
    t.start()
    print('im here')


asyncio.run(main())
# client.run_until_disconnected()
