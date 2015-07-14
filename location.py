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

locator = Locator()

readfile = open('ipAddress.txt','r')
for line in readfile:

	match = geolite2.lookup(line.strip())
	data = match.location
	locator.addNode(data)
readfile.close()

target = locator.getNodeSet()

rowKeys = target.keys()
for itemKey in rowKeys:
	lineKeys = target[itemKey]
	dataKeys = lineKeys.keys()
	for data in dataKeys:
		#print lineKeys[data].getLocation(), lineKeys[data].getNum()
		break


