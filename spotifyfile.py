from random import random
from tabnanny import verbose
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import spotipy.util as util
import sys
from random_word import RandomWords
import numpy as np
import time

class spotifyRandomiser:
    def __init__(self, username, verbose=False):
        self._username=username
        scope="user-modify-playback-state user-read-playback-position streaming user-top-read playlist-modify-public user-library-modify user-follow-read \
        user-read-currently-playing user-library-read"
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
        
        token = util.prompt_for_user_token(username, scope)

        self.sp = spotipy.Spotify(token)
        self._verbose=verbose
        self._playlist=[]
        time.sleep(10)

    def getPlaylist(self):
        return self._playlist


    def searchRandomWord(self):
        #Searches spotify with song with the title of a random word
        r=RandomWords()
        randomword=r.get_random_word()
        if self._verbose:
            print(f"Random word is : {randomword}")
        try:
            randomsongdict=self.sp.search(q=randomword, type="track", limit=1)
        except:
            print(f"For some reason spotify can't find {randomword}, sleeping")
            time.sleep(30)
            return 0
        try:
            randomsong=randomsongdict['tracks']['items'][0]
            if self._verbose:
                print(f"Song found is {randomsong['name']} at {randomsong['uri']}")
            return randomsong['uri']
        except IndexError:
            if self._verbose:
                print(f"Couldn't find song called {randomword}, try sleeping for 30s")
                time.sleep(30)
            return 0

    def constructPlaylist(self, playlistlength=30):
        play_count=0
        while play_count<playlistlength:
            trackid=self.searchRandomWord()
            if trackid!=0:
                self._playlist=np.append(self._playlist,trackid)
                play_count+=1
        if self._verbose:
            print("You've made a playlist, yaaay!")
    
        return 0

    def createPlaylist(self, playlistname):
        newplay=self.sp.user_playlist_create(self._username, playlistname)
        time.sleep(5)
        self.sp.user_playlist_add_tracks(self._username, newplay['id'], self._playlist)
        if self._verbose:
            print("Playlist made!")


if __name__=="__main__":
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print("Usage: %s username" % (sys.argv[0],))
        sys.exit()

    s=spotifyRandomiser(username, verbose=True)
    s.constructPlaylist(30)
    print(s.getPlaylist())
    s.createPlaylist("testing this agghh")