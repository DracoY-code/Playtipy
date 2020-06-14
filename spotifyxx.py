import spotipy
import spotipy.util as util

import os
import json
import configparser as cp
import webbrowser as browser

# Get cfg data
config = cp.ConfigParser()
config.read('config.cfg')


# Set auth variables
username = config.get('SPOTIFY', 'USER_ID')
scope = 'user-library-read user-read-private user-read-playback-state '
        + 'user-modify-playback-state'
id = config.get('SPOTIFY', 'CLIENT_ID')
secret = config.get('SPOTIFY', 'CLIENT_SECRET')


# Get token for auth
try:
    token = util.prompt_for_user_token(
        username,
        scope,
        client_id=id,
        client_secret=secret,
        redirect_uri='https://google.com/',
        cache_path=f'.cache-{username}'
    )
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(
        username,
        scope,
        client_id=id,
        client_secret=secret,
        redirect_uri='https://google.com/',
        cache_path=f'.cache-{username}'
    )


# Global variables
trackURIs = []
trackArt = []

def list_tracks(bot, artistID):
    """ List all tracks of an artst. """
    # Albums and track details
    global trackURIs, trackArt
    z = 0

    # Extract album data
    albumResults = bot.artist_albums(artistID)
    albumResults = albumResults['items']

    for item in albumResults:
        print("ALBUM - " + item['name'])
        albumID = item['id']
        albumArt = item['images'][0]['url']

        # Extract track details
        trackResults = bot.album_tracks(albumID)
        trackResults = trackResults['items']

        for item in trackResults:
            print(str(z) + ": " + item['name'])
            trackURIs.append(item['uri'])
            trackArt.append(albumArt)
            z += 1
        print()


# ------------------------------------------------------------------------------
if token:
    # Spotify object
    bot = spotipy.Spotify(auth=token)

    # Get all devices
    devices = bot.devices()
    devices = devices['devices']
    # print(json.dumps(devices, sort_keys=True, indent=2))

    # Current user data
    user = bot.current_user()
    # print(json.dumps(user, sort_keys=True, indent=2))

    name = user['display_name']

    while True:
        print(
            "\n" + "Welcome to Playtipy, " + name + "!" + "\n"
            + "Your personal client for Spotify!" + "\n\n"
            + "0 - Search for an artist" + "\n"
            + "1 - Play on a device" + "\n"
            + "2 - Exit" + "\n"
        )
        choice = input("Your choice: ")

        # Search for an artist
        if choice == "0":
            print("\n" + "What's the name of the artist? ", end="")
            query = input()
            print()

            # Get search results
            try:
                results = bot.search(query, 1, 0, "artist")
            except:
                print("\nNot found!")
                break
            # print(json.dumps(results, sort_keys=True, indent=2))

            # Artist details
            artist = results['artists']['items'][0]
            artistID = artist['id']
            print(artist['name'])
            print(artist['followers']['total'], "followers")
            print(artist['genres'][0])
            print()

            # Open artist image in browser
            browser.open(artist['images'][0]['url'])

            # Listing all tracks
            list_tracks(bot, artistID)

            # See album art
            while True:
                song = input("Select song id to see album art (x to exit): ")
                if song == "x":
                    # Emptying the global variables
                    trackURIs.clear()
                    trackArt.clear()
                    break
                try:
                    browser.open(trackArt[int(song)])
                except:
                    print("\nInvalid song selected!\n")


        if choice == "1":
            print()
            c = 0
            number_of_devices = len(devices)
            if number_of_devices == 0:
                print("No device available!")
                break
            for item in range(number_of_devices):
                print(f"{c} - {devices[item]['type']}")
                c += 1
            print()
            a = input("Select device to use: ")

            try:
                # Get device
                a = int(a)
                deviceID = devices[a]['id']
                deviceName = devices[a]['name']
                deviceType = devices[a]['type']
            except:
                print("Currently no such device available!")
                break

            # Current track
            track = bot.current_user_playing_track()
            try:
                artists = track['item']['artists']
            except:
                print("Device is idle!")
            # print(json.dumps(track, sort_keys=True, indent=2))
            print()

            if track != None:
                primary_artist = track['item']['artists'][0]['name']
                track = track['item']['name']
                print("Currently playing: " + primary_artist + " - " + track)

                # Show all the artists
                number_of_artists = len(artists)
                if number_of_artists > 1:
                    print("Other artists: ", end="")
                    for item in range(1, number_of_artists):
                        print(artists[item]['name'], end="   ")
                    print()
                print()

            # Getting artist from user
            query = input("Choose artist to list tracks: ")
            try:
                results = bot.search(query, 1, 0, "artist")
            except:
                print("\nNot found!")
                break

            # Get artist ID
            artist = results['artists']['items'][0]
            artistID = artist['id']

            # Listing all tracks
            list_tracks(bot, artistID)

            # Choose song to play
            song = input("Select song to play (x to exit): ")
            if song == "x":
                # Emptying global variables
                trackURIs.clear()
                trackArt.clear()
                break
            trackSelection = []
            trackSelection.append(trackURIs[int(song)])

            # Play song
            try:
                bot.start_playback(deviceID, None, trackSelection)
                # bot.next_track(deviceID)
                # bot.pause_playback(deviceID)
                # bot.previous_track(deviceID)
                # bot.shuffle(True, deviceID)
                print("\nSuccess; your song should have been playing!")
            except:
                print("\n"
                    + "You can't access this functionality; Premium required")
                break


        # End the program
        if choice == "2":
            break

else:
    print("Can't get token for", username)
# ------------------------------------------------------------------------------
