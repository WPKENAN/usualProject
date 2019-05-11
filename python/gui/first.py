#encoding=utf-8
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, width=400, height=10)
        self.pack()
        self.pilImage = Image.open("C:\\Users\\Anzhi\Desktop\\first.png").resize((993,516))
        self.tkImage = ImageTk.PhotoImage(image=self.pilImage)
        self.label = tk.Label(self, image=self.tkImage,width=993,height=516)
        self.label.place(x=0, y=0, relwidth=1, relheight=1)
        self.label.pack()

        self.tmpImage = Image.open("C:\\Users\\Anzhi\Desktop\\1.jpg").resize((993, 516))
        self.tmpTkimage = ImageTk.PhotoImage(image=self.tmpImage)
        self.label2 = tk.Label(self, image=self.tmpTkimage, width=993, height=516)
        self.label2.place(x=0, y=0, relwidth=1, relheight=1)
        self.label2.pack()
        self.button=tk.Button(root, text='choose an image', command=self.printcoords,width=20).pack()
        self.pre_label=tk.Label(self,text='识别种类',width=100)
        self.pre_label.pack()

    def processEvent(self, event):
        pass

        # function to be called when mouse is clicked
    def printcoords(self):
        try:
            File = filedialog.askopenfilename(parent=root, initialdir="C:\\Users\\Anzhi\Desktop\\", title='Choose an image.')
            self.pilImage = Image.open(File);
            self.tkImage = ImageTk.PhotoImage(image=self.pilImage);
            self.pre_label["text"]=File
            self.label["image"]=self.tkImage
        except:
            pass



if __name__ == '__main__':
    root = tk.Tk()
    root.title("宠物狗识别系统")
    app = App(root)
    root.mainloop()
