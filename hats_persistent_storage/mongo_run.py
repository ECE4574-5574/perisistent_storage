
import pymongo
import connect_to_mongoDB

uri = 'mongodb://dbUser:X574@ds045031.mongolab.com:45031/x574t'
btmongo = connect_to_mongoDB.MongoDBInstance(uri)
btmongo.connect()
btmongo.getHostName()
btmongo.getDefaultDatabase()
btmongo.getCurrentDatabase()
btmongo.getAllCollections()

data0 = {
    "timestamp" : "today",
    "devicetype" : {"ID":"identification","name":"brookeslight","color":"yellow"},
    "houseid" : "bt",
    "roomid" : "livingroom",
}

#btmongo.insertIntoCollection("User_Actions",data0)
btmongo.findAll("User_Actions")
print "Querying for devicetype = light"
#btmongo.queryWithCondition("User_Actions",{"devicetype":"light"})
btmongo.queryWithCondition("User_Actions",{"devicetype":{"color":"yellow"}})

#GET AT/USERID/TIMEFRAME/DEVICETYPE/HOUSEID/ROOMID
#btmongo.queryWithCondition("User_Actions",{"devicetype":


'''
#creating a new collection
blankdata = { "data":"first entry"}
data0 = {
    "timestamp" : "today",
    "devicetype" : "light",
    "houseid" : "bt",
    "roomid" : "livingroom",
}
data1 = {
    "timestamp" : "today",
    "devicetype" : "doorlock",
    "houseid" : "bt",
    "roomid" : "",
}
data2 = {
    "timestamp" : "last week",
    "devicetype" : "light",
    "houseid" : "bt",
    "roomid" : "dining room",
}
data3 = {
    "timestamp" : "last week",
    "devicetype" : "garage door",
    "houseid" : "bt",
    "roomid" : "",
}
btmongo.insertIntoCollection("User_Actions",data0)
btmongo.insertIntoCollection("User_Actions",data1)
btmongo.insertIntoCollection("User_Actions",data2)
btmongo.insertIntoCollection("User_Actions",data3)
#btmongo.dropCollection("User_Actions")

#btmongo.getAllCollections()


btmongo.findAll("newCollection")
house0 = {
	"Owner": "owner0",
	"House name": "house0_name",
	"Rooms": ["room0", "room1", "room2"]
	"Devices": ["device0", "device1", "device2"]
}
house1 = {
	"Owner": "owner1",
	"House name": "house1_name",
	"Rooms": ["room3", "room4", "room5"]
	"Devices": ["device3", "device4", "device5"]
}
house2 = {
	"Owner": "owner2",
	"House name": "house2_name",
	"Rooms": ["room6", "room7", "room8"]
	"Devices": ["device6", "device7", "device8"]
}

btmongo.insertIntoCollection("newCollection", house0)
btmongo.insertIntoCollection("newCollection", house1)
btmongo.insertIntoCollection("newCollection", house2)
btmongo.findAll("newCollection")
'''

btmongo.closeConnection()
