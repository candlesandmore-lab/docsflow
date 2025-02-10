# Python tkinter hello world program 

from tkinter import Tk, Label

root = Tk() # TK Root-Widget
a = Label(root, text ="Hello World") # TK widget, instantiated in root
a.pack() 

#print(a.configure().keys())
root.mainloop() 
