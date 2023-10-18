Things to do while releasing a new version
==========================================

This file is a memo for the maintainer.


1. Release
----------

* Update version number in ``setup.py``
* Update version number in ``img2gb/version.py``
* Edit / update changelog in ``README.rst``
* Commit / tag (``git commit -m vX.Y.Z && git tag vX.Y.Z && git push && git push --tags``)


2. Publish PyPI package
-----------------------

Automated :)


3. Windows standalone version
-----------------------------

* Use a fresh Windows VM with Git Bash installed
* run ``./scripts/build-windows.sh``


4. Publish Github Release
-------------------------

* Make a release on Github
* Add changelog
* Add Windows standalone executable
