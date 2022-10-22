import sys
import random
from baseClasses.spotipyLogin import spotifyLogin

'''
Code to control playlists
'''


class playlistShuffler(spotifyLogin):
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


if __name__=="__main__":
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print("Usage: %s username" % (sys.argv[0],))
        sys.exit()

    PLAYLISTNAME="Pull Request Merge Coffee"
    s=playlistShuffler(username, PLAYLISTNAME, verbose=True)