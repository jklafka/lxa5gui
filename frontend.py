from tkinter import *
from tkinter import filedialog
import os
import new_backend

def query_filename():
    ''' Gets the absolute path of the file to run through crab_nebula.
    Can be called more than once, but if called must be given a filename or
    the backend will crash upon running. '''
    master.filename =  filedialog.askopenfilename(initialdir = "/", \
            title = "Select input file",\
            filetypes = (("Text files", "*.txt"),("all files","*.*")))
    Label(master, text=os.path.relpath(master.filename)).grid(row=1, column=2)
    return

def run_crab_nebula(params):
    ''' Takes a dictionary of parameters and runs the Python
    crab_nebula algorithm through new_backend to generate the SVG image. '''
    params["filepath"] = master.filename
    if "sort_crit" not in params:
        params["sort_crit"] = None
    if "filter_crit" not in params:
        params["filter_crit"] = None
    if "zoom" not in params:
        params["zoom"] = 1

    new_backend.main(params["filepath"], params["sort_crit"], \
        params["filter_crit"], params["zoom"])
    return

params = {}
master = Tk()

# Sorting
var1 = IntVar()
Checkbutton(master, text="Sorting?", variable=var1).grid(row=2, sticky=W)
Label(master, text="Suffix").grid(row=3, column=0)
Label(master, text="Stem").grid(row=3, column=2)
e2 = Entry(master)
e3 = Entry(master)
e2.grid(row=3, column=1)
e3.grid(row=3, column=3)
if var1.get() == 1:
    params["sort_crit"] = e2.get()

# Filtering
var2 = IntVar()
Checkbutton(master, text="Filtering?", variable=var2).grid(row=4, sticky=W)
e4 = Entry(master)
e5 = Entry(master)
e4.grid(row=5, column=1)
e5.grid(row=5, column=3)
if var2.get() == 1:
    params["filter_crit"] = e4.get()

## implement zooming

Button(master, text = "Filename", command=query_filename).grid(row = 1, \
    column = 0, sticky = W)
Button(master, text='Quit', command=master.quit).grid(row=10, column=0, \
    sticky=W, pady=4)
Button(master, text='Run', command=lambda : run_crab_nebula(params)).\
    grid(row=10, column=1, sticky=W, pady=4)


mainloop()
