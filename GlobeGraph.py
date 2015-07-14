from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import argparse
from pylab import *
from geoip import geolite2 

class Peer():
	
	def __init__(self,pid,ip):
		self.pid = pid 
		self.ip = ip

	def getIp(self):
		return self.ip
	
	def getPid(self):
		return self.pid

def parseClientInfo( clientDataFileName ):
	
	peerData = {}
	readFile = open(clientDataFileName,'r')

	for line in readFile: 	
		split = line.split()
		peer = Peer(split[1],split[2])
		peerData[split[1]] = peer

	readFile.close()
	return peerData

def parseGroup( rttGroupFileName, peerInfo):

	groupSet = [] 
	readFile = open(rttGroupFileName,'r')
	for line in readFile:
		if 'printInfo,groupId:' in line:
			targetLine = line[line.index('printInfo,groupId:')+len('printInfo,groupId:'):]
			splitter = targetLine[targetLine.index('pid:')+len('pid:'):].split(',')

			group = []
			for item in splitter:
				if peerInfo.has_key(item):
					group.append(peerInfo[item])
					
			groupSet.append(group)

	readFile.close()
	return groupSet

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

def drawGraph(groupSet):

	my_map = Basemap(projection='robin', lat_0=0, lon_0=0,
				   resolution='l', area_thresh=1000.0)
					
	my_map.drawcoastlines()
	my_map.drawcountries()
	my_map.fillcontinents(color='gray')

	colorString = getAllTheColor()
	colorType = 0

	for group in groupSet:
		
		lon = []	
		lat = []
		for item in group:
			match = geolite2.lookup(item.getIp())
			lat.append( match.location[0])
			lon.append( match.location[1])

		x,y = my_map(lon,lat)
		my_map.plot(x,y,color=colorString[colorType],marker='o',markersize=15)
		colorType = (colorType + 1) % len(colorString)
	plt.show()

if __name__ == '__main__':

	parser = argparse.ArgumentParser()	
	parser.add_argument('-t',help='RttManger Log file name',type=str,required=True)	
	parser.add_argument('-a',help='Input the client data info which records its ip and pid.',type=str,required=True)
	args = parser.parse_args()
	
	peerInfo = parseClientInfo(args.a)
	groupSet = parseGroup(args.t,peerInfo)	
	drawGraph(groupSet)

