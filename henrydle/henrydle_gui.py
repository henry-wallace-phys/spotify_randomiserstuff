from henrydle import henrydle_base, answerStruct

#Was meant to use tkinter, at some point I will...

class henrydle_gui(henrydle_base):
    def __init__(self, username: str, pick_fromuserplaylist) -> None:
        super().__init__(username, pick_fromuserplaylist)


    def getUserInput(self, inputguess=None)->str:
        while True:
            if inputguess is None:
                inputguess = input ("What Song is this : ")
            if not isinstance(inputguess, str):
                print("Input must be a string!")
                continue
            else:
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
            gsr = input("Guess (g), Skip (s), replay (r) or give up (q)? (not entering one of these options will be treated as a guess): ").upper()
            if gsr == 'G':
                guesscheck = self.getUserInput()
                return guesscheck
            if gsr == 'S':
                return answerStruct.incorrect
            if gsr == 'R':
                self.playTrack(time)
                continue
            if gsr == 'Q':
                return "QUIT"
            else:
                guesscheck = self.getUserInput(gsr)
                return guesscheck

    def playTheGame(self):
        nAttempts=1
        time=1 #time of track in s

        guess_str=""

        #Give them 6 guesses
        while nAttempts<7:
            print(f"Guess number {nAttempts}/6")
            self.playTrack(time)
            guesscheck = self.guessSkipOrReplay(time)
            
            if(guesscheck=='QUIT'):
                print(f"BOOO You gave up after {time}s! The song was {self._randomtrack_name} by {self._artistnames}")
                guess_str+=answerStruct.incorrect*(6-nAttempts)
                print(guess_str)
                return 0
            
            
            guess_str+=guesscheck

            #Correct guess
            if(guesscheck==answerStruct.correctsong):
                print(f"Congrats! You got {self._randomtrack_name} by {self._artistnames}in {time}s")
                print(guess_str)
                print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%/n/n")
                return 0
            
                

            print(guess_str)
            time+=nAttempts
            nAttempts+=1
        
        print("Oh well, better luck next time!")
        print(f"The song was {self._randomtrack_name} by {self._artistnames}")
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%/n/n")


    def __call__(self):
        playhenrydle=True
        while playhenrydle:
            self.playTheGame()
            playhenrydle=self.playGameAgain()
