#!/usr/bin/env python3
"""
CGI-Tools Python Package
Copyright (C) 2016-2022 Assaf Gordon (assafgordon@gmail.com)
License: BSD (See LICENSE file)
"""

from __future__ import print_function
import sys, os, cgi, re, locale, resource, time, signal
from jinja2 import Template
from subprocess import Popen, PIPE
from cgi_tools import force_C_locale, set_resource_limits, \
                      http_bad_request_error, \
                      set_app_code, get_cgi_first_non_empty_param

def parse_cgi_params():
    """
    Extract CGI parameters, bail-out on any errors.
    """
    form = cgi.FieldStorage()
    text = get_cgi_first_non_empty_param(form, ['text_str','text_file'])
    return text



def cgi_main():
    """
    Main script: get CGI parameters, return HTML content.
    """

    text = parse_cgi_params()

    #note: these counts are different than wc's definition
    #      of chars/lines/words
    chars = len(text)
    lines = len(text.split('\n'))
    words = len(text.split())

    print ("Content-Type: text/plain")
    print ("")
    print ("%d characters" % chars)
    print ("%d words" % words)
    print ("%d lines" % lines)
    print ("\n\nText Below:\n")
    print (text)



if __name__ == "__main__":
    set_app_code(125)
    set_resource_limits(walltime=4)
    force_C_locale()
    cgi_main()
