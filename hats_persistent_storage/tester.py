import httplib
from sys import argv
script, req, cmd = argv[0:3]

# Extract body if there
body = None
if (len(argv) > 3):
  body = argv[3]

h1 = httplib.HTTPConnection('52.11.96.207:8080')

if body is None:
  print req, cmd
  h1.request(req, cmd)
else:
  print req, cmd, body
  h1.request(req, cmd, body)
r1 = h1.getresponse()
d1 = r1.read()
print r1.status, d1
