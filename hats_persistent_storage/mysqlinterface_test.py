import unittest
    
import httplib
from mysqlinterface import MySQLInterface
#from structures import User, House, Room, Device, UserAction, CompAction
from structures import *

class MySQLInterfaceTest(unittest.TestCase):
  def setUp(self):
    self.inter = MySQLInterface("mysql", "", "test_database")
    self.inter.reset_tables()
    self.dev1 = Device(1, 1, 1, "cat1", 1)
    self.dev2 = Device(1, 2, 2, "cat2", 1)
    self.dev3 = Device(1, 3, 1, "dog1", 2)
    self.dev4 = Device(1, 4, 2, "dog2", 2)
    self.dev5 = Device(1, 1, 1, "monkey1")
    self.dev6 = Device(1, 2, 2, "monkey2")

    self.r1devs = [self.dev1, self.dev2]
    self.r2devs = [self.dev3, self.dev4]
    self.h1devs = [self.dev5, self.dev6]

    self.room1 = Room(1, 1, "cat room", self.r1devs)
    self.room2 = Room(1, 2, "dog room", self.r2devs)
    self.hrooms = [self.room1, self.room2]

    self.house1 = House(1, "pet home", self.hrooms, self.h1devs)
    self.house2 = House(2, "people home", None, None)

    self.user1 = User(1, "OBAMA")
    self.user2 = User(2, "OSAMA")

    self.evilhouse = House(None, """'DROP TABLE houses;""", None, None)
    self.evilroom = Room(3, None, """'DROP TABLE house_rooms;""", None)
    self.evildevice = Device(3, None, 6, """'DROP TABLE house_devices;""")

    self.action1 = UserAction(1, 37, 1, 1, 2, "pet cat2")
    self.action2 = UserAction(1, 39, 1, 1, 1, "pet cat1")
    self.action3 = UserAction(2, 41, 2, None, 5, "fed monkey1")

    self.action4 = CompAction(1, 42, 1, 1, 2, "cat2 meow")
    self.action5 = CompAction(1, 44, 1, 1, 1, "cat1 meow")
    self.action6 = CompAction(2, 46, 2, None, 5, "monkey1 bite")

  def testSanity(self):
    self.assertEqual(1, 1)

  def testHouseInsertionAndQueries(self):
    result = self.inter.get_house_devices(1, None)
    self.assertEqual(self.inter.get_house_devices(1, None),
                     [])
    house1_id = self.inter.insert_house(self.house1)
    house2_id = self.inter.insert_house(self.house2)
    self.assertEqual(house1_id, 1)
    self.assertEqual(house2_id, 2)
    user1_id  = self.inter.insert_user(self.user1)
    user2_id  = self.inter.insert_user(self.user2)
    self.assertEqual(user1_id, 1)
    self.assertEqual(user2_id, 2)

    # Test data extraction
    self.assertEqual(self.inter.get_house_data(house1_id),
                     self.house1._data)
    self.assertEqual(self.inter.get_room_data(house1_id, 2),
                     self.room2._data)
    self.assertEqual(self.inter.get_device_data(house1_id, 1),
                     self.dev5._data)
    self.assertEqual(self.inter.get_user_data(1),
                     self.user1._data)

    # These are requests for items not in the databases.
    self.assertEqual(self.inter.get_house_data(3), None)
    self.assertEqual(self.inter.get_room_data(house1_id, 3), None)
    self.assertEqual(self.inter.get_device_data(house1_id, 3), None)
    self.assertEqual(self.inter.get_user_data(3), None)
        
    
    # Assert a device query has the proper result.
    answer = [self.dev2, self.dev4, self.dev6]
    result = self.inter.get_house_devices(house1_id, 2)
    self.assertEqual(len(answer), len(result))
    for i in range(0, len(result)):
      self.assertEqual(answer[i]._device_type, result[i]._device_type)
      self.assertEqual(answer[i]._data, result[i]._data)

    # Room device query test
    result = self.inter.get_room_devices(house1_id, 2, None)
    self.assertEqual(len(self.r1devs), len(result))
    for i in range(0, len(result)):
      self.assertEqual(self.r2devs[i]._device_id, result[i]._device_id)

  def testActionInsertionAndQueries(self):
    # Insert the actions
    self.inter.insert_user_action(self.action1)
    self.inter.insert_user_action(self.action2)
    self.inter.insert_user_action(self.action3)
    self.inter.insert_comp_action(self.action4)
    self.inter.insert_comp_action(self.action5)
    self.inter.insert_comp_action(self.action6)

    # User action query test
    answer = [self.action1, self.action2]
    result = self.inter.get_user_actions(1, None, None, None, None, None)
    self.assertEqual(len(answer), len(result))
    for i in range(0, len(result)):
      self.assertEqual(answer[i]._data, result[i]._data)

    # User action query by timestamp
    answer = [self.action2]
    result = self.inter.get_user_actions(None, None, None, None, 38, 40)
    self.assertEqual(len(answer), len(result))
    for i in range(0, len(result)):
      self.assertEqual(answer[i]._data, result[i]._data)

    # User actions by home
    answer = [self.action3]
    result = self.inter.get_user_actions(None, 2, None, None, None, None)
    self.assertEqual(len(answer), len(result))
    for i in range(0, len(result)):
      self.assertEqual(answer[i]._data, result[i]._data)

    # Computer actions by timestamp.
    answer = [self.action4, self.action5]
    result = self.inter.get_comp_actions(None, None, None, None, 42, 44)
    self.assertEqual(len(answer), len(result))
    for i in range(0, len(result)):
      self.assertEqual(answer[i]._data, result[i]._data)



  def testEvilQueries(self):
    self.inter.insert_house(self.evilhouse)
    self.inter.insert_room(self.evilroom)
    self.inter.insert_house_device(self.evildevice)


  def testUpdate(self):
    self.inter.insert_house(self.house1)
    self.inter.insert_user(self.user1)

    self.inter.update_house(1, "ANIMAL HOUSE")
    self.assertEqual(self.inter.get_house_data(1),
                     "ANIMAL HOUSE")

    self.inter.update_room(self.house1._house_id, self.room1._room_id, "HELLO KITTY ROOM")
    self.assertEqual(self.inter.get_room_data(self.house1._house_id, self.room1._room_id),
                     "HELLO KITTY ROOM")

    self.inter.update_device(self.house1._house_id, self.dev5._device_id, "Curious George")
    self.assertEqual(self.inter.get_device_data(self.house1._house_id, self.dev5._device_id),
                     "Curious George")

    self.inter.update_user(self.user1._user_id, "Mr. President")
    self.assertEqual(self.inter.get_user_data(self.user1._user_id),
                     "Mr. President")
  def tearDown(self):
    del self.inter

if __name__ == '__main__':
  unittest.main()
