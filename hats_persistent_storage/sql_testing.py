from sys import argv
import mysqlinterface as sqlinter
from structures import Device, Room, House

script, usr, pwd, dtbs = argv;

sql = sqlinter.MySQLInterface(usr, pwd, dtbs)
sql.reset_tables()


# Initialize devices and lists of devices.
dev1 = Device(1, 1, "cat1")
dev2 = Device(2, 1, "cat2")
dev3 = Device(3, 1, "dog1")
dev4 = Device(4, 1, "dog2")
dev5 = Device(5, 1, "monkey")
r1devs = [dev1, dev2]
r2devs = [dev3, dev4]
hdevs = [dev5]

# Initialize rooms and lists of rooms
room1 = Room(1, "cat room", r1devs)
room2 = Room(2, "dog room", r2devs)
hrooms = [room1, room2]

# Initialize house
house = House(10, "pet home", hrooms, hdevs)

sql.insert_house(house)

