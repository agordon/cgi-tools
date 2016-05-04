# Limit runtime to 1 second, then run an external command that runs for longer.
# SIGALRM exception is expeccted, which is caught and the script terminated
# while printing HTTP error message.

import os
from cgi_tools import set_resource_limits

set_resource_limits(walltime=1,cputime=10)
os.system("sleep 3")
