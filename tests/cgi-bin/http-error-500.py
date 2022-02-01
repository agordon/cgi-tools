#!/usr/bin/env python3
"""
CGI-Tools Python Package
Copyright (C) 2016-2022 Assaf Gordon (assafgordon@gmail.com)
License: BSD (See LICENSE file)
"""

from cgi_tools import force_C_locale, set_resource_limits, set_app_code, \
                      http_server_error

def cgi_main():
    http_server_error("test script, failing on purpose")

if __name__ == "__main__":
    set_app_code(2001)
    set_resource_limits(walltime=3)
    force_C_locale()
    cgi_main()
