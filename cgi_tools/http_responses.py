"""
CGI-Tools Python Package
Copyright (C) 2016-2022 Assaf Gordon (assafgordon@gmail.com)
License: BSD (See LICENSE file)
"""
from __future__ import print_function
import sys, random, os
from functools import reduce

req_code = ""

def set_app_code(app_code):
    global req_code
    req_code = int(app_code) + random.uniform(0,1)


# Get 4 random bytes, convert to unsigned 32-bit int, use as seed.
v = [ord(os.urandom(1)) for x in range(4)]
s = reduce(lambda x,y: x*y, v)
random.seed(s)
# Set default application code + random request code
set_app_code(512)


def log(*args):
    """ Write MSG to STDERR """
    prefix = "request %s: " % str(req_code)
    msg = prefix + ' '.join(map(str, args))
    #TODO: protect against non ASCII output
    #      (also against invalid UTF-8)
    print (msg, file=sys.stderr)


def log_req_info():
    # TODO: print request information (remote_addr, query_string)
    pass

def http_error(http_code,http_status,msg):
    """
    Send an error code + status to the HTTP server,
    and log the error on STDERR as well,
    then terminate the script with exit-code 1.

    http_code: int ( 40X = client errors, 50X = server errors)
    http_status: text message
    msg: any text

    Message is always sent as plain-text content.
    """
    log ("returned HTTP error %d (%s): %s" % (http_code, http_status, msg))
    print ("Status: %d %s" % (http_code, http_status))
    print ("Content-Type: text/plain")
    print ("")
    prefix = "request %s: " % str(req_code)
    msg = prefix + msg
    print (msg)
    sys.exit(1)



def http_bad_request_error(msg):
    """
    Shortcut for sending client errors (HTTP 400/Bad Request)
    """
    http_error(400,"Bad Request",msg)



def http_server_error(msg):
    """
    Shortcut for sending server errors (HTTP 500)
    """
    http_error(500,"Internal Server Error",msg)
