import os
import sys
import webbrowser

import spotipy
import spotipy.util as util
from spotipy.exceptions import SpotifyException


def show_current_song() -> None:
    """Tries to print the currently playing song details.
    """
    try:
        current_playback = spotipyObject.current_playback()
        if current_playback:
            deviceName = current_playback['device']['name']
            deviceType = current_playback['device']['type']
            artist = current_playback['item']['artists'][0]['name']
            song = current_playback['item']['name']
            print(f'\nCurrently playing : {song} - {artist}'
                + f' | {deviceName} [{deviceType}]')
    except (TypeError, ValueError):
        print('All devices are idle! ¯\_(ツ)_/¯')


def get_all_saved_tracks() -> list:
    """Returns a list containing all the saved tracks.
    """
    userTracks = spotipyObject.current_user_saved_tracks()
    allTracks = userTracks['items']

    while userTracks['next']:
        userTracks = spotipyObject.next(userTracks)
        allTracks.extend(userTracks['items'])

    return allTracks


def proper_time(time: float) -> str:
    """Returns proper representation of time provided in ms.
    """
    seconds = time // 1000
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    return f'{hours}:{minutes}:{seconds}'


if sys.argv[1:]:
    # Get user id from the command line
    username = sys.argv[1]
else:
    print('user_id missing! 😖')
    exit()

# Scope overkill
scope = 'user-read-playback-state\
        user-modify-playback-state\
        user-read-private\
        user-top-read\
        user-read-playback-position\
        user-read-currently-playing\
        playlist-read-private\
        user-follow-read\
        user-read-recently-played\
        playlist-modify-private\
        user-library-read'

try:
    token = util.prompt_for_user_token(
        username=username,
        scope=scope,
        cache_path=f'.cache-{username}'
    )
except:
    os.remove(f'.cache-{username}')
    token = util.prompt_for_username_token(username, scope)
finally:
    spotipyObject = spotipy.Spotify(auth=token)

user = spotipyObject.current_user()
name = user['display_name']

print(f'{name}, welcome to Playtipy v2.0! ☜(ﾟヮﾟ☜)')

