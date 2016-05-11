"""
CGI-Tools Python Package
Copyright (C) 2016 Assaf Gordon (assafgordon@gmail.com)
License: BSD (See LICENSE file)
"""
from __future__ import print_function
import sys, os, cgi, re, locale, resource, time, signal
from subprocess import Popen, PIPE
from .types import is_string, is_iterable, to_str_list

from .http_responses import http_server_error, log

def alarm_signal_handler(signum, frame):
    http_server_error("server error: wall-time limit reached")

def xcpu_signal_handler(signum, frame):
    http_server_error("server error: cpu-time limit reached")

def xfsz_signal_handler(signum, frame):
    http_server_error("server error: file-size limit reached")


def set_resource_limits(walltime=3,cputime=1,filesize=10000,
                        nice=10):
    """
    Self-imposed limits - reduce risk of abuse.
    Adjust values as needed (per script/scenario)

    walltime   = max. seconds of walltime
    cputime    = max. seconds of cputime (not wall time)
    filesize   = in bytes, per-process
    nice       = nice level
    """

    max_nofile   = 30        # num. of open descriptors, per process
    max_data     = 50000000  # in bytes, per-process (when using brk/sbrk)
    max_vmem     = 100000000 # in bytes, per-process (when mmap)

    try:
        signal.signal(signal.SIGALRM, alarm_signal_handler)
        signal.signal(signal.SIGXFSZ, xfsz_signal_handler)
        signal.signal(signal.SIGXCPU, xcpu_signal_handler)

        # Allow +1 for hard-limit - thus this script will receive
        # SIGXCPU/SIGXFSZ and will terminate cleanly (with HTTP error
        # returned)
        resource.setrlimit(resource.RLIMIT_CPU,    (cputime,cputime+1))
        resource.setrlimit(resource.RLIMIT_FSIZE,  (filesize,filesize*2))
        resource.setrlimit(resource.RLIMIT_NOFILE, (max_nofile,max_nofile+1))
        resource.setrlimit(resource.RLIMIT_DATA,   (max_data,max_data))

        # Max. wall time limit. SIGALRM will be triggered if expired.
        signal.alarm(walltime)

        # use AS as alternative to VMEM if the attribute isn't defined.
        # http://stackoverflow.com/a/30269998/5731870
        # http://git.savannah.gnu.org/cgit/bash.git/tree/builtins/ulimit.def#n154
        if hasattr(resource,'RLIMIT_VMEM'):
            resource.setrlimit(resource.RLIMIT_VMEM,(max_vmem,max_vmem))
        elif hasattr(resource,'RLIMIT_AS'):
            resource.setrlimit(resource.RLIMIT_AS,  (max_vmem,max_vmem))

        os.nice(nice)
    except resource.error as e:
        http_server_error("failed to set resource limits (%s)" % (str(e)))
    except OSError as e:
        http_server_error("failed to renice (%s)" % (str(e)))


def force_C_locale():
    """
    Force C/POSIX locale for this script, and all executed children.
    """
    locale.setlocale(locale.LC_ALL,'C')
    os.environ["LC_ALL"] = 'C'
    os.environ["LC_LANG"] = 'C'
    os.environ["LANG"] = 'C'
    os.environ["LANGUAGE"] = 'C'
    os.environ["LC_CTYPE"] = 'C'

    #TODO: consider this (with ignoring non-ascii output)
    #sys.stdout = codecs.getwriter('ascii')(sys.stdout)



def run_cmd_list(cmd):
    cmd = to_str_list(cmd)

    msg = ' '.join(cmd)
    log ("executing: " + msg)

    try:
        devnull = open('/dev/null','r')
        p = Popen(cmd,shell=False,stdin=devnull,stdout=PIPE,stderr=PIPE)
        devnull.close()
        (out,err) = p.communicate()
        ## NOTE:
        ## returned values are not necessarily ASCII, or even valid text/utf/etc.
        ## ALWAYS sanitize output.
        ## Python (at least v2) has severe problems handling non-ascii
        ## characters without extra processing.
        return ( p.returncode==0, p.returncode, out, err )
    except IOError as e:
        http_server_error("failed to execute '%s': IOError: %s" % (str(cmd[0]), str(e)))
    except OSError as e:
        http_server_error("failed to execute '%s': %s" % (str(cmd[0]), str(e)))


def check_run_cmd_list(cmd):
    cmd = to_str_list(cmd)

    (ok,exitcode,out,err) = run_cmd_list(cmd)
    if not ok:
        http_server_error("command '%s' returned error (exit code %d)" % \
                          (cmd[0],exitcode))
    return (out,err)
