"""
CGI-Tools Python Package
Copyright (C) 2016-2022 Assaf Gordon (assafgordon@gmail.com)
License: BSD (See LICENSE file)
"""


# Find the string type, in python2/python3 compatbile way
string_type = None
try:
    # Python 2 has 'basestring'
    string_type = basestring
except NameError:
    # Python 3 has 'str'
    string_type = str



def is_string(x):
    """Returns TRUE if X is a string object"""
    return isinstance(x, string_type)



def is_iterable(x):
    """Returns TRUE if X is iterable.
    (returns TRUE also for strings)
    """
    try:
        _ = iter(x)
        return True
    except TypeError as e:
        return False
    # other exceptions can occur, but we let them propagate
    # as they are indication of other problems.



def to_str_list(arg):
    """returns a list of strings based on input values.

    if the arg is a single string, returns a list with a single item.
    if the arg is a list (or other iterables), returns a list with
    stringified items.

    examples:
    to_str_list("hello") => ["hello"]
    to_str_list(["hello"]) => ["hello"]
    to_str_list(["hello",42]) => ["hello","42"]

    """

    # String is a special case: it's iterable, but we don't want to iterate
    # the individual characters
    if is_string(arg):
        return [arg]

    # TODO: Handle locale/charset str() conversion errors
    if is_iterable(arg):
        return list(map(str,arg))

    return [str(arg)]
