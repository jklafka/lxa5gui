from tkinter import *
from tkinter import filedialog
import os
import json_backend

def query_filename():
    ''' Gets the absolute path of the file to run through crab_nebula.
    Can be called more than once, but if called must be given a filename or
    the backend will crash upon running. '''
    master.filename =  filedialog.askopenfilename(initialdir = "/", \
            title = "Select input file",\
            filetypes = (("Text files", "*.txt"),("all files","*.*")))
    Label(master, text=os.path.relpath(master.filename)).grid(row=1, column=2)
    return

def get_params(params):
    '''
    Retrieves the sorting, zooming and filtering parameters (if any) to use
    in running the crab_nebula algorithm. 
    '''
    if var1.get() == 1:
        params["sort_crit"] = "stems"
    if var2.get() == 1:
        params["sort_crit"] = "suffixes"
    if var3.get() == 1:
        params["sort_crit"] = "robustness"
    if var4.get() == 1:
        params["zoom"] = e6.get()
    suff_filter = e4.get()
    stem_filter = e5.get()
    print(suff_filter)
    print(stem_filter)
    params["filter_crit"] = ""
    if stem_filter != "":
        params["filter_crit"] += "stem="
        params["filter_crit"] += stem_filter
    elif suff_filter != "":
        params["filter_crit"] += "suffix="
        params["filter_crit"] += suff_filter
    return params

def run_crab_nebula(params):
    ''' Takes a dictionary of parameters and runs the Python
    crab_nebula algorithm through new_backend to generate the SVG image. '''
    params = get_params(params)
    print(params)
    params["filepath"] = master.filename
    if "sort_crit" not in params:
        params["sort_crit"] = None
    if params["filter_crit"] == "":
        params["filter_crit"] = None
    if "zoom" not in params:
        params["zoom"] = 1

    json_backend.main(params["filepath"], params["sort_crit"], \
        params["filter_crit"], params["zoom"])
    return

params = {}
master = Tk()

# Sorting
Label(master, text = "Sorting criterion?").grid(row=2, column = 0)
var1 = IntVar()
Checkbutton(master, text="Sort by stems?", variable=var1)\
    .grid(row=3, column=0, sticky=W)
var2 = IntVar()
Checkbutton(master, text="Sort by suffixes?", variable=var2)\
    .grid(row=3, column=1, sticky=W)
var3 = IntVar()
Checkbutton(master, text="Sort by robustness?", variable=var3)\
    .grid(row=3, column=2, sticky=W)


# Filtering
var4 = IntVar()
Label(master, text="Filters?").grid(row=4, column = 0)
e4 = Entry(master)
e5 = Entry(master)
Label(master, text="Suffix").grid(row=5, column=0)
Label(master, text="Stem").grid(row=5, column=2)
e4.grid(row=5, column=1)
e5.grid(row=5, column=3)
suff_filter = e4.get()
stem_filter = e5.get()

# Zooming
var4 = IntVar()
Checkbutton(master, text="Zoom?", variable=var4)\
    .grid(row=7, column=0, sticky=W)
Label(master, text = "Zoom level").grid(row=8, column = 0)
e6 = Entry(master)
e6.grid(row=8, column=1)

Button(master, text = "Filename", command=query_filename).grid(row = 1, \
    column = 0, sticky = W)
Button(master, text='Quit', command=master.quit).grid(row=10, column=0, \
    sticky=W, pady=4)
Button(master, text='Run', command=lambda : run_crab_nebula(params)).\
    grid(row=10, column=1, sticky=W, pady=4)

def var_states():
   print(var1.get())

mainloop()
