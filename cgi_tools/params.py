"""
CGI-Tools Python Package
Copyright (C) 2016 Assaf Gordon (assafgordon@gmail.com)
License: BSD (See LICENSE file)
"""
from tempfile import NamedTemporaryFile
from .http_responses import http_bad_request_error, http_server_error, log
from .types import to_str_list

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



def get_cgi_first_non_empty_param(form,param_names):
    """
    For HTML forms which allow EITHER uploading a file or pasting text, e.g.:

       <form method="POST" enctype="multipart/form-data" action="[URL]">
           paste input:
           <br/>
           <textarea name="text_str" rows="10" cols="50"></textarea>
           <br/>
           or upload  a file:
           <input type="file" name="text_file" />
           <br/>
           <input type="submit" value="go" />
       </form>

    Calling
       a = get_cgi_first_non_empty_param(form,['text_str','text_file'])

    Will return the content of either the text from the <textarea>
    or the content of the uploaded file.

    The first non-empty parameter is returned.

    If all are empty, an HTTP 400 (bad request) error is returned.

    NOTE:
    The returned value is not necessarily valid text (could be UTF-8,
    invalid UTF-8, other encoding, or binary data).
    """
    param_names = to_str_list (param_names)

    for p in param_names:
        text = form.getfirst(p,"")
        if len(text)>0:
            return text

    l = ','.join(param_names)
    http_bad_request_error("at least one CGI parameters must be non-empty: "+l)
