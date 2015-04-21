import httplib
from sys import argv
script, req, cmd = argv[0:3]

# Extract body if there
body = None
if (len(argv) > 3):
  body = argv[3]

h1 = httplib.HTTPConnection('172.31.26.85:8080')

if body is None:
  print req, cmd
  h1.request(req, cmd)
else:
  print req, cmd, body
  h1.request(req, cmd, body)
print "status"
r1 = h1.getresponse()
print "got response"
d1 = r1.read()
print "got read"
print r1.status, d1
