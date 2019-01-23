from tkinter import *
import new_backend

def run_crab_nebula(params):
    ''' Takes a dictionary of parameters and runs the Python
    crab_nebula algorithm through new_backend to generate the SVG image. '''

    if "sort_crit" not in params:
        params["sort_crit"] = None
    if "filter_crit" not in params:
        params["filter_crit"] = None
    if "zoom" not in params:
        params["zoom"] = 1

    new_backend.main(params["filepath"], params["sort_crit"], \
        params["filter_crit"], params["zoom"])

params = {}
master = Tk()
Label(master, text="Filepath").grid(row=0)
Label(master, text="Suffix").grid(row=2, column=0)
Label(master, text="Stem").grid(row=2, column=2)

e1 = Entry(master)
e2 = Entry(master)
e3 = Entry(master)

e1.grid(row=0, column=1)
e2.grid(row=2, column=1)
e3.grid(row=2, column=3)

var1 = IntVar()
Checkbutton(master, text="Sorting?", variable=var1).grid(row=1, sticky=W)

params["filepath"] = e1.get()
if var1.get() is 1:
    params["sort_crit"] = e2.get()

Button(master, text='Quit', command=master.quit).grid(row=5, column=0, \
    sticky=W, pady=4)
Button(master, text='Run', command=run_crab_nebula(params)).\
    grid(row=5, column=1, sticky=W, pady=4)

mainloop()
