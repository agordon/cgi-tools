#!/usr/bin/env python
"""
CGI-Tools Python Package
Copyright (C) 2016 Assaf Gordon (assafgordon@gmail.com)
License: BSD (See LICENSE file)
"""

from __future__ import print_function
import sys, os, cgi, re, locale, resource, time, signal
from jinja2 import Template
from subprocess import Popen, PIPE
from cgi_tools import force_C_locale, set_resource_limits, \
                      http_bad_request_error,  http_server_error, \
                      valid_regex, run_cmd_list

def valid_delta(v):
    return valid_regex("[-a-zA-Z0-9: \.\+]+",v)


def parse_cgi_params():
    """
    Extract CGI parameters, bail-out on any errors.
    """
    form = cgi.FieldStorage()

    delta = form.getfirst('d',None)
    if not valid_delta(delta):
        http_bad_request_error("invalid delta value (%s)" % (str(delta)))

    fmt = form.getfirst('f',"")
    if not (fmt in ["",'8601','2822','3339']):
        http_bad_request_error("invalid format value (%s)" % (str(fmt)))

    return (delta,fmt)


def run_gnu_date(delta,fmt):
    cmd = ["date" ]
    if fmt:
        cmd.append(fmt)
    cmd.append("-d")
    cmd.append("now " + str(delta))
    (ok, _, out, err) = run_cmd_list(cmd)
    return (ok, out, err)


def cgi_main():
    """
    Main script: get CGI parameters, return HTML content.
    """

    (delta, fmt) = parse_cgi_params()

    if not fmt or len(str(fmt).strip())==0:
        fmt_string = "(default)"
        fmt = None
    elif fmt=='8601':
        fmt_string = "iso-8601"
        fmt = "--iso-8601=seconds"
    elif fmt=='2822':
        fmt_string = "rfc-2822"
        fmt = "--rfc-2822"
    elif fmt=='3339':
        fmt_string = "rfc-3339"
        fmt = "--rfc-3339=seconds"
    else:
        # should never happen
        http_server_error("internal error: invalid fmt (%s)" % (str(fmt)))

    (date_ok,date_result,date_error) = run_gnu_date(delta,fmt)
    #NOTE: if date failed, the jinja2 template below will
    #      display the error - so we don't terminate with server-error.

    print ("Content-Type: text/html")
    print ("")

    html_tmpl="""
    <html>
    <body>
      Hello from Python CGI Script (Program Execution Example)
      <br/>
      <br/>

      Time Delta: <b>now (and) {{ delta }}</b>
      <br/>

      Output Format: {{ fmt_string }}
      <br/>
      <br/>

      Result:
       {% if date_ok %}
         <b><code>{{date_result}}</code></b>
       {% else %}
         Failed to run date:
         <b><code>{{ date_error }}</b></code>
       {% endif %}
      </body>
    </html>
    """
    tmpl = Template(html_tmpl)
    html = tmpl.render(delta=delta,fmt_string=fmt_string,
                       date_ok=date_ok, date_result=date_result,
                       date_error=date_error)
    print (html)



if __name__ == "__main__":
    set_resource_limits(walltime=4)
    force_C_locale()
    cgi_main()
