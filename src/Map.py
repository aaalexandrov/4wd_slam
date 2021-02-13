import math

from PIL import Image

Invalid = -1
Free = 255
Blocked = 0
Unknown = 127

def neg(p):
    return tuple(-e for e in p)

def add(p0, p1):
    return tuple(e0+e1 for e0, e1 in zip(p0, p1))

def sub(p0, p1):
    return tuple(e0-e1 for e0, e1 in zip(p0, p1))

def mul(p0, p1):
    return tuple(e0*e1 for e0, e1 in zip(p0, p1))

def div(p0, p1):
    return tuple(e0-e1 for e0, e1 in zip(p0, p1))

def veclen2(p):
    return sum(e*e for e in p)

def veclen(p):
    return math.sqrt(veclen2(p))

def vecdist2(p0, p1):
    return veclen2(sub(p1, p0))

def vecdist(p0, p1):
    return veclen(sub(p1, p0))

def vecindir(angle, veclen = 1.0):
    return tuple(cos(angle)*veclen, sin(angle)*veclen)

class Map:
    def __init__(self, sizeInMeters, metersPerPixel):
        self.scale = metersPerPixel
        self.size = self.pixelFromPos(sizeInMeters)
        self.map = Image.new("I", self.size, color = Unknown)
        
    def pixelInside(self, pix):
        x, y = pix
        return 0 <= x and x < self.size[0] and 0 <= y and y < self.size[1]
    
    def pixelFromPos(self, pos):
        x, y = int(pos[0] / self.scale), int(pos[1] / self.scale)
        return (x, y)
    
    def posFromPixel(self, pix):
        return mul(pix, self.scale)
        
    def sizeInMeters(self):
        return self.posFromPixel(self.size)
    
    def getAt(self, pos):
        pix = self.pixelFromPos(pos)
        return self.getPix(pix)
    
    def getPix(self, pix):
        return self.map.getpixel(pix) if self.pixelInside(pix) else Invalid
    
    def setPix(self, pix, v):
        if self.pixelInside(pix):
            self.map.putpixel(pix, v)
    
    def setLine(self, pos0, pos1):
        dpos = sub(pos1, pos0)
        d = veclen(dpos)
        step = (self.scale * 0.1) / d
        t = 0
        while t <= 1:
            p = add(pos0, mul((t, t), dpos))
            pix = self.pixelFromPos(p)
            self.setPix(pix, Free)
            t += step
        self.setPix(self.pixelFromPos(pos1), Blocked)
        self.setPix(self.pixelFromPos(pos0), Free)
