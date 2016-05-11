#!/usr/bin/env python
"""
CGI-Tools Python Package
Copyright (C) 2016 Assaf Gordon (assafgordon@gmail.com)
License: BSD (See LICENSE file)
"""

from cgi_tools import force_C_locale, set_resource_limits, set_app_code

def cgi_main():
    print "Content-Type: text/plain"
    print
    print "Hello World, cgi_tools imported!"


if __name__ == "__main__":
    set_app_code(2000)
    set_resource_limits(walltime=3)
    force_C_locale()
    cgi_main()
