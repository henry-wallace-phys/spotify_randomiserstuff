from sre_parse import Verbose
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import spotipy.util as util
import sys
from random_word import RandomWords
import random
import numpy as np
import time
from tqdm import tqdm

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

class controlTools(spotifyLogin):
    '''
    Set of tools for controlling spotify playlist
    '''
    def __init__(self, username, playlistname, verbose=False):
        '''
        Playlist name: string = playlistname
        '''
        super().__init__(username)
        
        self._playlistname = playlistname
        userplaylists = self._sp.user_playlists(username)
        
        self._verbose = verbose

        self._playlistid=None        
        for iPlaylist in userplaylists['items']:
            if iPlaylist['name']==self._playlistname:
                self._playlistid=iPlaylist['id']
                continue
        
        if self._playlistid==None:
            print({f"ERROR : Could not find playlist called {playlistname}, sorry"})
            sys.exit()

        if self._verbose:
            print(f"Found playlist : {playlistname}")

        self._playlist = self._sp.playlist(self._playlistid)
        self._tracknames=[self._playlist['tracks']['items'][iTrack]['track']['name'] for iTrack in range(len(self._playlist['tracks']['items']))]
        self._trackids=[self._playlist['tracks']['items'][iTrack]['track']['id'] for iTrack in range(len(self._playlist['tracks']['items']))]
        self._track_name_dict={id : name for id,name in zip(self._trackids, self._tracknames)}

    def makeRandomQueue(self):
        random.shuffle(self._trackids)

    def playlistname(self):
        return self._playlistname

    def playlistid(self):
        return self._playlistid

    def tracklist(self):
        return self._tracknames

    def trackids(self):
        return self._trackids

    def trackname_to_id(self):
        return self._track_name_dict

    def __call__(self):
        print("Randomising track order")
        self.makeRandomQueue()

        if(self._verbose):
            print(f"Original track order is {self._tracknames}")
            print(f"New track order is {[self._track_name_dict[id] for id in self._trackids]}")        
            print("Adding to queue")

        for id in self._trackids:
            self._sp.add_to_queue(id)
        
        if(self._verbose):
            print("Skip to next track for proper randomisation! Done")


class spotifyRandomiser(spotifyLogin):
    #Class to find random songs on spotify, sleep statements necessary for API to work!
    def __init__(self, username, verbose=False):
        super().__init__(username)
        self._verbose=verbose
        self._playlist=[]
        self._newplay=None
        time.sleep(10)

    def getPlaylist(self):
        return self._playlist

    def searchRandomWord(self):
        #Searches spotify with song with the title of a random word
        r=RandomWords()
        randomword=r.get_random_word()
        if self._verbose:
            print(f"Random word is : {randomword}")
        if randomword==None:
            if self._verbose:
                print("Random word is None, skipping")
            return 0
        try:
            randomsongdict=self._sp.search(q=randomword, type="track", limit=1)
        except:
            if(self._verbose):
                print(f"For some reason spotify can't find {randomword}, sleeping")
            time.sleep(5)
            return 0
        try:
            randomsong=randomsongdict['tracks']['items'][0]
            if self._verbose:
                print(f"Song found is {randomsong['name']} at {randomsong['uri']}")
            return randomsong['uri']
        except IndexError:
            if self._verbose:
                print(f"Couldn't find song called {randomword}")
            time.sleep(3)
            return 0

    def constructPlaylistArray(self, playlistlength=30):
        startpoint=0
        startpoint+=len(self._playlist)
        self._playlist=np.append(self._playlist, np.empty(playlistlength, str))
        for i in tqdm(range(startpoint, playlistlength)):
            addplay=False
            while addplay==False:
                trackid=self.searchRandomWord()
                if trackid!=0:
                    self._playlist[i]=trackid
                    addplay=True
        if self._verbose:
            print("You've made a playlist, yaaay!")
    
        return 0

    def createPlaylist(self, playlistname):
        self._newplay=self._sp.user_playlist_create(self._username, playlistname)
        time.sleep(5)
        self._sp.user_playlist_add_tracks(self._username, self._newplay['id'], self._playlist)
        if self._verbose:
            print("Playlist made!")




if __name__=="__main__":
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print("Usage: %s username" % (sys.argv[0],))
        sys.exit()

    # s=spotifyRandomiser(username, verbose=False)
    # s.constructPlaylistArray(100)
    # s.createPlaylist("Bigger Rando")
    
    c=controlTools(username, "MeMelt")
    c()
    