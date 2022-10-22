import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util

'''
Code to login to spotify
'''

class spotifyLogin:
    def __init__(self, username):
        self._username=username
        self._scope="user-modify-playback-state user-read-playback-position streaming user-top-read playlist-modify-public user-library-modify user-follow-read \
        user-read-currently-playing user-library-read"
        self._sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=self._scope))
        
        self._token = util.prompt_for_user_token(username, self._scope)

        self._sp = spotipy.Spotify(self._token)

    #Just some diagnostics stuff
    @property
    def username(self):
        return self._username

    @property
    def token(self):
        return self._token

    @property
    def spotifyinstance(self):
        return self._sp


    @property
    def scope(self):
        return self._scope 