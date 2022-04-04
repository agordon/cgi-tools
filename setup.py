"""
CGI-Tools Python Package
Copyright (C) 2016-2022 Assaf Gordon (assafgordon@gmail.com)
License: BSD (See LICENSE file)
"""

from setuptools import setup
from detect_version import detect_version

setup(
    name = "cgi-tools",
    version = detect_version("cgi_tools"),
    author = "Assaf Gordon",
    author_email = "AssafGordon@gmail.com",

    description = "Collection of tools for quick CGI scripts development",
    long_description="",

    license = "BSD",
    keywords = "CGI",
    url = "https://github.com/agordon/cgi-tools",
    packages=['cgi_tools'],
    scripts=['bin/jinja2-cgi'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: BSD License",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    install_requires=[
          'jinja2',
          'werkzeug'
    ],
    test_suite = 'tests',
)
