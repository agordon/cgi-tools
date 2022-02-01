#!/usr/bin/env python3
"""
CGI-Tools Python Package
Copyright (C) 2016-2022 Assaf Gordon (assafgordon@gmail.com)
License: BSD (See LICENSE file)
"""

from __future__ import print_function
import sys, cgi, math
from cgi_tools import force_C_locale, set_resource_limits, set_app_code

def waste_time():
    """use %100 of the CPU for a really long time"""
    for i in xrange(0,sys.maxint):
        a = math.sqrt(i)

def cgi_main():
    waste_time()

    print ("Content-Type: text/plain")
    print ("")
    print ("If you see this message, the script failed")


if __name__ == "__main__":
    set_app_code(123)
    # Allow 10 seconds of wall-time, and 1 second of cputime.
    set_resource_limits(walltime=10,cputime=1)
    force_C_locale()
    cgi_main()
