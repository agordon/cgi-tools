"""
CGI-Tools Python Package
Copyright (C) 2016 Assaf Gordon (assafgordon@gmail.com)
License: BSD (See LICENSE file)
"""
import unittest

import os, sys, copy, urllib,re, StringIO
from pprint import pprint
from subprocess import Popen,PIPE


# find script's directory
# (to determine the directory of the 'standalone' scripts)
tests_dir=os.path.join(os.path.dirname(__file__))
tests_dir=os.path.abspath(tests_dir)

# Add this directory to PYTHONPATH
# (need to be absolute path, since cwd is changed before
#  executing the cGI script)
pythonpath_dir=os.path.dirname(tests_dir)
if not os.path.isdir(os.path.join(pythonpath_dir,"cgi_tools")):
    raise RuntimeError("can't find 'cgi_tools' directory - tests will fail")

class FakeCGIResponse:
    def __init__(self, http_code, http_status, headers, content):
        self.http_code = http_code
        self.http_status = http_status
        self.headers = headers
        self.content = content

        self.content_as_file = StringIO.StringIO(content)

    def getcode(self):
        return self.http_code

    def read(self,size=None):
        return self.content_as_file.read(size)

    def readline(self,size=None):
        return self.content_as_file.readline(size)

    def readlines(self,size=None):
        return self.content_as_file.readlines(size)

    def __iter__(self):
        return self.content_as_file.__iter__()



class CGIScriptTests(unittest.TestCase):

    def run_cgi_script(self,cgi_script_file,get_params={},
                       remote_addr="127.0.0.1",
                       remote_port="1234",
                       remote_host="bar.example.com",
                       remote_user=None,
                       server_name="foo.example.com",
                       server_port="80",
                       http_host="foo.example.com",
                       http_referer=None,
                       http_user_agent="cgi_tools_client_simulator"):
        """Runs a script as if it's a webserver invoking a CGI script
        by emulating the required CGI environment variables.

        Currently supports only GET parameteres.

        NOTE:
        1. The 'cgi_script_file' should contain a filename only (not path),
           and the file is expected to exist under ./tests/cgi-bin/ .

        2. This web-server simulator can only handle small input and
           output sizes (all are buffered in memory).
        """

        script_abs_path = os.path.join(tests_dir,'cgi-bin',cgi_script_file)
        if not os.path.isfile(script_abs_path):
            raise RuntimeError("internal test error: cgi script file '%s'" \
                               " not found" % (cgi_script_file))

        st = os.stat(script_abs_path)
        if st.st_mode & 0100 == 0:
            raise RuntimeError("internal test error: cgi script file '%s'" \
                               " is not executable" % (cgi_script_file))



        env = {} #copy.deepcopy(os.environ)

        # Ensure CGI scripts can find the 'cgi_tool' module
        ppath = pythonpath_dir + ":" + os.environ.get('PYTHONPATH','')
        env['PYTHONPATH'] = ppath

        # PATH is needed incase 'python' itself is not in the
        # standard directories
        env['PATH'] = os.environ.get('PATH','')

        env['SERVER_SOFTWARE'] = "cgi_tools_server_simulator"
        env['GATEWAY_INTERFACE'] = 'CGI/1.1'
        env['SERVER_NAME'] = server_name
        env['SERVER_PORT'] = server_port

        env['REMOTE_HOST'] = remote_host
        env['REMOTE_ADDR'] = remote_addr
        env['REMOTE_PORT'] = remote_port
        if remote_user:
            env['REMOTE_USER'] = remote_user

        env['HTTP_HOST'] = http_host
        if http_referer:
            env['HTTP_REFERER'] = http_referer
        if http_user_agent:
            env['HTTP_USER_AGENT'] = http_user_agent
        #TODO:
        #env['HTTP_COOKIE'] = ""

        # Currently, only GET is supported
        env['REQUEST_METHOD'] = "GET"

        # TODO: fill these
        env['PATH_INFO'] = ""
        env['PATH_TRANSLATED'] = ""

        env['SCRIPT_NAME'] = os.path.basename(cgi_script_file)

        # TODO: for POST
        # env['CONTENT_TYPE'] = ""
        # env['CONTENT_LENGTH'] = ""

        # Build query string
        query = urllib.urlencode (get_params)
        if query:
            env['QUERY_STRING'] = query

        cwd = os.path.dirname(script_abs_path)

        # TODO: change when adding POST
        devnull = open("/dev/null",'r')

        print "Simulating CGI script: %s (in '%s')" % (cgi_script_file, cwd)

        p = Popen([script_abs_path], shell=False,
                  env=env, cwd=cwd, stdin=devnull, stdout=PIPE, stderr=PIPE)

        (out,err) = p.communicate()
        print "CGI returned exit code: ", p.returncode

        if err:
            print "CGI printed to STDERR:"
            print "====="
            print err
            print "====="

        if out:
            print "CGI returned information (STDOUT):"
            print "====="
            print out
            print "====="

        ## Parse the returned information for the CGI script,
        ## minimally emulating the HTTP web server.
        d = out.split('\n')
        d = [x.strip('\r') for x in d]

        ## Split into HTTP headers and content
        headers = []
        content = []
        header_mode = True
        status = None
        for l in d:
            if header_mode:
                # A single empty line separates header from content.
                if len(l)==0:
                    header_mode = False
                    continue

                # CGI script sent a custom status, don't assume 200
                if l.startswith("Status: "):
                    status = l[8:]
                    continue
                headers.append(l)
            else:
                content.append(l)

        if not status:
            # CGI script did not sent status, assume HTTP 200
            status = "200 OK"

        print "Detected HTTP Status:", status
        status_code = re.search("^([0-9]+) ", status)
        if not status_code:
            raise RuntimeError("internal test error: cgi script file '%s'" \
                               " returned invalid status '%s'" \
                               % (cgi_script_file, status))

        r = FakeCGIResponse(int(status_code.group(1)),
                            status, headers, '\n'.join(content))
        return r


    def test_cgi_server(self):
        """Ensure the test CGI server works.
        Try to fetch the simple cgi shell script."""

        r = self.run_cgi_script("simple.sh")
        self.assertEqual ( r.getcode(), 200 )


    def test_cgi_import(self):
        """Ensure the test CGI scripts can import cgi_tools package"""
        r = self.run_cgi_script("import-test.py" )
        self.assertEqual ( r.getcode(), 200 )


    def test_cgi_script_err_500(self):
        """test http_server_error()"""
        r = self.run_cgi_script("http-error-500.py" )
        self.assertEqual ( r.getcode(), 500 )


    def test_cgi_script_err_400(self):
        """test http_bad_request_error()"""
        r = self.run_cgi_script("http-error-400.py" )
        self.assertEqual ( r.getcode(), 400 )



if __name__ == '__main__':
    unittest.main()
