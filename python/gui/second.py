from tkinter import *
root = Tk()
#以不同的颜色区别各个frame
for fm in ['red','blue','yellow','green','white','black']:
    #注意这个创建Frame的方法与其它创建控件的方法不同，第一个参数不是root
    Frame(height = 800,width = 800,bg = fm).pack()
root.mainloop()
#添加不同颜色的Fr