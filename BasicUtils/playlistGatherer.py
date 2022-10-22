from BackEndBaseClasses.spotipyLogin import spotifyLogin
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

        self._playlistignorelist=[]
        self._badartists=[]
        self._artistsarray=[]

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


    def _gatherUserPlaylistIDs(self):
        tempplaylistarr=[]
        print("Getting list of playlists")
        trackcounter=0
        done=False
        while not done:
            plist=[]
            if(self._username==self._playlistowner):
                newplaylists=self._sp.current_user_playlists(50, offset=50*trackcounter)
            else:
                newplaylists=self._sp.user_playlists(self._playlistowner, 50, offset=50*trackcounter)

            for iPlaylist in newplaylists['items']:
                if iPlaylist['name'] not in self._playlistignorelist:
                    plist.append(iPlaylist)

            if(len(plist)==0):
                done=True
            tempplaylistarr.append(plist)
            trackcounter+=1
        
            #Ensure uniqueness
            for iPlayArr in tempplaylistarr:
                for iPlay in iPlayArr:
                    if iPlay['id'] not in self._playlistids:
                        self._playlistids.append(iPlay['id'])
                        self._playlistnames.append(iPlay['name'])

        print(f"Found {len(self._playlistids)} playlists")     

    def gatherAllUserSongs(self):
        print("GATHERING SONGS")
        tempTrackArr=[]

        for iPlaylistID in tqdm(self._playlistids):
            iPlaylist=self._sp.playlist(iPlaylistID)
            tracklist=[iTrack['track'] for iTrack in iPlaylist['tracks']['items']]
            tempTrackArr.append(tracklist)
            
        print("Getting unique track array")
        for iTrackArr in tqdm(tempTrackArr):
            for iTrack in iTrackArr:
                if iTrack is not None:
                    trackname=iTrack['name']
                    trackartist=iTrack['artists'][0]['name']
                    trackuri=iTrack['uri']
                    if trackuri not in self._trackuris and 'spotify:track' in str(trackuri):
                        if trackartist not in self._badartists:
                            pass
                        if trackartist not in self._track_artist_name_dict:
                            self._trackuris.append(trackuri)
                            self._tracklist.append(iTrack)
                            self._track_artist_name_dict[trackartist] = [trackname]
                            self._artistsarray.extend([a['uri'] for a in iTrack['artists']])
                        elif trackname not in self._track_artist_name_dict[trackartist]:
                            self._trackuris.append(trackuri)
                            self._track_artist_name_dict[trackartist].append(trackname)
                            self._tracklist.append(iTrack)

        print(f"Found {len(self._trackuris)} songs from {len(self._track_artist_name_dict.keys())} artists")

    def makeMegaPlaylist(self):
        
        pexists=(self._newplaylist in self._playlistnames)

        pcount=1
        while pexists:
            newname=self._newplaylist+f" ({pcount})"
            if newname not in self._playlistnames:
                pexists=False
                self._newplaylist = newname
            else:
                pcount+=1

        print(f"Making mega playlist called {self._newplaylist}!")

        self._newplaylist=self._sp.user_playlist_create(self._username, self._newplaylist)
        
        for iTrack in tqdm(range(0, len(self._trackuris), 99)):
            iTrackList=self._trackuris[iTrack:iTrack+99]
            try:
                self._sp.user_playlist_add_tracks(self._username, self._newplaylist['id'], iTrackList)
            except:
                print("You've given me a bad track!")
                print(iTrackList)
                sys.exit(-1)
        print("Made new playlist!")


    def badMusicRemover(self):
        print(f"Removing {self._badartists} from your playlists")
        badmusiccounter=0

        if len(self._badartists)==0:
            return 0

        for iPlaylist in tqdm(self._playlistids):
            playlist=self._sp.playlist(iPlaylist)
            if playlist['owner']['id'] == self._username:
                tracklist=[iTrack['track'] for iTrack in playlist['tracks']['items']]
                for iTrack in tracklist:
                    if 'spotify:track' in iTrack['uri']:
                        trackartists=[iArtist['name'] for iArtist in iTrack['artists']]
                        if len(set.intersection(set(trackartists), set(self._badartists)))>0:
                            badmusiccounter+=1
                            try:
                                self._sp.playlist_remove_all_occurrences_of_items(self._username, iPlaylist, [iTrack['uri']])
                            except:
                                print("Tried to remove badly formatted track")

        print(f"Removed {badmusiccounter} songs")

    def makePlaylistForCategory(self, category, categoryval, categoryfunction=None, playlistname=None):
        print(f"Trying to make playlist containing all songs with {category}={categoryval}")
        cattrackuris=[]
        for iTrack in tqdm(self._tracklist):

            if categoryfunction is None:
                categoryfunction=lambda cv,iTr: iTr[category]==cv
            
            try:
                if categoryfunction(categoryval, iTrack):
                    cattrackuris.append(iTrack['uri'])
            except:
                print("Warning : Found exception, skipping!")

        if(len(cattrackuris)<=0):
            print(f"Could not find any songs with {category}={categoryval}")
            return 0
        else:
            if playlistname is None:
                playlistname=f"{self._playlistname}_{categoryval}"
        
            categoryplaylist=self._sp.user_playlist_create(self._username, f"{playlistname}")
            for iTr in tqdm(range(0, len(cattrackuris), 99)):
                iTrackList = cattrackuris[iTr:iTr+99]
                self._sp.user_playlist_add_tracks(self._username,categoryplaylist['id'], iTrackList)

            print(f"Made new playlist called {playlistname} with {len(cattrackuris)} songs")


    def makePlaylistForYear(self, release_year: str, playlistname=None):
        yearfunc=lambda ry, Tr: Tr['album']['release_date'][:4]==ry
        self.makePlaylistForCategory("release_date", release_year, categoryfunction=yearfunc, playlistname=playlistname)
    
    def makePlaylistForMonth(self, release_month: str, playlistname=None):
        monthfunc=lambda rm, Tr: Tr['album']['release_date'][5:7]==rm
        self.makePlaylistForCategory("release_date", release_month, playlistname=playlistname, categoryfunction=monthfunc)
 
    def makePlaylistForArtist(self, artist: str, playlistname=None):
        artistfunc=lambda a,Tr: a in [iArt['name'] for iArt in Tr['artists']]
        self.makePlaylistForCategory("artists", artist, playlistname=playlistname, categoryfunction=artistfunc)
    
    def makePlaylistByStartingLetter(self, letter: str, playlistname=None):
        letterfunc=lambda l, Tr: str(Tr['name'][0]).capitalize()==l
        self.makePlaylistForCategory("name", letter, playlistname=playlistname, categoryfunction=letterfunc)
                

    def __call__(self, playlistowner=None, newplaylistname: str='all my songs',
                 badartists=[], playlistignorelist=[]):
        
        self._playlistowner=playlistowner
        self._playlistignorelist=playlistignorelist
        self._newplaylist=newplaylistname
        self._badartists=badartists

        if self._playlistowner is None:
            self._playlistowner=self._username
        else:
            print(f"FINDING PLAYLIST FOR {playlistowner}")
        
        self._gatherUserPlaylistIDs()
        self.gatherAllUserSongs()


