from utils.playlistGatherer import playlistGatherer
import matplotlib.pyplot as plt
import sys
from tqdm import tqdm
import collections
'''
Fun stats stuff with my playlists
'''
class playListStats(playlistGatherer):
    def __init__(self, username: str, playlistignorelist=[]):
        super().__init__(username)
    
        super_args={'playlistignorelist' : playlistignorelist}
        super().__call__(username, *super_args)
        self._genrearray=[]
        self._uniquegenrearray=[]
        self._genrefreqdict={}

    def getGenreList(self):
        return self._uniquegenrearray

    def getGenreFreqs(self):
        return self._genrefreqdict

    def generateTrackGenreArrays(self):
        print("Getting artist genres")
        self._genrearray=[]
        for iArtist in tqdm(self._artistsarray):
            self._genrearray.extend(self._sp.artist(iArtist)['genres'])
        self._uniquegenrearray= list(set(self._genrearray))
        print(f"You listen to {len(self._uniquegenrearray)} genres!")

    def generateTrackGenreFreqDict(self):
        self._genrefreqdict={}
        for genre in self._genrearray:
            if genre in self._genrefreqdict:
                self._genrefreqdict[genre]+=1
            else:
                self._genrefreqdict[genre]=1
        self._genrefreqdict={ g: f for g,f in sorted(self._genrefreqdict.items(), key=lambda item: item[1]) }
        print(self._genrefreqdict)
        
    def plotTopGenres(self, plottopN=40):
        topgenres={g: self._genrefreqdict[g] for g in list(self._genrefreqdict.keys())[:plottopN]}
        plt.bar(x=list(topgenres.keys()), height=list(topgenres.values()))
        plt.show()


    def __call__(self):
        print("Making some pretty plots!")
        self.generateTrackGenreArrays()
        self.generateTrackGenreFreqDict()



if __name__=='__main__':
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print("Usage: %s username" % (sys.argv[0],))
        sys.exit()    
    P=playListStats(username)
    P()
    P.plotTopGenres(20)
