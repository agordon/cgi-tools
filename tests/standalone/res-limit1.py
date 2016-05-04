# Limit walltime to 1 second, then sleep for 2 seconds.
#
# a SIGALRM is expected, which is caught and the script terminates
# with HTTP error printed.
from time import sleep
from cgi_tools import set_resource_limits

set_resource_limits(walltime=1,cputime=10)
sleep(2)
