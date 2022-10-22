from time import sleep
from baseClasses import newPlaylistGenerator
from utils import playlistGatherer
import random 

class answerStruct:
    incorrect='⬛' #User guessed wrong
    correctsong='🟩' #User guessed correctly
    correctartist='🟨' #User was almost there!

class henrydle_base(newPlaylistGenerator):
    # Base class for Henrydle, uses random word gathering from playlist gatherer
    # Probably ought to abstract some things from the gatherer
    # Can either pick anything or just from your own songs
    def __init__(self, username: str, pick_fromuserplaylist: bool=True) -> None:
        super().__init__(username) #Login
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print("Welcome to Henrydle")

        self._useusersongs = pick_fromuserplaylist
        randomtrack_id = None

        if self._useusersongs: #Get it from user playlists
            print("Playing Henrydle in user song mode")

            self._pGather=playlistGatherer(username)
            self._pGather(username)
            randomtrack_id = random.choice(self._pGather.getTrackURIs())

        else: #Get it from a random word
            while  randomtrack_id==None:
                #Grab random track
                randomtrack_id=self.searchRandomWord()
        
        randomtrack = self._sp.track(randomtrack_id)

        self._randomtrack_uri=[randomtrack['uri']]
        self._randomtrack_name = randomtrack['name']
        self._randomtrack_artists = [iArtist['uri'] for iArtist in randomtrack['artists']]
        self._randomtrack_artistnames = [iArtist['name'] for iArtist in randomtrack['artists']]
    
        self._artisttracks = self.getArtistTrackList()
        self._artistnames = ""

        for iArtist in self._randomtrack_artistnames:
            self._artistnames+=f"{iArtist} "

    def getTrackName(self) -> str :
        return self._randomtrack_name

    def getTrackUri(self) -> list[str] :
        return self._randomtrack_uri

    def getTrackArtists(self) -> list[str] :
        return self._randomtrack_artistnames


    def playTrack(self, time: float) -> None:
        #Plays track for <time> s
        self._sp.start_playback(uris=self._randomtrack_uri)
        sleep(time)
        self._sp.pause_playback()

    def getArtistTrackList(self)->list[str]:
        #Gets albums for the artist
        alltrack_arr=[]
        for iArtistID in self._randomtrack_artists:
            artistalbums = self._sp.artist_albums(iArtistID)
            for iAlbum in artistalbums['items']:
                album_tracks=self._sp.album_tracks(iAlbum['uri'])
                for iTrack in album_tracks['items']:
                    alltrack_arr.append(iTrack['name'].upper())
        return alltrack_arr

    def guessTrack(self, songname: str)->str:
        songname=songname.upper()
        if len(songname)==0: #Just skip it if they don't enter anything!
            return answerStruct.incorrect
        elif songname == self._randomtrack_name.upper():
            #Done!
            return answerStruct.correctsong
        elif songname in self._randomtrack_name.upper():
            if songname in self._artisttracks: #Means all the remixes etc. don't matter!
                print("Not this version, but you've got it!")
                return answerStruct.correctartist
            else:
                print("Almost got it, but not quite!")
                return answerStruct.correctartist

        #Now we check to see if the artist is the same
        elif songname in self._artisttracks:
            return answerStruct.correctartist
        else:
            return answerStruct.incorrect

    def resetHenrydle(self):
        randomtrack_id = None
        if self._useusersongs:
            randomtrack_id=random.choice(self._pGather.getTrackURIs())
        else:
            while  randomtrack_id==None:
                #Grab random track
                randomtrack_id=self.searchRandomWord()
        
        randomtrack = self._sp.track(randomtrack_id)

        self._randomtrack_uri=[randomtrack['uri']]
        self._randomtrack_name = randomtrack['name']
        self._randomtrack_artists = [iArtist['uri'] for iArtist in randomtrack['artists']]
        self._randomtrack_artistnames = [iArtist['name'] for iArtist in randomtrack['artists']]

        self._artisttracks = self.getArtistTrackList()
