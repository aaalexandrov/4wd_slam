import tkinter as tk
from PIL import Image, ImageTk
from Map import *
from Slam import *

class SlamUI:
    ImageSize = 512
    
    def __init__(self, slam):
        self.slam = slam
            
        self.window = tk.Tk()
        self.window.title("Freenove 4WD Navigation")
        
        self.imgTk = ImageTk.PhotoImage(image="I", size=(self.ImageSize, self.ImageSize))
        self.map = tk.Canvas(width=self.imgTk.width(), height=self.imgTk.height(), bg="white")
        self.mapImg = self.map.create_image(0, 0, anchor=tk.NW, image=self.imgTk)
        self.map.bind("<Button-1>", self.mapClicked)
        self.map.pack()
        
        cmdFrame = tk.Frame(master=self.window)
        self.scanBtn = tk.Button(master=cmdFrame, text="Scan", command=self.scan)
        self.scanBtn.pack(fill=tk.X, side=tk.LEFT, expand=True)
        self.turnBtn = tk.Button(master=cmdFrame, text="Turn", command=self.turn)
        self.turnBtn.pack(fill=tk.X, side=tk.LEFT, expand=True)
        self.goBtn = tk.Button(master=cmdFrame, text="Go", command=self.go)
        self.goBtn.pack(fill=tk.X, side=tk.LEFT, expand=True)
        self.stopBtn = tk.Button(master=cmdFrame, text="Stop", command=self.stop)
        self.stopBtn.pack(fill=tk.X, side = tk.LEFT, expand=True)
        cmdFrame.pack(fill=tk.X)
        
        self.quitBtn = tk.Button(text="Quit", command=self.quit)
        self.quitBtn.pack(fill=tk.X)
        
        self.idArrow=None
        self.idCircle=None
        self.target = None
        
        self.syncWithSlam(True)

    def setArrow(self, pixStart, pixEnd):
        if self.idArrow:
            self.map.delete(self.idArrow)
        self.idArrow = self.map.create_line(pixStart[0], pixStart[1], pixEnd[0], pixEnd[1], fill="red", arrow=tk.LAST)

    def setCircle(self, pixPos, pixRadius):
        if self.idCircle:
            self.map.delete(self.idCircle)
        self.idCircle = self.map.create_oval(pixPos[0]-pixRadius, pixPos[1]-pixRadius, pixPos[0]+pixRadius, pixPos[1]+pixRadius, fill="green")

    def pixelFromPos(self, pos):
        pix = mul(div(pos, self.slam.map.sizeInMeters()), (self.ImageSize,)*2)
        pix = (pix[0], self.ImageSize - pix[1])
        return pix
        
    def posFromPixel(self, pix):
        pix = (pix[0], self.ImageSize - pix[1])
        return mul(div(pix, (self.ImageSize,)*2), self.slam.map.sizeInMeters())

    def syncWithSlam(self, syncMap):
        pix = self.pixelFromPos(self.slam.pos)
        delta = vecindir(self.slam.dir, 3.0)
        delta = (delta[0], -delta[1])
        self.setArrow(sub(pix, delta), add(pix, delta))
        if syncMap:
            self.updateImage(self.slam.map.map)
        
    def updateImage(self, img):
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
        self.imgTk.paste(img.resize((self.ImageSize, self.ImageSize), resample=Image.NEAREST))

    def mapClicked(self, event):
        if event.x >= self.imgTk.width() or event.y >= self.imgTk.height():
            return
        p = (event.x, event.y)
        self.setCircle(p, 5)
        self.target = self.posFromPixel(p)

    def scanCmd(self):
        self.slam.scan()
        self.syncWithSlam(True)
    
    def scan(self):
        self.slam.car.execCommand(self.scanCmd)
        
    def turnCmd(self, tgt):
        self.slam.turn(tgt)
        self.syncWithSlam(False)
    
    def turn(self):
        self.slam.car.execCommand(lambda: self.turnCmd(self.target))

    def goCmd(self, tgt):
        self.slam.moveTo(tgt)
        self.syncWithSlam(False)

    def go(self):
        self.slam.car.execCommand(lambda: self.goCmd(self.target))
    
    def stop(self):
        self.slam.car.execCommand(None)

    def run(self):
        self.window.mainloop()

    def quit(self):
        self.window.destroy()

if __name__ == '__main__':
    slam = Slam()
    ui = SlamUI(slam)
    ui.run()
