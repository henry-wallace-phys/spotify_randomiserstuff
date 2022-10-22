Python code to play with spotify:
    
    To run simply do:
          $ python3 main.py
   
     (jupyter doesn't like this code for some reason!)
    
    - baseClasses ; Contains basic information for searching + loging into spotify

    - utils ;
        - playListGatherer : Makes playlists based on user criterion
        - playListShuffler : Actually shuffles a user's playback into the queue
        - playListStats : Gets user spotify statistics (incomplete!)
    
    - henrydle ;
        Personal implentation of heardle
        - henrydle_base : Base class, contains information for guessing and generating 
        - henrydle_gui : Basic UI stuff for Henrydle
