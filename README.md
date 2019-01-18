# lxa5gui: A Python GUI for the Linguistica 5 project

### Basic usage
To test a simple working GUI representation using SVG, you will need an installation of Python 3, along with the svgwrite package (which can be installed with pip) and numpy. Clone the repo. Run

`python3 new_backend.py PATH_TO_SAMPLE`

where PATH_TO_SAMPLE is the relative filepath to the name of a .txt file with a corpus sample you want to analyze.
The program will create an SVG file named "crab_nebula.svg", which you can view with any svg viewer (Chrome works).

### Advanced Usage

To use the overall zoom, signature filter and signature sort features of **lxa5gui**, run

`python3 new_backend.py PATH_TO_SAMPLE SORTING_CRITERION FILTER_CRITERION ZOOM_LEVEL`

where PATH_TO_SAMPLE is as above. SORTING_CRITERION is one of the following: "stems" to sort by number of stems; "suffixes" to sort by number of suffixes; or "robustness" to sort by signature robustness. ZOOM is a float percentage of how much to magnify the resulting SVG file by. FILTER_CRITERION is either "suffix=X" where X is replaced by the suffix you want to filter by or "stem=X" where X is replaced by the stem you want to filter by. 

No additional dependecies are required.

### Files
*gui_crab_nebula.py*: a slightly modified version of the crab_nebula Python program written by John Goldsmith and Aris Xanthos. The original can be found at this repository (https://github.com/axanthos/lxa5crab). The output of the "main" function has been changed to only return the dictionary of signatures, mapping suffixes to their parastems.

*backend.py*: an older but functional approach to constructing the SVG representation.

*new_backend.py*: the current approach to constructing the SVG representation of signatures in lxa5gui. The approach depends on two types of "boxes": data_boxes, an abstract representation of a signature, group of stems or group of affixes that holds any text, parameters, statistics or characteristics what is represented; and graphics_box, which draws a data_box.

*test-svgwrite.svg*: a sample SVG file showing the output of backend.py.

*crab_nebula.svg*: a sample SVG file shwoing the output of new_backend.py.

### Under Development
