import tkinter as tk
from PIL import Image, ImageTk
from Map import *

class SlamUI:
    ImageSize = 512
    
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Freenove 4WD Navigation")
        self.imgTk = ImageTk.PhotoImage(image="I", size=(self.ImageSize, self.ImageSize))
        self.imgSize = (self.imgTk.width(), self.imgTk.height())
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
        """
        img = Image.new("I", (16, 16), color="grey")
        for y in range(img.height):
            for x in range(img.width):
                img.putpixel((x, y), x * y)
        self.window.after(2000, lambda: self.updateImage(img))
        """

    def setArrow(self, pixStart, pixEnd):
        if self.idArrow:
            self.map.delete(self.idArrow)
        self.idArrow = self.map.create_line(pixStart[0], pixStart[1], pixEnd[0], pixEmd[1], fill="red", arrow=tk.LAST)

    def setCircle(self, pixPos, pixRadius):
        if self.idCircle:
            self.map.delete(self.idCircle)
        self.idCircle = self.map.create_oval(pixPos[0]-pixRadius, pixPos[1]-pixRadius, pixPos[0]+pixRadius, pixPos[1]+pixRadius, fill="green")
        
    def updateImage(self, img):
        self.imgTk.paste(img.resize((self.ImageSize, self.ImageSize), resample=Image.NEAREST))
        self.imgSize = (img.width, img.height)

    def mapClicked(self, event):
        if event.x >= self.imgTk.width() or event.y >= self.imgTk.height():
            return
        x = event.x * self.imgSize[0] // self.imgTk.width()
        y = event.y * self.imgSize[1] // self.imgTk.height()
        self.setCircle((x, y), 5)

    def scan(self):
        pass
        
    def turn(self):
        pass

    def go(self):
        print("Going!")
        map = Map((6.4, 6.4), 0.1)
        map.setLine((1.55, 5.55), (5.55,2.55))
        self.updateImage(map.map)
    
    def stop(self):
        print("Stopping!")

    def run(self):
        self.window.mainloop()

    def quit(self):
        self.window.destroy()

if __name__ == '__main__':
    ui = SlamUI()
    ui.run()
