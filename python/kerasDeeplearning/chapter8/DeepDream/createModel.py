import tkinter as tk
import sys
from tkinter import *
from tkinter.filedialog import askdirectory
import os
#from f_boq import getfboq

#import ImageTk


#coding=utf-8
material = Tk()
path = StringVar()
path_fboq = StringVar()
path_pboq = StringVar()

def selectPath():
    path_ = askdirectory()
    path.set(path_)


#file_dir=f_boq.file_dir
def getfboq():
    user=path.get()
    return path


def getpboq():
    path_pboq = path.get()



#https://s4.aconvert.com/convert/p3r68-cdx67/cbvkq-rgamb.gif

material.geometry("550x300")
material.configure(bg='#F8F8FF ')

#material = tk.Tk()

F1 = Frame(material)
F1.grid(row=0)

photo = PhotoImage(file="cat.gif")
label = Label(material, image=photo)
label.image = photo
label.place(x=420, y=150)



# the label of path
Label(material,text = "target path:").grid(row = 0, column = 0)
Entry(material, textvariable = path).grid(row = 0, column = 1)
Button(material, text = "path choose", command = selectPath).grid(row = 0, column = 2)

#path.set(Entry.textvariable)

#L1=Label(material,text = "file path:",bg='#008080').grid(row = 1, column = 0)
#path=Entry(material, textvariable = path_choose).grid(row = 1, column = 1)
#button1=Button(material, text = "choose path", command = selectPath,bg='#008080').grid(row = 1, column = 3)

#L2=Label(material,text = "PBOQ:",bg='#008080').grid(row = 2, column = 0)
#pboq_path=Entry(material, textvariable = path).grid(row = 2, column = 1)
#button2=Button(material, text = "choose path", command = selectPath,bg='#008080').grid(row = 2, column = 3)

# the label of button
button2=Button(material, text = "run fboq", command = getfboq,bg='#6495ED')
button3=Button(material, text = "run pboq", command = getpboq,bg='#6495ED')

button2.place(x=380, y=0)
button3.place(x=310,y=0)
material.mainloop()
