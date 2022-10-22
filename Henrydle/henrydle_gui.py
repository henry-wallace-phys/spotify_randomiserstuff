from henrydle import henrydle_base, answerStruct

class henrydle_gui(henrydle_base):
    def __init__(self, username: str) -> None:
        super().__init__(username)


    def getUserInput(self, inputguess=None)->str:
        while True:
            inputguess = input ("What Song is this : ")
            if not isinstance(inputguess, str):
                print("Input must be a string!")
                continue
            else:
                print(inputguess)
                return self.guessTrack(inputguess.upper())
    
    def __call__(self):
        nAttempts=0
        time=1 #time of track in s

        guess_str=""

        #Give them 6 guesses
        while nAttempts<6:
            print("Guess number {nAttempts}/6")
            self.playTrack(time)
            guesscheck = self.getUserInput()
            guess_str+=guesscheck
            
            #Correct guess
            if(guesscheck==answerStruct.correctsong):
                print(f"Congrats! You got {self._randomtrack_name} in {time}s")
                print(guess_str)
                return 0

            print(guess_str)
            time+=nAttempts
            nAttempts+=1