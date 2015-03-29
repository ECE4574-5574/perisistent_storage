import mysql.connector
from mysql.connector import errorcode
from structures import Device, Room, House

class MySQLInterface:
  def __init__(self, usr, pwd, dtbs):
    # Store information.
    self._dtbs = dtbs;
    self._usr = usr;
    self._pwd = pwd;

    # Try to connect to the given database.
    self._broken = False;
    try:
      self._cnx =  mysql.connector.connect(
          user=self._usr,
          passwd=self._pwd,
          host='localhost');
    except mysql.connector.Error as err:
      self._broken = True;
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
      else:
        print(err)
      return;

    # Create a cursor for the database.
    self._cur = self._cnx.cursor();
    self._cur.execute("CREATE DATABASE IF NOT EXISTS " + self._dtbs);
    self._cur.execute("USE " + self._dtbs);

    # Create strings for each table name
    self._house_table = "houses";
    self._hr_table = "house_rooms";
    self._hd_table = "house_devices";
    self._rd_table = "room_devices";

  # If the broken flag has been set anywhere, do not execute methods.
  def is_broken(self):
    if self._broken:
      print "Can not use method. Error occurred when Table was opened."
      return True;

  # If the database was freshly created, this is a necessary step.
  def reset_tables(self):
    if self.is_broken(): return

    # The schema for the tables are hardcoded here, modify if changes desired.
    Tables = {}
    Tables['houses'] = (
      "CREATE TABLE houses ("
      "house_id MEDIUMINT, "
      "data MEDIUMBLOB, "
      "PRIMARY KEY(house_id) );")

    Tables['house_rooms'] = (
      "CREATE TABLE house_rooms ("
      "house_id MEDIUMINT, "
      "room_id MEDIUMINT, "
      "data MEDIUMBLOB, "
      "PRIMARY KEY(house_id, room_id) );")

    Tables['house_devices'] = (
      "CREATE TABLE house_devices ("
      "house_id MEDIUMINT, "
      "device_id MEDIUMINT, "
      "device_type MEDIUMINT, "
      "data MEDIUMBLOB, "
      "PRIMARY KEY(house_id, device_id) );")

    Tables['room_devices'] = (
      "CREATE TABLE room_devices ("
      "house_id MEDIUMINT, "
      "room_id MEDIUMINT, "
      "device_id MEDIUMINT, "
      "device_type MEDIUMINT, "
      "data MEDIUMBLOB, "
      "PRIMARY KEY(house_id, room_id, device_id) );")

    # Actually create these tables.
    for name, ddl in Tables.iteritems():
      try:
        self._cur.execute("DROP TABLE IF EXISTS " + name)
        self._cur.execute(ddl);
      except mysql.connector.Error as err:
        print(err.msg)
        self._broken = True;
        return;


  # Internal. Format an insertion query to the house table.
  def __sql_insert_house(self, house):
    query = '''INSERT INTO %s VALUES (%d, '%s')''' % (
        self._house_table, house._house_id, house._data)
    print "insert_house Query: %s" % query
    self._cur.execute(query)


  # Internal. Format an insertion query to the house room table.
  def __sql_insert_house_room(self, room):
    query = '''INSERT INTO %s VALUES (%d, %d, '%s')''' % (
        self._hr_table, room._house_id, room._room_id, room._data)
    print "Room Query: %s" % query
    self._cur.execute(query)


  # Internal. Format an insertion query to the house device table.
  def __sql_insert_house_device(self, device):
    query = '''INSERT INTO %s VALUES (%d, %d, %d, '%s')''' % (
        self._hd_table, device._house_id, device._device_id,
        device._device_type, device._data)
    print "Device Query: %s" % query
    self._cur.execute(query)


  # Internal. Format an insertion query to the room device table.
  def __sql_insert_room_device(self, device):
    query = '''INSERT INTO %s VALUES (%d, %d, %d, %d, '%s')''' % (
        self._rd_table, device._house_id, device._room_id,
        device._device_id, device._device_type, device._data)
    print "Device Query: %s" % query
    self._cur.execute(query)


  # Insert a house into the SQL database.
  def insert_house(self, house):
    for room in house._rooms:
      self.insert_room(room)

    for device in house._devices:
      self.insert_house_device(device);

    self.__sql_insert_house(house)


  # Insert a room into the SQL database.
  def insert_room(self, room):
    for device in room._devices:
      self.insert_room_device(device);

    self.__sql_insert_house_room(room)


  # Insert a device associated with a house but no room.
  def insert_house_device(self, device):
    self.__sql_insert_house_device(device)


  # Insert a device associated with a room inside of a house.
  # Warning! Make sure room has room ID set.
  def insert_room_device(self, device):
    if (device._room_id == None):
      print device._data
      raise ValueError('Tried to insert a device into a room without room ID')
    self.__sql_insert_room_device(device)









  # NOT YET IMPLEMENTED.
  # Add an additional room to a house.
  def appendhr_room(self, house_id, room):
    self.insert_room(room)
    #self.insert_relation(self._hr_table, house_id, room._room_id)


  # NOT YET IMPLEMENTED.
  # Add an additional device to a house.
  def appendhd_device(self, house_id, device):
    self.insert_house_device(device)
    #self.insert_relation(self._hd_table, house._house_id, device._device_id)

  # NOT YET IMPLEMENTED.
  # Add an additional device to a room.
  def appendrd_device(self, room_id, device):
    self.insert_room_device(device);
    #self.insert_relation(self._rd_table, room._room_id, device._device_id)


  # NOT YET IMPLEMENTED
  def modify_house(self, house_id, house):
    return


  # NOT YET IMPLEMENTED
  def modify_room(self, room_id, room):
    return


  # NOT YET IMPLEMENTED
  def modify_device(self, device_id, device):
    return


  # NOT YET IMPLEMENTED
  def delete_house(self, house_id):
    return
  

  # NOT YET IMPLEMENTED
  def delete_room(self, room_id):
    return


  # NOT YET IMPLEMENTED
  def delete_device(self, device_id):
    return
