"""
CGI-Tools Python Package
Copyright (C) 2016-2022 Assaf Gordon (assafgordon@gmail.com)
License: BSD (See LICENSE file)
"""
import unittest

from time import sleep
import math, os

from cgi_tools import force_C_locale, set_resource_limits, \
                      run_cmd_list, check_run_cmd_list

class SystemTests(unittest.TestCase):

    def test_force_C_locale(self):
        ## For now, just test that it doesn't crash
        force_C_locale()


    def test_resource_limit(self):
        ## For now, just test that it doesn't crash
        set_resource_limits(cputime=1000, walltime=1000)


    def test_run_cmd_list_1(self):
        # run a simple command that succeeds
        (ok, exitcode, out, err) = run_cmd_list( ["uname","-s"] )
        self.assertTrue(ok)
        self.assertEqual(exitcode, 0)
        self.assertEqual(err,"")  # STDERR should be empty
        self.assertNotEqual(out,"") # STDOUT should not be empty


    def test_run_cmd_list_2(self):
        # run a simple command that fails
        (ok, exitcode, out, err) = run_cmd_list( ["uname","-Q"] )
        self.assertFalse(ok)
        self.assertNotEqual(exitcode, 0)
        self.assertEqual(out,"")    # STDOUT should be empty
        self.assertNotEqual(err,"") # STDERR should not be empty


    def test_run_cmd_list_3(self):
        # run a non-existing command, run_cmd_list should call sys.exit().
        # Python's sys.exit() is translated to SystemExit exception,
        # so trap it, and ensure the exit-code is non-zero)
        with self.assertRaises(SystemExit) as cm:
            run_cmd_list( ["foo-Bar-BAZ","--help"] )

        self.assertNotEqual(cm.exception.code,0)


    def test_run_cmd_list_4(self):
        # A single string is valid (if it's the only command)
        (ok, exitcode, out, err) = run_cmd_list( "date" )
        self.assertTrue(ok)
        self.assertEqual(exitcode, 0)
        self.assertEqual(err,"")    # STDERR should be empty
        self.assertNotEqual(out,"") # STDOUT should not be empt


    def test_run_cmd_list_5(self):
        # A list with a single item is valid
        (ok, exitcode, out, err) = run_cmd_list( ["uptime"] )
        self.assertTrue(ok)
        self.assertEqual(exitcode, 0)
        self.assertEqual(err,"")    # STDERR should be empty
        self.assertNotEqual(out,"") # STDOUT should not be empt


    def test_run_cmd_list_6(self):
        # Prevent programming errors: a single shell command line shouldn't work.
        with self.assertRaises(SystemExit) as cm:
            run_cmd_list( "uname -a" )

        self.assertNotEqual(cm.exception.code,0)

    def test_run_cmd_list_7(self):
        # Ensure STDIN is redirected from /dev/null.
        # sha1sum from /dev/null is known (and should return immediately).
        # if STDIN is wrongly redirected (or connected to the terminal's),
        # the program will timeout.
        (ok, exitcode, out, err) = run_cmd_list( ["timeout","2","sha1sum"] )
        self.assertTrue(ok)
        self.assertEqual(exitcode, 0)
        self.assertEqual(err,"")    # STDERR should be empty
        out = out.strip()
        self.assertEqual(out,"da39a3ee5e6b4b0d3255bfef95601890afd80709  -")


    def test_check_run_cmd_list_1(self):
        # run a simple command that succeeds
        (out, err) = check_run_cmd_list( ["uname","-s"] )
        self.assertEqual(err,"")  # STDERR should be empty
        self.assertNotEqual(out,"") # STDOUT should not be empty


    def test_check_run_cmd_list_2(self):
        # run a simple command that fails
        with self.assertRaises(SystemExit) as cm:
            (out, err) = check_run_cmd_list( ["uname","-Q"] )


if __name__ == '__main__':
    unittest.main()
