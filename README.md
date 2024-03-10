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


# Warts
- In general, this code evolved and was not designed.  It is messy.
- Puzzles that have breaks in the grid lines aren't handled how you would expect. You would expect to analyse
  the image, create a full grid, remove the edges of the grid that are "broken", set the cells' features (colored
  rectangles, triangles), then run the solver to generate valid paths.  However, because of how the code evolved... it
  was easier to generate the full grid, generate all paths for that grid, come up with all solutions and THEN remove
  those solutions that happened to include edges that were broken.
- The `cfg.py` module started as static constants. But it evolved into storing the puzzle-specific logic. Mutating global
  state, etc. Yuck.
