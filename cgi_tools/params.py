"""
CGI-Tools Python Package
Copyright (C) 2016 Assaf Gordon (assafgordon@gmail.com)
License: BSD (See LICENSE file)
"""
from tempfile import NamedTemporaryFile
from .http_responses import http_bad_request_error, http_server_error

def save_cgi_file_param(form,var_name,suffix=None):
    if not var_name in form:
        msg = "missing CGI file parameter '%s'" % (var_name)
        http_bad_request_error(msg)

    f = form[var_name]
    if not f.file:
        msg = "invalid '%s' parameter (expecting file-upload)" % (var_name)
        http_server_error(msg)

    local_fn=""
    remote_fn=f.filename
    try:
        if not suffix:
            suffix=""
        outf = NamedTemporaryFile(suffix=suffix,delete=False)
        local_fn = outf.name
        while 1:
            chunk = f.file.read(100000)
            if not chunk: break
            outf.write (chunk)
        outf.close()

        return (local_fn,remote_fn)
    except IOError as e:
        http_server_error("cgi file upload I/O error: %s" % (str(e)))
    except OSError as e:
        http_server_error("cgi file upload OS error: %s" % (str(e)))
