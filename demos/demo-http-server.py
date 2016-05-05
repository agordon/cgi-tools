#!/usr/bin/env python

"""
CGI-Tools Python Package
Copyright (C) 2016 Assaf Gordon (assafgordon@gmail.com)
License: BSD (See LICENSE file)
"""

import BaseHTTPServer
import CGIHTTPServer
import sys, os


# locale the package's directory, and add it to PYTOHNPATH
# (for the CGI scripts to find it)
dir=os.path.dirname(__file__)
if len(dir)==0:
    dir="." # darn python, that's no how dirname supposed to work!
dir=os.path.abspath(dir)
pdir=os.path.join(dir,'..') # parent directory
sdir=os.path.join(pdir,'cgi_tools') # package directory
if not os.path.exists(sdir):
    sys.exit("error: can't find package directory '%s'" % sdir)
pp = os.environ.get('PYTHONPATH','')
os.environ['PYTHONPATH'] = pdir + ":" + pp

# cd into the script's directory
# (there's an 'index.html' in it)
os.chdir(dir)

# Run the server
server = BaseHTTPServer.HTTPServer
handler = CGIHTTPServer.CGIHTTPRequestHandler
server_address = ("127.0.0.1", 8888)
handler.cgi_directories = ["/cgi-bin"]
httpd = server(server_address, handler)

print "Visit http://%s:%s to see CGI demos" % server_address
httpd.serve_forever()
