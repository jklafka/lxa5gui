from tkinter import filedialog
from tkinter import *

root = Tk()
root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("Text files", "*.txt"),("all files","*.*")))
print (root.filename)
