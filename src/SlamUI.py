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
        self.map.bind("<Button-1>", self.MapClicked)
        self.map.pack()
        cmdFrame = tk.Frame(master=self.window)
        self.go = tk.Button(master=cmdFrame, text="Go", command=self.Go)
        self.go.pack(fill=tk.X, side=tk.LEFT, expand=True)
        self.stop = tk.Button(master=cmdFrame, text="Stop", command=self.Stop)
        self.stop.pack(fill=tk.X, side = tk.LEFT, expand=True)
        cmdFrame.pack(fill=tk.X)
        self.quit = tk.Button(text="Quit", command=self.Quit)
        self.quit.pack(fill=tk.X)
        img = Image.new("I", (16, 16), color="grey")
        for y in range(img.height):
            for x in range(img.width):
                img.putpixel((x, y), x * y)
        self.window.after(2000, lambda: self.UpdateImage(img))
        
    def UpdateImage(self, img):
        self.imgTk.paste(img.resize((self.ImageSize, self.ImageSize), resample=Image.NEAREST))
        self.imgSize = (img.width, img.height)

    def MapClicked(self, event):
        if event.x >= self.imgTk.width() or event.y >= self.imgTk.height():
            return
        x = event.x * self.imgSize[0] // self.imgTk.width()
        y = event.y * self.imgSize[1] // self.imgTk.height()
        print(f"Click at {x}, {y}")

    def Go(self):
        print("Going!")
        map = Map((64, 64), 0.1, None)
        map.setLine((1.55, 5.55), (5.55,2.55))
        self.UpdateImage(map.map)
    
    def Stop(self):
        print("Stopping!")

    def Run(self):
        self.window.mainloop()

    def Quit(self):
        self.window.destroy()

if __name__ == '__main__':
    ui = SlamUI()
    ui.Run()
