#!/usr/bin/env python
"""
CGI-Tools Python Package
Copyright (C) 2016 Assaf Gordon (assafgordon@gmail.com)
License: BSD (See LICENSE file)
"""

from __future__ import print_function
import sys, os, cgi
from cgi_tools import force_C_locale, set_resource_limits, \
                      check_run_cmd_list,  save_cgi_file_param


def get_cgi_params():
    """
    Extract CGI parameters, bail-out on any errors.
    """
    form = cgi.FieldStorage()
    (local,remote) = save_cgi_file_param(form,"datafile",".cgi-file-checksum")
    return (local,remote)


def run_checksum(filename):
    cmd = ["sha1sum",filename]
    (out, err) = check_run_cmd_list(cmd)
    # return the first whitespace-delimited field (the checksum value)
    return out.split()[0]


def cgi_main():
    """
    Main script: get CGI parameters, return HTML content.
    """

    (local,remote) = get_cgi_params()
    cksum = run_checksum(local)
    os.unlink(local)

    print ("Content-Type: text/plain")
    print ("")
    print ("sha1 checksum of: %s = %s" % (str(remote),str(cksum)))


if __name__ == "__main__":
    set_resource_limits(walltime=2,filesize=1024*1024)
    force_C_locale()
    cgi_main()
