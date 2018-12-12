# -*- coding:utf-8 -*-
# file: TkinterCanvas.py
#
import tkinter     
from PIL import Image, ImageTk
 
root = tkinter.Tk(className = 'rank')
canvas = tkinter.Canvas(root,
    width = 455,      
    height = 576,     
    bg = 'white')     
image = Image.open("rank_bg.jpg")
im = ImageTk.PhotoImage(image)
 
canvas.create_image(227.5,288,image = im)
f = open('rank.txt','r')
s = f.readlines()
v = []
for i in s:
    v.append(i.strip())
if len(v) > 10:
    k = 10
else:
    k=len(v)
    
y_pix=50

for i in range(k):
    canvas.create_text(227.5,y_pix,text='Time for No.'+str(i+1)+' : '+v[i],font=("Verdana", 20, "bold"))
    y_pix += 30
canvas.pack()       
root.mainloop()

