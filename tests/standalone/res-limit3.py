# Limit runtime to 1 second of %100 CPU time,
# then waste CPU cycles for a long time.

# SIGXCPU exception is expeccted, which is caught and the script terminated
# while printing HTTP error message.

import math,sys
from cgi_tools import set_resource_limits

set_resource_limits(walltime=10,cputime=1)

for i in xrange(0,sys.maxint):
    a = math.sqrt(i)
