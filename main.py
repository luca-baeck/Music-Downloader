import spotipy
from youtubesearchpython import VideosSearch
import os
from pytube import YouTube
from pytube import Playlist
from pytube.cli import on_progress
import os.path
import requests


clientId = "301eba20552b498aac63fd5d7401bc91"
clientSecret = "08bc13b7b3ea450a9203ee03ce6c4cc6"

AUTH_URL = 'https://accounts.spotify.com/api/token'
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': clientId,
    'client_secret': clientSecret,
})
auth_response_data = auth_response.json()
access_token = auth_response_data['access_token']
spotify = spotipy.Spotify(access_token)

pName = ""

def getLinks(songs):
    links = []
    for song in songs:
        videosSearch = VideosSearch(song, limit=1)
        result = videosSearch.result()['result'][0]
        print('')
        print(song)
        print(result['link'])
        print('')
        link = result['link']
        links.append(link)
    return links

def makeOutput(name, output_path):
    counter = 1
    x = name + ' ' + str(counter)
    x = str(x)

    while(os.path.isdir(os.path.join(output_path, x))):
        counter = counter +1
        x = name + ' ' + str(counter)
        x = str(x)


    os.makedirs(os.path.join(output_path, x))
    return os.path.join(output_path, x)


def getSongs(link, output_path):
    songs = []
    if('open.spotify.com' in link):

        if('/track/' in link):
            results = spotify.track(link)
            song = results
            print('')
            print('Song name: ' + song['name'])
            print('')
            print(song['name'])
            print(song['artists'][0]['name'])
            print('')
            search = song['name'] + " " + song['artists'][0]['name']
            songs.append(search)
            output_path = makeOutput(search , output_path)


        elif('/playlist/' in link):
            results = spotify.playlist_items(link)
            results = results['items']
            id = link.replace('https://open.spotify.com/playlist/', '')
            if('?' in id):
                index = id.index('?')
                id = id[:index]
            playlist = spotify.playlist(id)
            print('')
            print('Playlist name: ' + playlist['name'])
            print('')
            output_path = makeOutput(playlist['name'] , output_path)


            for track in results:
                song = track['track']
                print('')
                print(song['name'])
                print(song['artists'][0]['name'])
                print('')
                search = song['name'] + " " + song['artists'][0]['name']
                songs.append(search)


        elif ('/album/' in link):
            results = spotify.album_tracks(link)
            results = results['items']
            id = link.replace('https://open.spotify.com/playlist/', '')
            if ('?' in id):
                index = id.index('?')
                id = id[:index]
            album = spotify.album(id)
            print('')
            print('Album name: ' + album['name'])
            print('')
            output_path = makeOutput(album['name'] , output_path)

            for track in results:
                song = track
                print('')
                print(song['name'])
                print(song['artists'][0]['name'])
                print('')
                search = song['name'] + " " + song['artists'][0]['name']
                songs.append(search)

    elif('youtube.com/' in link):

        if('/watch?' in link):
            yt = YouTube(link)
            print('')
            print('Song name: ' + yt.title)
            print('')
            print(yt.title)
            print(yt.author)
            print('')
            search = yt.title
            songs.append(search)
            output_path = makeOutput(search, output_path)

        elif('/playlist?' in link):
            play_list = Playlist(link)
            print('')
            print('Playlist name: ' + play_list.title)
            print('')
            output_path = makeOutput(play_list.title , output_path)

            for track in play_list.videos:
                print('')
                print(track.title)
                print(track.author)
                print('')
                search = track.title
                songs.append(search)


    return songs , output_path

def downloadSongs(links, output_path):
    counter = 0
    for link in links:
        yt = YouTube(link, on_progress_callback=on_progress)
        print('')
        print('downloaded ' + str(counter) + ' Songs from ' + str(len(links)) + ' Songs')
        print('')
        print('downloading ' + yt.title + ' from ' + yt.author + '(' + str(yt.length) + 's)' + ': ' + link)
        print("Song stats:")
        print('Views: ' + str(yt.views))
        print("Rating: " + str(yt.rating))
        print("From: " + str(yt.publish_date))
        print('')

        # Download mp3
        audio_file = yt.streams.filter(only_audio=True).first().download(output_path)
        base, ext = os.path.splitext(audio_file)
        new_file = base + '.mp3'
        os.rename(audio_file, new_file)
        counter = counter + 1
        print('')
        print('')
        print('')
    print('downloaded ' + str(counter) + ' Songs from ' + str(len(links)) + ' Songs')
    print('')
    print('')

print('')
print('***************************************************')
print('********** Music downloader by Luca Bäck **********')
print('***************************************************')
print('')

def run():
    link = input('Enter a link to a song, album or playlist on spotify or youtube... ')
    output_path = input('Enter a path where you want your songs to be saved... ')

    while( os.path.isdir(output_path) is False):
        output_path = input('Enter a path where you want your songs to be saved... ')

    x = getSongs(link, output_path)
    songs = x[0]
    if not(songs):
        return
    output_path = x[1]
    links = getLinks(songs)
    downloadSongs(links, output_path)
    print('Downloaded all songs')
    print('')


while True:
    run()