while True:
    show_current_song()

    # Main Menu
    print('\n0 - Exit (～￣▽￣)～')
    print('1 - Search your devices')
    print('2 - Search your playlists')
    print('3 - Get all saved tracks')
    print('4 - Search an artist\n')

    choice = input('Your choice : ')

    if choice == '0':
        print('Bye!👋')
        break

    elif choice == '1':
        devices = spotipyObject.devices()
        deviceIDs = []

        num = 0
        device_menu = f'{num} - Go Back!\n'
        
        for device in devices['devices']:
            num += 1
            deviceIDs.append(device['id'])
            deviceName = device['name']
            deviceType = device['type']
            device_menu += f'{num} - {deviceName} [{deviceType}]\n'

        while True:
            print(device_menu)
            device_choice = input('Select the device : ')

            if device_choice == '0':
                print('Going back!🔙')
                break

            try:
                # Id of chosen device
                deviceId = deviceIDs[int(device_choice) - 1]

                while True:
                    print('0 - Go back!')
                    print('1 - Resume playback')
                    print('2 - Next track')
                    print('3 - Pause track')
                    print('4 - Previous track')
                    print('5 - Set Repeat mode')
                    print('6 - Toggle Shuffle state')

                    option_choice = input('\nSelect playback option : ')

                    try:
                        if option_choice == '0':
                            print('Going back!🔙\n')
                            break

                        elif option_choice == '1':
                            spotipyObject.start_playback(device_id=deviceId)

                        elif option_choice == '2':
                            spotipyObject.next_track(device_id=deviceId)

                        elif option_choice == '3':
                            spotipyObject.pause_playback(device_id=deviceId)

                        elif option_choice == '4':
                            spotipyObject.previous_track(device_id=deviceId)

                        elif option_choice == '5':
                            state = input(
                                'Select state [track/off] : '
                            ).lower()
                            if state == 'track' or state == 'off':
                                spotipyObject.repeat(state, deviceId)
                                print('Mode changed successfully! ✔')
                            else:
                                print('Mode could not be changed! ❌')

                        elif option_choice == '6':
                            state = input(
                                'Select state [true/false] : '
                            ).lower()
                            if state == 'true' or state == 'false':
                                spotipyObject.shuffle(state, deviceId)
                                print('Shuffle state changed! ✔')
                            else:
                                print('Error while changing state! ❌')

                        show_current_song()
                    except SpotifyException:
                        print('Forbidden 403: PREMIUM REQUIRED ⛔\n')

            except (IndexError, ValueError, TypeError):
                print('Device not found!📵')

        # Clears the device id list
        deviceIDs.clear()

    elif choice == '2':
        user_playlists = spotipyObject.user_playlists(user['id'])
        playlistIDs = []
        playlist_track_totals = []

        num = 0
        playlist_menu = f'{num} - Go Back!\n'

        for playlist in user_playlists['items']:
            num += 1
            playlistIDs.append(playlist['id'])
            playlist_track_totals.append(playlist['tracks']['total'])

            playlistName = playlist['name']
            playlistScope = playlist['public']

            if playlistScope:
                playlistScope = 'Public'
            else:
                playlistScope = 'Private'

            playlist_menu += f'{num} - {playlistName} [{playlistScope}]\n'

        while True:
            print(playlist_menu)
            playlist_choice = input('Select the playlist : ')

            if playlist_choice == '0':
                print('Going back!🔙')
                break

            try:
                while True:
                    print('0 - Go Back!')
                    print('1 - Get total of tracks')
                    print('2 - Get all tracks')

                    option_choice = input('\nSelect desired option : ')

                    if option_choice == '0':
                        print('Going back!🔙\n')
                        break

                    elif option_choice == '1':
                        # Get the total tracks from list
                        playlistTotalTracks = playlist_track_totals[
                            int(playlist_choice) - 1
                        ]
                        print(f'Total tracks : {playlistTotalTracks}\n')

                    elif option_choice == '2':
                        # Get the id from list
                        playlist_id = playlistIDs[int(playlist_choice) - 1]

                        tracks = spotipyObject.user_playlist_tracks(
                            user=user['id'],
                            playlist_id=playlist_id
                        )

                        trackData = ''

                        for track in tracks['items']:
                            track = track['track']
                            trackName = track['name']
                            primary_artist = track['artists'][0]['name']
                            trackData += f'{trackName} - {primary_artist}\n'

                        print(trackData)

            except (IndexError, ValueError, TypeError):
                print('Playlist not found!😲')

        # Clear playlist lists
        playlistIDs.clear()
        playlist_track_totals.clear()

    elif choice == '3':
        # Duration of the whole list
        duration = 0
        tracks = get_all_saved_tracks()
        
        for item in tracks:
            track = item['track']
            trackName = track['name']
            primary_artist = track['artists'][0]['name']
            
            duration += track['duration_ms']

            print(f'{trackName} - {primary_artist}')

        print(f'\n⏱  {proper_time(duration)} for {len(tracks)} tracks!')

    elif choice == '4':
        query = input('So, which artist do you wanna search? ').lower()
        results = spotipyObject.search(query, limit=1, offset=0,
                                       type='artist')

        # Artist details
        artist = results['artists']['items'][0]
        artistID = artist['id']

        print('\n', artist['name'], sep='')
        print(artist['followers']['total'], 'followers')
        print(artist['genres'][0])

        # Open artist image in browser
        webbrowser.open(artist['images'][0]['url'])

        # Get all albums of the artist
        albumResults = spotipyObject.artist_albums(artistID)['items']

        trackArts, artistData, num = [], '', 0

        for item in albumResults:
            # Album details
            albumName = item['name']
            albumId = item['id']
            albumArt = item['images'][0]['url']

            artistData += f'\nALBUM - {albumName}\n'

            # Get all tracks in the album
            trackResults = spotipyObject.album_tracks(albumId)['items']

            for item in trackResults:
                # Track details
                trackName = item['name']

                # Update the track list
                trackArts.append(albumArt)

                artistData += f'{num} : {trackName}\n'
                num += 1

        while True:
            print(artistData)
            song = input('Select the song number (x to exit) : ')

            if song == 'x': break

            try:
                # Open the track art in the browser
                webbrowser.open(trackArts[int(song)])
                print('You should be directed to the art! 😃')
            except (ValueError, IndexError, TypeError):
                print('Song does not exits ❌')

        # Clear the track list
        trackArts.clear()
