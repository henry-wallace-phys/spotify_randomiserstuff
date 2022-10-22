from asyncio.windows_events import NULL
from formatter import NullWriter
from BackEndBaseClasses.newPlaylistGenerator import newPlaylistGenerator

class henrydle_base(newPlaylistGenerator):
    # Base class for Henrydle, uses random word gathering from playlist gatherer
    # Probably ought to abstract some things from the gatherer
    def __init__(self, username) -> None:
        super().__init__(username)

        self._randomtrack=None
        while  self._randomtrack==None:
            self._randomword=self.searchRandomWord()