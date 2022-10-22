from henrydle import henrydle_base, answerStruct
import henrydle

class henrydle_gui(henrydle_base):
    def __init__(self, username: str, pick_fromuserplaylist) -> None:
        super().__init__(username, pick_fromuserplaylist)


    def getUserInput(self, inputguess=None)->str:
        while True:
            inputguess = input ("What Song is this : ")
            if not isinstance(inputguess, str):
                print("Input must be a string!")
                continue
            else:
                print(inputguess)
                return self.guessTrack(inputguess.upper())

    def playGameAgain(self)->bool:
        while True:
            inputguess = input("Play again? [y/n] : ")
            if inputguess=='y':
                self.resetHenrydle()
                return True
            elif inputguess=='n':
                return False
            else:
                print(f"{inputguess} is invalid! Please enter [y/n] : ")
                continue
    
    def guessSkipOrReplay(self, time: float):
        while True:
            gsr = input("Guess (g), Skip (s) or replay (r)? : ").upper()
            if gsr == 'G':
                guesscheck = self.getUserInput()
                return guesscheck
            if gsr == 'S':
                return answerStruct.incorrect
            if gsr == 'R':
                self.playTrack(time)
                continue
            else:
                print(f"{gsr} invalid! Please enter (g, s, r)")
                continue

    def playTheGame(self):
        nAttempts=0
        time=1 #time of track in s

        guess_str=""

        #Give them 6 guesses
        while nAttempts<6:
            print("Guess number {nAttempts}/6")
            self.playTrack(time)
            guesscheck = self.guessSkipOrReplay(time)
            guess_str+=guesscheck

            #Correct guess
            if(guesscheck==answerStruct.correctsong):
                print(f"Congrats! You got {self._randomtrack_name} in {time}s")
                print(guess_str)
                return 0

            print(guess_str)
            time+=nAttempts
            nAttempts+=1

    def __call__(self):
        playhenrydle=True
        while playhenrydle:
            self.playTheGame()
            playhenrydle=self.playGameAgain()
