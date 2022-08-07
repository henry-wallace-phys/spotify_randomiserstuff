from spotipyLogin import spotifyLogin
from tqdm import tqdm
import sys
'''
Gathers all user playlists together
'''

class playlistGatherer(spotifyLogin):
    def __init__(self, username: str):
        super().__init__(username)
        
        #Get all the playlists together
        self._playlistids=[]
        self._playlistnames=[]

        self._tracklist=[]
        self._trackuris=[]
        self._track_artist_name_dict={}

        self._playlistname=''
        self._playlistowner=None

    def getPlaylistIDs(self):
        return self._playlistids
    
    def getPlaylistNames(self):
        return self._playlistnames

    def getPlaylistName(self):
        return self._playlistname

    def getTrackURIs(self):
        return self._trackuris

    def getTrackNames(self):
        return self._track_artist_name_dict

    def getNewPlaylist(self):
        return self._newplaylist


    def _gatherUserPlaylistIDs(self):
        tempplaylistarr=[]
        print("Getting list of playlists")
        trackcounter=0
        done=False
        while not done:
            if(self._username==self._playlistowner):
                    newplaylists=self._sp.current_user_playlists(50, offset=50*trackcounter)
            else:
                newplaylists=self._sp.user_playlists(self._playlistowner, 50, offset=50*trackcounter)
            idlist=[iPlaylist['id'] for iPlaylist in newplaylists['items']]
            if(len(idlist)==0):
                done=True
            tempplaylistarr.append(idlist)
            trackcounter+=1
        
            #Ensure uniqueness
            for iPlayArr in tempplaylistarr:
                for playID in iPlayArr:
                    if playID not in self._playlistids:
                        self._playlistids.append(playID)

        print(f"Found {len(self._playlistids)} playlists")      

    def makePlaylistNameList(self):
        print("GETTING PLAYLIST NAMES")
        if(len(self._playlistids)==0):
            print("No playlists gathered yet")
            return []
        for iPlaylist in tqdm(self._playlistids):
            pl=self._sp.playlist(iPlaylist)
            self._playlistnames.append(pl['name'])
        return self._playlistnames

    def gatherUserSongs(self):
        print("GATHERING SONGS")
        tempTrackArr=[]

        for iPlaylistID in tqdm(self._playlistids):
            iPlaylist=self._sp.playlist(iPlaylistID)
            tracklist=[iTrack['track'] for iTrack in iPlaylist['tracks']['items']]
            tempTrackArr.append(tracklist)


        for iTrackArr in tempTrackArr:
            for iTrack in iTrackArr:
                trackname=iTrack['name']
                trackartist=iTrack['artists'][0]['name']
                trackuri=iTrack['uri']
                if trackuri not in self._trackuris and 'spotify:track' in str(trackuri):
                    if trackartist not in self._track_artist_name_dict:
                        self._trackuris.append(trackuri)
                        self._track_artist_name_dict[trackartist] = [trackname]
                    elif trackname not in self._track_artist_name_dict[trackartist]:
                        self._trackuris.append(trackuri)
                        self._track_artist_name_dict[trackartist].append(trackname)

        print(f"Found {len(self._trackuris)} songs from {len(self._track_artist_name_dict.keys())} artists")

    def makeMegaPlaylist(self, newplaylistname):
        print(f"Making mega playlist called {newplaylistname}!")

        self._playlistname=newplaylistname
        self._newplaylist=self._sp.user_playlist_create(self._username, newplaylistname)
        
        for iTrack in tqdm(range(0, len(self._trackuris), 99)):
            iTrackList=self._trackuris[iTrack:iTrack+99]
            try:
                self._sp.user_playlist_add_tracks(self._username, self._newplaylist['id'], iTrackList)
            except:
                print("You've given me a bad track!")
                print(iTrackList)
                sys.exit(-1)
        print("Made new playlist!")
            

    def __call__(self, playlistowner=None, newplaylistname: str='all my songs'):
        if playlistowner is None:
            self._playlistowner=self._username
        self._gatherUserPlaylistIDs()
        self.gatherUserSongs()
        self.makeMegaPlaylist(newplaylistname)


if __name__=='__main__':

    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print("Usage: %s username" % (sys.argv[0],))
        sys.exit()

    p=playlistGatherer(username)
    p()
    # p.makePlaylistNameList()
    # p.makeTrackNameList()

    