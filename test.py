from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
from pylab import *
from geoip import geolite2 

class NodeLeader():

	def __init__(self,lat,lon):
		self.lon = lon
		self.lat = lat
		self.num = 0

	def addNum(self): 	
		self.num = self.num+1

	def getNum(self):
		return self.num
	
	def getLocation(self):
		return (self.lat,self.lon)

class Locator():

	def __init__(self):

		self.nodeSet = {} 

	def addNode(self,value):

		try:
			targetRow = self.nodeSet[value[0]]	
		except KeyError:
			targetRow = {}
			self.nodeSet[value[0]] = targetRow 

		try:
			targetLine = targetRow[value[1]]
		except KeyError:
			targetLine = NodeLeader(value[0],value[1])
			targetRow[value[1]] = targetLine 

		targetLine.addNum()

	def getNodeSet(self): 

		return self.nodeSet

def getAllTheColor():

	colorString = []
	colorFile = 'ColorDictionary.txt' 
	colorReader = open(colorFile,'r')
	for line in colorReader:
		splitter = line.strip().strip('\n')
		splitter = splitter.split(',')
		colorString = colorString + splitter

	colorReader.close()
	colorString = filter(None,colorString)
	return colorString

def getAllTheLocation():
	
	locator = Locator()
	readfile = open('ipAddress.txt','r')
	for line in readfile:

		match = geolite2.lookup(line.strip())
		data = match.location
		locator.addNode(data)
	readfile.close()
	return locator

if __name__ == '__main__':

	my_map = Basemap(projection='robin', lat_0=0, lon_0=0,
				   resolution='l', area_thresh=1000.0)
					
	my_map.drawcoastlines()
	my_map.drawcountries()
	my_map.fillcontinents(color='gray')

	locator = getAllTheLocation()
	target = locator.getNodeSet()
	rowKeys = target.keys()

	min_marker_size = 8 

	colorString = getAllTheColor()
	colorType = 0

	for itemKey in rowKeys:
		lineKeys = target[itemKey]
		dataKeys = lineKeys.keys()
		for data in dataKeys:
			locationInfo = lineKeys[data].getLocation()
			x,y = my_map(locationInfo[1],locationInfo[0])
			msize = lineKeys[data].getNum() + min_marker_size
			my_map.plot(x,y,color=colorString[colorType],marker='o',markersize=msize)
			colorType = (colorType + 1) % len(colorString)
			break

	plt.show()

