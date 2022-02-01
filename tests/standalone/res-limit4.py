"""
CGI-Tools Python Package
Copyright (C) 2016-2022 Assaf Gordon (assafgordon@gmail.com)
License: BSD (See LICENSE file)

Limit runtime to 1 second of %100 CPU time,
then run an external program which waste CPUs.

The child program will get SIGXCPU and will terminate (coredump).
This script (the parent) will get see a non-zero exitcode.
"""

import os
from cgi_tools import set_resource_limits, run_cmd_list

set_resource_limits(walltime=10,cputime=1)

cmd = ["sh","-c","seq inf>/dev/null"]
(ok,exitcode,out,err) = run_cmd_list( cmd )

print("ok = ",ok)
print("exitcode = ", exitcode)
print("out = ",out)
print("err = ",err)

# The program's exit code should not be zero
if ok:
    sys.exit("set_resource_limits failed to limit external program's cputime")

if exitcode==0:
    sys.exit("set_resource_limits failed to limit external program's cputime")

print("set_resource_limits successfully restricted external program's cputime")
