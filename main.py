from henrydle import henrydle_gui
import sys
#Useful script, mostly for testing, will run Henrydle!

def useYourOwnMusic()->bool:
    nattempts=0
    while True and nattempts<3:
        response = input("Do you want to use your own music? [y/n] : ")
        if response=='y':
            print("Using your music!")
            return True
        elif response=='n':
            print("Generating songs using random words!")
            return False
        else:
            print("Invalid, please enter y/n!")
            continue
    print("You've taken more than 3 attempts to do this, shutting down")
    sys.exit(0)


if __name__=="__main__":
    dohernydles=True
    username=input("Please Enter Username : ")
    doownmusic=useYourOwnMusic()
    henrydle = henrydle_gui(username, doownmusic)
    henrydle()
            
    