TODO List
=========

* Get version from git (but also package version in dist)
* Documentation
    * Describe scripts
    * Docstring exported functions (https://www.python.org/dev/peps/pep-0257/)
* version 2: use pythonian idioms
* add resource tests
    * file size limits
    * file descriptors limits
    * memory limits
* Document command-line usage:
    * HTTP GET requests:

        ```
        curl 'http://localhost:8888/cgi-bin/get-params.py?name=foo&age=43'
        curl 'http://localhost:8888/cgi-bin/get-params.py?name=foo&age=XXX'

        curl 'http://localhost:8888/cgi-bin/gnu-date-delta.py?d=2+years'
        ```

    * HTTP POST requests:

        ```
        curl -F name=foo -F age=43 http://localhost:8888/cgi-bin/get-params.py
        curl -F age=43     http://localhost:8888/cgi-bin/get-params.py
        curl -F name=XXXX  http://localhost:8888/cgi-bin/get-params.py

        curl -F d="2 years - 3 days" http://localhost:8888/cgi-bin/gnu-date-delta.py
        ```
* Explain setting up a tiny container with Busybox's HTTPD + local-unix sockets.
    * Mention `curl -H "Expect:"` for faster busybox POST requests.
* Catch-all for exceptions, send back server-error
