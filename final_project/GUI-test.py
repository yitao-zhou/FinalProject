import tkinter
root = tkinter.Tk()  # 生成root主窗口
label = tkinter.Label(root, text='Come and Chat')  # 生成标签
label.pack()  # 将标签添加到主窗口
button1 = tkinter.Button(root, text='Button1')  # 生成button1
button1.pack(side=tkinter.LEFT)  # 将button1添加到root主窗口
button2 = tkinter.Button(root, text='Button2')
button2.pack(side=tkinter.RIGHT)
root.mainloop()  # 进入消息循环（必需组件）
