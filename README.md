# lxa5gui: A Python GUI for the Linguistica 5 project

### Basic usage
To test a simple working GUI representation using Tkinter, run

`python frontend.py`

A window will appear. From here you must choose a .txt file to run the Crab Nebula algorithm on. Choose one type of sorting if you wish to sort, and if you want to filter then check the box next to "Filter?" and put in either a stem or suffix to filter by. If you want to increase the size of the SVG output, then check the box next to "Zoom?" and put a positive integer in the box next to "Zoom level". All three features can be used simultaneously. 

The program will create an SVG file named "crab_nebula.svg", which you can view with any svg viewer (e.g. Google Chrome).

### Advanced Usage

To use the backend directly with overall zoom, signature filter and signature sort features of **lxa5gui**, run

`python new_backend.py PATH_TO_SAMPLE SORTING_CRITERION FILTER_CRITERION ZOOM_LEVEL`

where PATH_TO_SAMPLE is as above. SORTING_CRITERION is one of the following: "stems" to sort by number of stems; "suffixes" to sort by number of suffixes; or "robustness" to sort by signature robustness. ZOOM is a float percentage of how much to magnify the resulting SVG file by. FILTER_CRITERION is either "suffix=X" where X is replaced by the suffix you want to filter by or "stem=X" where X is replaced by the stem you want to filter by.

No additional dependecies are required.

### Files
*gui_crab_nebula.py*: a slightly modified version of the Crab Nebula Python program written by John Goldsmith and Aris Xanthos. The original can be found at this repository (https://github.com/axanthos/lxa5crab). The output of the "main" function has been changed to only return the dictionary of signatures, mapping suffixes to their parastems.

*backend.py*: an older but functional approach to constructing the SVG representation.

*new_backend.py*: the current approach to constructing the SVG representation of signatures in lxa5gui. The approach depends on two types of "boxes": data_boxes, an abstract representation of a signature, group of stems or group of affixes that holds any text, parameters, statistics or characteristics what is represented; and graphics_box, which draws a data_box.

*frontend.py*: the user-friendly GUI for running the Crab Nebula algorithm on a .txt file of user's choice.

*test-svgwrite.svg*: a sample SVG file showing the output of backend.py.

*crab_nebula.svg*: a sample SVG file shwoing the output of new_backend.py.

### Under Development
*frontend.py*: implementing zoom and more minor features. Next step beyond that is to directly display the SVG image through Tkinter.
*new_backend.py*: improving the sort and filter features, and making zoom more interactive.
