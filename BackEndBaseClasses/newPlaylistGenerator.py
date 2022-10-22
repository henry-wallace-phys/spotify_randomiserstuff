import sys
from random_word import RandomWords
import numpy as np
import time
from tqdm import tqdm

from BackEndBaseClasses .spotipyLogin import spotifyLogin

'''
Tools to make new playlists from non-user generated stuff
'''

class newPlaylistGenerator(spotifyLogin):
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
        #out of scope of this really, should make a generic utils class...
        r=RandomWords()
        randomword=r.get_random_word()
        if self._verbose:
            print(f"Random word is : {randomword}")
        if randomword==None:
            if self._verbose:
                print("Random word is None, skipping")
            return None
        try:
            randomsongdict=self._sp.search(q=randomword, type="track", limit=1)
        except:
            if(self._verbose):
                print(f"For some reason spotify can't find {randomword}, sleeping")
            time.sleep(5)
            return None
        try:
            randomsong=randomsongdict['tracks']['items'][0]
            if self._verbose:
                print(f"Song found is {randomsong['name']} at {randomsong['uri']}")
            return randomsong['uri']
        except IndexError:
            if self._verbose:
                print(f"Couldn't find song called {randomword}")
            time.sleep(3)
            return None

    def constructPlaylistArray(self, playlistlength=30):
        startpoint=0
        startpoint+=len(self._playlist)
        self._playlist=np.append(self._playlist, np.empty(playlistlength, str))
        for i in tqdm(range(startpoint, playlistlength)):
            trackid=None
            while trackid==None:
                trackid=self.searchRandomWord()
            self._playlist[i]=trackid
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

    s=newPlaylistGenerator(username, verbose=False)
    s.constructPlaylistArray(100)
    s.createPlaylist("Bigger Rando")
    

    