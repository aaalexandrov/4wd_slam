from Map import *
from Car import *

class Slam:
	MapSize = 16
	TileSize = 0.25
	ScanAngle = math.pi / 3
	
	def __init__(self):
		self.car = Car()
		self.car.stop()
		
		self.map = Map((self.MapSize, self.MapSize), self.TileSize)
		self.pos = mul(self.map.sizeInMeters(), (0.5,)*2)
		self.dir = 0.0
	
	
	def scan(self):
		self.car.pointSonic()
		scans = self.car.scanSector(-self.ScanAngle, self.ScanAngle)
		for ang, dist in scans:
			end = add(self.pos, vecindir(self.dir+ang, dist))
			self.map.setLine(self.pos, end)
			
	
