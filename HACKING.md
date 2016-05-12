
Registering a new package
-------------------------

See fantastic tutorial at: http://peterdowns.com/posts/first-time-with-pypi.html

prepare PyPi config file (with updated passwords):

    $ cat ~/.pypirc
    [distutils]
    index-servers =
       pypi
       pypitest

    [pypi]
    repository=https://pypi.python.org/pypi
    username=agn
    password=xxx

    [pypitest]
    repository=https://testpypi.python.org/pypi
    username=agn
    password=xxx

Register on PyPiTest first:

    python setup.py register -r pypitest

If all went well, register on PyPi:

    python setup.py register -r pypi

Making a new release
--------------------

1. Tag a new version. Uploading to PyPi requires
   a clean public version, without a private version part
   (see PEP-440 for details).
   So `0.0.4` is OK, while `0.0.4-7-gab12-dirty` will be rejected
   by PyPi.

        git tag -a "0.0.2" -m "version 0.0.2"

    Ensure the new version is properly detected and used:

        $ ./detect_version.py cgi_tools
        0.0.2

2. Test upload to PyPiTest:

        $ python setup.py sdist upload -r pypitest
        [...]
        Writing cgi-tools-0.0.2/setup.cfg
        Creating tar archive
        removing 'cgi-tools-0.0.2' (and everything under it)
        running upload
        Submitting dist/cgi-tools-0.0.2.tar.gz to https://pypi.python.org/pypitest
        Server response (200): OK

3. If upload went well, upload to PyPi

        python setup.py sdist upload -r pypi

4. Push changes to github, including tags (if your remote is `origin`,
    replace `github` below):

        git push github master
        git push github --tags

