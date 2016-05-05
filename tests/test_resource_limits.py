"""
CGI-Tools Python Package
Copyright (C) 2016 Assaf Gordon (assafgordon@gmail.com)
License: BSD (See LICENSE file)
"""
import unittest

from time import sleep
import math, os, sys

from cgi_tools import run_cmd_list

#export PYTHONPATH based on sys.path
pythonpath = ':'.join(sys.path)
if 'PYTHONPATH' in os.environ:
    pythonpath = pythonpath + ":" + os.environ['PYTHONPATH']
os.environ['PYTHONPATH'] = pythonpath

# find script's directory
# (to determine the directory of the 'standalone' scripts)
standalone_dir=os.path.join(os.path.dirname(__file__),"standalone")


class ResourceLimitTests(unittest.TestCase):

    def test_res_limit1(self):
        script = os.path.join(standalone_dir,"res-limit1.py")
        cmd = ["python", script ]
        (ok,exitcode,out,err) = run_cmd_list(cmd)

        self.assertFalse(ok)
        self.assertNotEqual(exitcode,0)
        self.assertIn("wall-time", out)
        self.assertIn("wall-time", err)

    def test_res_limit2(self):
        script = os.path.join(standalone_dir,"res-limit2.py")
        cmd = ["python", script ]
        (ok,exitcode,out,err) = run_cmd_list(cmd)

        self.assertFalse(ok)
        self.assertNotEqual(exitcode,0)
        self.assertIn("wall-time", out)
        self.assertIn("wall-time", err)

    def test_res_limit3(self):
        script = os.path.join(standalone_dir,"res-limit3.py")
        cmd = ["python", script ]
        (ok,exitcode,out,err) = run_cmd_list(cmd)

        self.assertFalse(ok)
        self.assertNotEqual(exitcode,0)
        self.assertIn("cpu-time", out)
        self.assertIn("cpu-time", err)

    def test_res_limit4(self):
        script = os.path.join(standalone_dir,"res-limit4.py")
        cmd = ["python", script ]
        (ok,exitcode,out,err) = run_cmd_list(cmd)

        self.assertTrue(ok)
        self.assertEqual(exitcode,0)

if __name__ == '__main__':
    unittest.main()
