This is an experiment into seeing if I can have a tool that solves some puzzles from 
"The Witness" puzzle video game in real time while playing the game.

I place some very tight constraints on it to make it easier to write.


# Install

    py -3.11 -m venv venv
    source venv/Scripts/activate
    pip install pillow keyboard pytest matplotlib
    ...or...
    pip install -r requirements.txt


# Assumptions
- The Witness application is run at a resolution of 640x480.
- The Witness applications is run in windowed mode, not fullscreen.
- All desktop screen scaling is removed. 
