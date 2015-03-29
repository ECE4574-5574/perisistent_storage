import pymongo

# This class wraps very basic mongodb operations such as
# build/close connection, connection status, basic insert/query
class MongoDBInstance:
	def __init__(self, uri):
		self.MONGODB_URI = uri
		self.client = None
		self.db = None

	def connect(self):
		print "Connecting..."
		try:
			self.client = pymongo.MongoClient(self.MONGODB_URI);
			print "Connection established"
		except Exception, e:
			print "Connection failed"
			raise e

	def closeConnection(self):
		print "CLosing connection..."
		self.client.close()
		print "Connection closed"

	# Print False if there has been an error communicating with the server, else True
	def isAlive(self):
		print self.client.alive()

	# Current connected host
	def getHostName(self):
		host = self.client.host
		print host

	# Current connected port
	def getPortNumber(self):
		port = self.client.port
		print port

	# Get default database in that instance
	def getDefaultDatabase(self):
		self.db = self.client.get_default_database()
		return self.db

	# Return current database
	def getCurrentDatabase(self):
		print self.db
		return self.db

	# Print all collections(kind of like table in a sql db) in current database
	def getAllCollections(self):
		print self.db.collection_names(include_system_collections = False)

	# Insert JSON style data in to a specific collection
	def insertIntoCollection(self, collection_name, json_data):
		collection = self.db[collection_name]
		collection.insert(json_data)
		return collection;

	# Prints a single document in a collection (or None if there is no such collection)
	def findAny(self, collection_name):
		collection = self.db[collection_name]
		print collection.find_one();

	# Prints all documents matching a query (or None if there are no matches)
	def queryWithCondition(self, collection_name, condition):
		collection = self.db[collection_name]
		for post in collection.find(condition):
		    print post

    # Prints all documents in a collection (or None if there is no such collection)
	def findAll(self, collection_name):
		collection = self.db[collection_name]
		for post in collection.find():
			print post

	# Delete a collection
	def dropCollection(self, collection_name):
		self.db.drop_collection(collection_name)


sample = {
	"Owner": "Ning",
	"House name": "Ning's house",
	"Rooms": ["Bedroom1", "Bedroom2", "Bedroom3"]
}

query = {
	"Owner": "Ning"
}

testCon = {
	"author": "Mike"
}

uri = 'mongodb://dbUser:X574@ds045031.mongolab.com:45031/x574t'

if __name__ == '__main__':
    mongo = MongoDBInstance(uri)
    mongo.connect()
    mongo.getHostName();
    # get a db from this instance
    # note that this database currently have two collections: newCollection and test_database
    mongo.getDefaultDatabase()
    print "current database:"
    mongo.getCurrentDatabase()
    print "all collections in the database:"
    mongo.getAllCollections()
    # insert
    # mongo.insertIntoCollection("newCollection", sample)
    print "find any document in newColletion:"
    mongo.findAny("newCollection")
    print "find documents in newColletion that match condition:"
    mongo.queryWithCondition("newCollection", query)
    print "find all documents in test_database:"
    mongo.findAll("test_database")
    print "find documents in test_database that match condition:"
    mongo.queryWithCondition("test_database", testCon)

