"""
CGI-Tools Python Package
Copyright (C) 2016 Assaf Gordon (assafgordon@gmail.com)
License: BSD (See LICENSE file)
"""

from setuptools import setup

setup(
    name = "cgi-tools",
    version = "0.0.1",

    author = "Assaf Gordon",
    author_email = "AssafGordon@gmail.com",

    description = ("Collection of tools for quick CGI scripts development"),
    long_description=""" """,

    license = "BSD",
    keywords = "CGI",
    url = "",
    packages=['cgi_tools'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: BSD License",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries"
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    test_suite = 'tests',
)
