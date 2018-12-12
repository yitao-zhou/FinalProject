from tkinter import *
import time
 
class StopWatch(Frame):
    msec = 50
    def __init__(self, parent=None, **kw):
        Frame.__init__(self, parent, kw)
        self._start = 0.0
        self._elapsedtime = 0.0
        self._running = False
        self.timestr = StringVar()
        self.makeWidgets()
        self.flag  = True
        
    def makeWidgets(self):
        l = Label(self, textvariable = self.timestr,background = "#92877d",font=("Verdana", 20, "bold"))
        self._setTime(self._elapsedtime)
        l.pack(fill = X, expand = NO)
    def _update(self):
        self._elapsedtime = time.time() - self._start
        self._setTime(self._elapsedtime)
        self._timer = self.after(self.msec, self._update)
    def _setTime(self, elap):
        minutes = int(elap/60)
        seconds = int(elap-minutes*60.0)
        hseconds = int((elap - minutes*60.0 - seconds) *100)
        self.timestr.set('%2d:%2d:%2d' %(minutes, seconds, hseconds))
    def Start(self):
        if not self._running:
            self._start = time.time() - self._elapsedtime
            self._update()
            self._running = True
    def Stop(self):
        if self._running:
            self.after_cancel(self._timer)
            self._elapsedtime = time.time() - self._start
            self._setTime(self._elapsedtime)
            self._running = False
            return  self.timestr.get()
    def Reset(self):
        self._start = time.time()
        self._elapsedtime = 0.0
        self._setTime(self._elapsedtime)
 
 
    def stopwatch(self):
        if self.flag == True:
            self.pack(side = TOP)
            Button(self, text = 'start', command = self.Start).pack(side = LEFT)
            Button(self, text = 'stop', command = self.Stop).pack(side = LEFT)
            Button(self, text = 'reset', command = self.Reset).pack(side = LEFT)
        self.flag = False
 

if __name__ == '__main__':
    def main():
        root = Tk()
        root.geometry('250x100')
        frame1 = Frame(root)
        frame1.pack(side = BOTTOM)
        sw = StopWatch(root)
        sw.stopwatch()
        root.mainloop()
        
    main()

