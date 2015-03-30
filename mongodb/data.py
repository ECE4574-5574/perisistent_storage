import datetime

#*****************************************************
# Sample data for computer action
# Note that the assumptive structure of JSON data is:
	# "Computer_Log": {
	# 	"TIMEFRAME":
	# 	"USERID":
	# 	"HOUSEID":
	# 	"ROOM": [{"ROOMID":
	# 	          "DEVICE":[{"DEVICETYPE": 
	# 					     "DEVICENAME": 
	# 						 "DEVICEID":
	# 						 }
	# 						{"DEVICETYPE":
	# 						 "DEVICENAME":
	# 						 "DEVICEID": 
	# 						 }]
	# 			 }
	# 			 {"ROOMID":
	# 	          "DEVICE":[{"DEVICETYPE": 
	# 					     "DEVICENAME": 
	# 						 "DEVICEID":
	# 						 }
	# 						{"DEVICETYPE":
	# 						 "DEVICENAME":
	# 						 "DEVICEID": 
	# 						 }]
	# 			 }
	# 			]
	# }
#**********************************

computer_action_sample0 = {
	"Computer_Log": {
		"TIMEFRAME": datetime.datetime(2015, 2, 20, 10, 17, 13),
		"USERID": "Mike",
		"HOUSEID": "001",
		"ROOM": [{"ROOMID": "001",
		          "DEVICE":[{"DEVICETYPE": "Light",
						     "DEVICENAME": "light1",
							 "DEVICEID": "300",
							 "Status": "on"}, 
							{"DEVICETYPE": "Light",
							 "DEVICENAME": "light2",
							 "DEVICEID": "302",
							 "Status": "on"},
							{"DEVICETYPE": "Window",
							 "DEVICEID": "101",
							 "Status": "closed"}]}
				]
	}
}

computer_action_sample1 = {
	"Computer_Log": {
		"TIMEFRAME": datetime.datetime(2015, 3, 13, 8, 10, 5),
		"USERID": "Harry",
		"HOUSEID": "001",
		"ROOM": [{"ROOMID": "002",
		          "DEVICE":[{"DEVICETYPE": "Light",
						     "DEVICENAME": "light1",
							 "DEVICEID": "303",
							 "Status": "on"}, 
							{"DEVICETYPE": "Light",
							 "DEVICENAME": "light2",
							 "DEVICEID": "304",
							 "Status": "on"},
							{"DEVICETYPE": "Window",
							 "DEVICEID": "100",
							 "Status": "closed"}]}
		]
	}
}

computer_action_sample2 = {
	"Computer_Log": {
		"TIMEFRAME": datetime.datetime(2014, 11, 20, 14, 25, 20),
		"USERID": "Jack",
		"HOUSEID": "001",
		"ROOM": [{"ROOMID": "003",
		          "DEVICE":[{"DEVICETYPE": "Light",
						     "DEVICENAME": "light1",
							 "DEVICEID": "306",
							 "Status": "on"}, 
							{"DEVICETYPE": "Light",
							 "DEVICENAME": "light2",
							 "DEVICEID": "307",
							 "Status": "on"},
							{"DEVICETYPE": "Door",
							 "DEVICEID": "104",
							 "Status": "closed"}]}
		]
	}
}

computer_action_sample3 = {
	"Computer_Log": {
		"TIMEFRAME": datetime.datetime(2014, 11, 14, 9, 46, 2),
		"USERID": "Rick",
		"HOUSEID": "001",
		"ROOM": [{"ROOMID": "004",
		          "DEVICE":[{"DEVICETYPE": "Light",
						     "DEVICENAME": "light1",
							 "DEVICEID": "309",
							 "Status": "on"}, 
							{"DEVICETYPE": "TV",
							 "DEVICENAME": "tv1",
							 "DEVICEID": "201",
							 "Status": "on"},
							{"DEVICETYPE": "Door",
							 "DEVICEID": "105",
							 "Status": "closed"}]},
				 {"ROOMID": "007",
		          "DEVICE":[{"DEVICETYPE": "Thermostat",
						     "DEVICENAME": "Nest",
							 "DEVICEID": "403",
							 "TEMPERATURE": "70"}
							]}
				]
	}
}

computer_action_sample4 = {
	"Computer_Log": {
		"TIMEFRAME": datetime.datetime(2015, 3, 23, 0, 0, 0),
		"HOUSEID": "001",
		"ROOM": [{"ROOMID": "001",
		          "DEVICE":[{"DEVICETYPE": "Light",
						     "DEVICENAME": "light1",
							 "DEVICEID": "300",
							 "Status": "on"}, 
							{"DEVICETYPE": "Light",
							 "DEVICENAME": "light2",
							 "DEVICEID": "302",
							 "Status": "on"},
							{"DEVICETYPE": "Door",
							 "DEVICEID": "102",
							 "Status": "closed"}]},
				 {"ROOMID": "002",
		          "DEVICE":[{"DEVICETYPE": "Light",
						     "DEVICENAME": "light1",
							 "DEVICEID": "303",
							 "Status": "on"}, 
							{"DEVICETYPE": "Light",
							 "DEVICENAME": "light2",
							 "DEVICEID": "304",
							 "Status": "on"},
							{"DEVICETYPE": "Door",
							 "DEVICEID": "103",
							 "Status": "closed"}]},
				 {"ROOMID": "003",
		          "DEVICE":[{"DEVICETYPE": "Light",
						     "DEVICENAME": "light1",
							 "DEVICEID": "306",
							 "Status": "on"}, 
							{"DEVICETYPE": "Light",
							 "DEVICENAME": "light2",
							 "DEVICEID": "307",
							 "Status": "on"},
							{"DEVICETYPE": "Door",
							 "DEVICEID": "104",
							 "Status": "closed"}]},
				 {"ROOMID": "004",
		          "DEVICE":[{"DEVICETYPE": "Light",
						     "DEVICENAME": "light1",
							 "DEVICEID": "309",
							 "Status": "on"}, 
							{"DEVICETYPE": "Light",
							 "DEVICENAME": "light2",
							 "DEVICEID": "310",
							 "Status": "on"},
							{"DEVICETYPE": "Door",
							 "DEVICEID": "105",
							 "Status": "closed"}]}
				 ]
	}
}