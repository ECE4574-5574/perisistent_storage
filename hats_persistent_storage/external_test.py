import httplib
from sys import argv
#script, req, cmd = argv[0:3]

# Extract body if there
body = None
if (len(argv) > 3):
  body = argv[3]

h1 = httplib.HTTPConnection('172.31.26.85:8083')

ok = 1
h1.request("POST", "H", "house1")
r1 = h1.getresponse()
if (r1.status != 200):
  print "Error: Can't post house"
  ok = 0
r1.read()

h1.request("POST", "U", "user1")
r1 = h1.getresponse()
if (r1.status != 200):
  print "Error: Can't post user"
  ok = 0
r1.read()

if not ok:
  print "Errors found. There are issues"
