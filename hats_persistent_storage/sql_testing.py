from sys import argv
import mysqlinterface as sqlinter
from structures import Device, Room, House

# Read in mysql arguments.
script, usr, pwd, dtbs = argv;

# Initialize the interface and reset the table.
sql = sqlinter.MySQLInterface(usr, pwd, dtbs)
sql.reset_tables()

# Initialize devices and lists of devices.
dev1 = Device(10, 1, 1, "cat1", 1)
dev2 = Device(10, 2, 1, "cat2", 1)
dev3 = Device(10, 3, 1, "dog1", 2)
dev4 = Device(10, 4, 1, "dog2", 2)
dev5 = Device(10, 5, 1, "monkey")
r1devs = [dev1, dev2]
r2devs = [dev3, dev4]
hdevs = [dev5]

# Initialize rooms and lists of rooms
room1 = Room(10, 1, "cat room", r1devs)
room2 = Room(10, 2, "dog room", r2devs)
hrooms = [room1, room2]

# Initialize house
house = House(10, "pet home", hrooms, hdevs)

# Insert it all recursively.
sql.insert_house(house)

