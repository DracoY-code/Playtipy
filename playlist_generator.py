import spotipy
from spotipy.oauth2 import SpotifyOAuth

from dotenv import load_dotenv

load_dotenv()


class SpotifyPlaylistGenerator():
    """Generates playlist from saved tracks.
    """

    def __init__(self, playlist_name: str=None) -> None:
        scope = '''
            playlist-modify-public
            playlist-modify-private
            user-library-modify
            playlist-read-private
            user-read-private
            user-library-read
            playlist-read-collaborative
        '''
        self.spotipyObject = spotipy.Spotify(
            auth_manager=SpotifyOAuth(scope=scope)
        )
        self.playlist_name = playlist_name
        self.user = self.spotipyObject.current_user()['id']

    def get_all_saved_tracks(self) -> list[dict]:
        """Returns a list containing all the saved tracks.
        """
        saved_tracks = self.spotipyObject.current_user_saved_tracks()
        all_tracks = saved_tracks['items']

        while saved_tracks['next']:
            saved_tracks = self.spotipyObject.next(saved_tracks)
            all_tracks.extend(saved_tracks['items'])

        return all_tracks

    def create_playlist(self, public: bool, description: str) -> None:
        """Create the playlist.
        """
        self.spotipyObject.user_playlist_create(
            self.user,
            self.playlist_name,
            public=public,
            description=description
        )

    def get_playlist_id(self) -> str:
        """Returns the playlist id.
        """
        playlist_id = ''
        playlists = self.spotipyObject.user_playlists(self.user)
        for playlist in playlists['items']:
            if playlist['name'] == self.playlist_name:
                playlist_id = playlist['id']
        return playlist_id

    def get_playlist_tracks(self, playlist_id: str) -> list[dict]:
        """Get all tracks in a playlist.
        """
        playlist = self.spotipyObject.user_playlist(self.user, playlist_id)
        tracks = playlist['tracks']

        all_tracks = tracks['items']

        while tracks['next']:
            tracks = self.spotipyObject.next(tracks)
            all_tracks.extend(tracks['items'])

        return all_tracks

    def get_track_ids(self) -> list[str]:
        """Get track ids from a playlist.
        """
        return [item['track']['id'] for item in self.get_playlist_tracks()]

    def get_saved_track_ids(self) -> list[str]:
        """Get track ids of all saved tracks.
        """
        return [item['track']['id'] for item in self.get_all_saved_tracks()]

    def add_to_playlist(self, playlist_id: str, track_ids: list[str]) -> None:
        """Add Tracks to the playlist.
        """
        start, end, total = 0, 100, len(track_ids)
        while total > 0:
            self.spotipyObject.user_playlist_add_tracks(self.user, playlist_id, track_ids[start:end])
            start += 100
            end += 100
            total -= 100

    def search_track(self, query: str) -> list[str]:
        """Search track with a query.
        """
        results = self.spotipyObject.search(q=query, limit=10, type='track')
        tracks = results['tracks']

        track_ids = []
        
        print()
        for idx, item in enumerate(tracks['items']):
            print(f"{idx}) {item['artists'][0]['name']} - {item['name']}")
            track_ids.append(item['id'])

        return track_ids

    def duration_saved(self) -> None:
        """Count the duration of all saved tracks.
        """
        tracks = self.get_all_saved_tracks()

        time_ms = sum([item['track']['duration_ms'] for item in tracks])
        time_min, time_sec = divmod(time_ms//1000, 60)
        time_hour, time_min = divmod(time_min, 60)

        print(f'{time_hour} hours {time_min} minutes {time_sec} seconds')

    def duration(self, playlist_id: str) -> None:
        """Count the duration of the playlist.
        """
        tracks = self.get_playlist_tracks(self.get_playlist_id())

        time_ms = sum([item['track']['duration_ms'] for item in tracks])
        time_min, time_sec = divmod(time_ms//1000, 60)
        time_hour, time_min = divmod(time_min, 60)

        print(f'{time_hour} hours {time_min} minutes {time_sec} seconds')


if __name__ == '__main__':
    print('Welcome to Spotify Playlist Generator!')

    while True:
        print('\n1 - Saved Tracks')
        print('2 - User Playlist')
        print('0 - Exit\n')

        list_choice = input('Where to go? ')
        if list_choice == '0':
            print('Bye')
            break

        if list_choice == '1':
            sp = SpotifyPlaylistGenerator()
            while True:
                print('\n1 - Create Playlist for Saved Tracks')
                print('2 - Add Tracks to the Playlist')
                print('3 - List All Saved Tracks')
                print('4 - Get Duration')
                print('0 - Go Back\n')

                operation = input('What to do? ')

                if operation == '1':
                    isPublic = input('Public? ([y]/n) ')
                    if isPublic == 'n':
                        sp.create_playlist(False, input('Please enter description of your playlist!\n'))
                    else:
                        sp.create_playlist(True, input('Please enter description of your playlist!\n'))
                    print('\nDone.')
                elif operation == '2':
                    sp.add_to_playlist(sp.get_playlist_id(), sp.get_saved_track_ids())
                    print('\nDone.')
                elif operation == '3':
                    for idx, item in enumerate(sp.get_all_saved_tracks()):
                        print(f'{idx}) {item["track"]["artists"][0]["name"]} - {item["track"]["name"]}')
                    print('\nDone.')
                elif operation == '4':
                    sp.duration_saved()
                elif operation == '0':
                    break
                else:
                    pass
        elif list_choice == '2':
            sp = SpotifyPlaylistGenerator(input('\nEnter playlist name: '))
            while True:
                print('\n1 - New Playlist? Create!')
                print('2 - Search and Add Tracks')
                print('3 - List All Tracks')
                print('4 - Get Duration')
                print('0 - Go Back\n')

                operation = input('What to do? ')

                if operation == '1':
                    isPublic = input('Public? ([y]/n) ')
                    if isPublic == 'n':
                        sp.create_playlist(False, input('Please enter description of your playlist!\n'))
                    else:
                        sp.create_playlist(True, input('Please enter description of your playlist!\n'))
                    print('\nDone.')
                elif operation == '2':
                    track_ids = sp.search_track(input('Search track: '))
                    track_num = int(input('\nSelect a track number: '))
                    if track_num < 0:
                        continue
                    sp.add_to_playlist(sp.get_playlist_id(), [track_ids[track_num]])
                    print('\nDone.')
                elif operation == '3':
                    for idx, item in enumerate(sp.get_playlist_tracks(sp.get_playlist_id())):
                        print(f'{idx}) {item["track"]["artists"][0]["name"]} - {item["track"]["name"]}')
                    print('\nDone.')
                elif operation == '4':
                    sp.duration(sp.get_playlist_id())
                elif operation == '0':
                    break
                else:
                    pass
        else:
            pass
