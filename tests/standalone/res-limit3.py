"""
CGI-Tools Python Package
Copyright (C) 2016-2022 Assaf Gordon (assafgordon@gmail.com)
License: BSD (See LICENSE file)

Limit runtime to 1 second of %100 CPU time,
then waste CPU cycles for a long time.

SIGXCPU exception is expeccted, which is caught and the script terminated
while printing HTTP error message.
"""

import math,sys
from cgi_tools import set_resource_limits

set_resource_limits(walltime=10,cputime=1)

for i in range(0,sys.maxsize):
    a = math.sqrt(i)
