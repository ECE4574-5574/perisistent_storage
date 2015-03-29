from sys import argv
import mysqlinterface as sqlinter
from structures import Device, Room, House, User

# Read in mysql arguments.
script, usr, pwd, dtbs = argv;

# Initialize the interface and reset the table.
sql = sqlinter.MySQLInterface(usr, pwd, dtbs)
sql.reset_tables()

# Initialize devices and lists of devices.
dev1 = Device("duck10", "1", "1", "cat1", "1")
dev2 = Device("duck10", "2", "1", "cat2", "1")
dev3 = Device("duck10", "3", "1", "dog1", "2")
dev4 = Device("duck10", "4", "1", "dog2", "2")
dev5 = Device("duck10", "5", "1", "monkey")
r1devs = [dev1, dev2]
r2devs = [dev3, dev4]
hdevs = [dev5]

# Initialize rooms and lists of rooms
room1 = Room("duck10", "1", "cat room", r1devs)
room2 = Room("duck10", "2", "dog room", r2devs)
hrooms = [room1, room2]

# Initialize house
house = House("duck10", "pet home", hrooms, hdevs)

# Insert it all recursively.
sql.insert_house(house)

user1 = User("1", "OBAMA")
user2 = User("2", "OSAMA")
sql.insert_user(user1)
sql.insert_user(user2)
