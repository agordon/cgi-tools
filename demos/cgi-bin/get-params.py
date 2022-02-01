#!/usr/bin/env python3
"""
CGI-Tools Python Package
Copyright (C) 2016-2022 Assaf Gordon (assafgordon@gmail.com)
License: BSD (See LICENSE file)
"""

from __future__ import print_function
import sys, cgi, re
from jinja2 import Template
from cgi_tools import force_C_locale, set_resource_limits, \
                      http_bad_request_error,  http_server_error, \
                      valid_int, valid_regex

def parse_cgi_params():
    """
    Extract CGI parameters, bail-out on any errors.
    returns a tuple of the validated values.
    """
    form = cgi.FieldStorage()

    name = form.getfirst('name',None)
    if not valid_regex("[a-z]+",name):
        http_bad_request_error("invalid name value (%s)" % (str(name)) );
    age =  form.getfirst('age',None)
    if not valid_int(age):
        http_bad_request_error("invalid age value (%s)" % (str(age)) );

    return (name, age)


def cgi_main():
    """
    Main script: get CGI parameters, return HTML content.
    """

    (name, age) = parse_cgi_params()

    print ("Content-Type: text/html")
    print ("")

    html_tmpl="""
    <html>
    <body>
    Hello from Python CGI Script
    <br/>
    <br/>
    Your name: <b>{{ name }}</b>
    <br/>
    You age: <b>{{ age }}</b>
    </body>
    </html>
    """
    tmpl = Template(html_tmpl)
    html = tmpl.render(name=name, age=age)
    print (html)



if __name__ == "__main__":
    set_resource_limits(walltime=4)
    force_C_locale()
    cgi_main()
