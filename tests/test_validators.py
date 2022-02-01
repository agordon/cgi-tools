"""
CGI-Tools Python Package
Copyright (C) 2016-2022 Assaf Gordon (assafgordon@gmail.com)
License: BSD (See LICENSE file)
"""
import unittest

from cgi_tools import valid_int, valid_float, valid_regex, valid_in_list

class ValidatorsTests(unittest.TestCase):

    def test_valid_int(self):
        self.assertTrue(valid_int("123"))
        self.assertTrue(valid_int("0"))
        self.assertTrue(valid_int("-43"))
        self.assertTrue(valid_int(42))
        self.assertFalse(valid_int(""))
        self.assertFalse(valid_int(None))
        self.assertFalse(valid_int("a"))
        self.assertFalse(valid_int("43a"))
        self.assertFalse(valid_int("04.3"))
        self.assertFalse(valid_int("False"))

    def test_valid_float(self):
        self.assertTrue(valid_float("123"))
        self.assertTrue(valid_float("0"))
        self.assertTrue(valid_float("-43"))
        self.assertFalse(valid_float(""))
        self.assertFalse(valid_float(None))
        self.assertFalse(valid_float("a"))
        self.assertFalse(valid_float("43a"))
        self.assertTrue(valid_float("04.3"))
        self.assertFalse(valid_float("False"))

    def test_valid_regex(self):
        self.assertTrue (valid_regex("[a-z]", "a"))
        self.assertFalse(valid_regex("[a-z]", "A"))
        self.assertFalse(valid_regex("[a-z]", ""))
        self.assertFalse(valid_regex("[a-z]", "aa"))
        self.assertTrue (valid_regex("[a-z]+", "abfdvfdvafdasa"))
        self.assertFalse(valid_regex("[a-z]+", ""))
        self.assertFalse(valid_regex("[a-z]+", None))
        self.assertTrue (valid_regex("[_a-z][_a-z0-9]*", "da4324"))
        self.assertFalse(valid_regex("[_a-z][_a-z0-9]*", "4324"))

    def test_valid_in_list(self):
        self.assertTrue (valid_in_list("a",  ["a","b","c"]) )
        self.assertFalse(valid_in_list("",   ["a","b","c"]) )
        self.assertFalse(valid_in_list(None, ["a","b","c"]) )
        self.assertFalse(valid_in_list("d",  ["a","b","c"]) )

        self.assertTrue (valid_in_list(1, [1,2,3] ))


if __name__ == '__main__':
    unittest.main()