if __name__=='__main__':
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print("Usage: %s username" % (sys.argv[0],))
        sys.exit()

    BADLIST=['Tones And I', 'AJR', 'Ed Sheeran']
    IGNORELIST=['owens music']
    p=playlistGatherer(username)
    p(newplaylistname='All My Songs', playlistowner='dramallamaduck2', playlistignorelist=IGNORELIST, badartists=BADLIST)

    # p.makeMegaPlaylist()

    # for iYear in range(1960, 2022):
    # p.makePlaylistForYear(f"{2022}", f"All My Songs from {2022}")
    
    # monthtonamedict={
    #     '01' : "January", 
    #     '02' : "February",
    #     '03' : "March",
    #     '04' : "April",
    #     '05' : "May",
    #     '06' : "June",
    #     '07' : "July",
    #     '08' : "August",
    #     '09' : "September",
    #     '10' : "October",
    #     '11' : "November",
    #     '12' : "December"
    # }

    # for month in monthtonamedict.keys():
    #     p.makePlaylistForMonth(f"{month}", playlistname=f"All Songs I Like Released In {monthtonamedict[month]}")

    # for l in string.ascii_uppercase:
    #     p.makePlaylistByStartingLetter(l, playlistname=f"All Songs I Like Beginning with {l}")
    
