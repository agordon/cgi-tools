#!/usr/bin/env python3
"""
CGI-Tools Python Package
Copyright (C) 2016-2022 Assaf Gordon (assafgordon@gmail.com)
License: BSD (See LICENSE file)
"""

from jinja2 import Template
import platform

sysdata = [ platform.machine(),
            platform.node(),
            platform.processor(),
            platform.system() ]

pydata = [ platform.python_implementation(),
           platform.python_version() ]

print "Content-Type: text/html"
print                           # blank line, end of headers


# Generate response HTML using Jinja2 Templating system
html_tmpl="""
<html>
<head>
Hello from Python CGI Script
<br/>
<br/>
System Data: <code>{{ system_data }}</code>
<br/>
<br/>
Python Data: <code>{{ python_data }}</code>
</body>
</html>
"""

tmpl = Template(html_tmpl)
html = tmpl.render(system_data = sysdata,
                   python_data = pydata)

print html
