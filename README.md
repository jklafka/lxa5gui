# lxa5gui: A Python GUI for the Linguistica 5 project

### Test
To test a simple working GUI representation using SVG, you will need an installation of Python3, along with the svgwrite package (which can be installed with pip). Clone the repo. Run 

`python3 backend.py font_size text.txt`

where font_size is an integer representing the font size of text in the svg drawing and text.txt is the name of a .txt file with a corpus sample you want to analyze. The program will create a .svg file named "test-svgwrite.svg", which you can view with any svg viewer (Chrome works). 

### Files
gui_crab_nebula.py: a slightly modified version of the crab_nebula Python program written by John Goldsmith and Aris Xanthos, found at this repository (https://github.com/axanthos/lxa5crab). The output of the "main" function has been changed to only return the dictionary of signatures, mapping suffixes to their parastems. 

backend.py: an older but functional approach to constructing the SVG representation. 

new_backend.py: the current approach (under development). 

test-svgwrite.svg: a sample svg file showing the output of backend.py. 

### Currently under development:

new_backend.py
