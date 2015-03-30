
import pymongo
import connect_to_mongoDB

uri = 'mongodb://dbUser:X574@ds045031.mongolab.com:45031/x574t'
btmongo = connect_to_mongoDB.MongoDBInstance(uri)
btmongo.connect()
btmongo.getHostName()
btmongo.getDefaultDatabase()
btmongo.getCurrentDatabase()
btmongo.getAllCollections()
