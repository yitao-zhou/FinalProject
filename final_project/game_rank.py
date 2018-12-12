# -*- coding:utf-8 -*-
# file: TkinterCanvas.py
#
import tkinter         # 导入Tkinter模块
from PIL import Image, ImageTk
 
root = tkinter.Tk(className = 'rank')
canvas = tkinter.Canvas(root,
    width = 455,      # 指定Canvas组件的宽度
    height = 576,      # 指定Canvas组件的高度
    bg = 'white')      # 指定Canvas组件的背景色
#im = Tkinter.PhotoImage(file='img.gif')     # 使用PhotoImage打开图片
image = Image.open("rank_bg.jpg")
im = ImageTk.PhotoImage(image)
 
canvas.create_image(227.5,288,image = im)# 使用create_image将图片添加到Canvas组件中
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
canvas.pack()         # 将Canvas添加到主窗口
root.mainloop()

