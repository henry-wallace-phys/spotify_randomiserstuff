from henrydle import henrydle_gui
#Useful script, mostly for testing, will run Henrydle!

if __name__=="__main__":
    username=input("Please Enter Username : ")
    henrydle = henrydle_gui(username)
    henrydle()