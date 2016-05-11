"""
CGI-Tools Python Package
Copyright (C) 2016 Assaf Gordon (assafgordon@gmail.com)
License: BSD (See LICENSE file)
"""
import re
from .http_responses import http_server_error
from .types import to_str_list

def valid_regex(regex,value):
    """
    """
    if not value:
        return False
    if len(str(value).strip())==0:
        return False
    t = re.compile("^" + regex +"$")
    if not t.match(value):
        return False
    return True


def valid_int(i):
    """
    """
    if not i:
        return False;
    try:
        i = int(i)
        return True
    except ValueError as e:
        return False;


def valid_float(i):
    """
    """
    if not i:
        return False;
    try:
        i = float(i)
        return True
    except ValueError as e:
        return False;


def valid_in_list(v,l):
    """
    returns TRUE if str(v) is in list.
    returns FALSE otherwise.
    returns FALSE if v is None, or empty string.
    """
    l = to_str_list(l)
    if v is None:
        return False
    v = str(v).strip()
    if not v:
        return False
    return v in l
