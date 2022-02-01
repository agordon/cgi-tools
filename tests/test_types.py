"""
CGI-Tools Python Package
Copyright (C) 2016-2022 Assaf Gordon (assafgordon@gmail.com)
License: BSD (See LICENSE file)
"""
import unittest

from time import sleep
import math, os

from cgi_tools.types import is_string, is_iterable, to_str_list

class TypesTests(unittest.TestCase):
    def test_is_string(self):
        self.assertTrue ( is_string( "hello"    ) )
        self.assertTrue ( is_string( ""         ) )
        self.assertFalse( is_string( None       ) )
        self.assertFalse( is_string( 1          ) )
        self.assertFalse( is_string( 13.41      ) )
        self.assertFalse( is_string( ["hello"]  ) )
        self.assertFalse( is_string( ("hello",) ) )
        self.assertFalse( is_string( {"hello":"world"}) )
        self.assertFalse( is_string( len        ) )

    def test_is_iterable(self):
        self.assertTrue ( is_iterable( [1,2,3]      ) )
        self.assertTrue ( is_iterable( range(0,10)  ) )
        #self.assertTrue ( is_iterable( xrange(0,10) ) )
        self.assertTrue ( is_iterable( (1,2,3)      ) )
        self.assertTrue ( is_iterable( (1,)         ) )
        self.assertTrue ( is_iterable( "hello"      ) )
        self.assertFalse( is_iterable( None         ) )
        self.assertFalse( is_iterable( 1.43         ) )
        self.assertFalse( is_iterable( 1            ) )
        self.assertFalse( is_iterable( len          ) )


    def test_to_str_list(self):
        self.assertEqual( to_str_list("a"),           ["a"] )
        self.assertEqual( to_str_list(["a"]),         ["a"] )
        self.assertEqual( to_str_list(("a",)),        ["a"] )
        self.assertEqual( to_str_list([1,"2",3]),     ["1","2","3"] )



if __name__ == '__main__':
    unittest.main()
