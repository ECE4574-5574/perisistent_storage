class Device:
  def __init__(self, house_id, device_id, device_type, data, room_id=None):
    self._house_id = house_id
    if (room_id != None):
      self._room_id = room_id
    self._device_id = device_id
    self._device_type = device_type
    self._data = data


class Room:
  def __init__(self, house_id, room_id, data, devices):
    self._house_id = house_id
    self._room_id = room_id
    self._data = data

    self._devices = []
    if not (devices is None):
      for device in devices:
        self._devices.append(device)


class House:
  def __init__(self, house_id, data, rooms, devices):
    self._house_id = house_id
    self._data = data

    self._rooms = []
    if not (rooms is None):
      for room in rooms:
        self._rooms.append(room)

    self._devices = []
    if not (devices is None):
      for device in devices:
        self._devices.append(device)


class User:
  def __init__(self, user_id, data):
    self._user_id = user_id
    self._data = data
