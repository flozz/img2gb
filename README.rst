img2gb - Converts Images to GameBoy Tileset and Tilemap
=======================================================

|GitHub| |Lint and Tests| |PYPI Version| |License| |Discord| |Black|

    img2gb generates GameBoy Tilesets and Tilemaps from standard image (PNG,
    JPEG,...). It converts the images into the GameBoy image format and
    generates C code (``.c`` and ``.h`` files) that can be used in GameBoy
    projects.

.. image:: ./doc/_static/banner.png

* Documentation: https://flozz.github.io/img2gb/
* HowTo: https://flozz.github.io/img2gb/howto.html


Dependencies
------------

* Python >= 3.9
* Pillow >= 5.0


Install
-------

* See https://flozz.github.io/img2gb/install.html


Usage
-----

* See https://flozz.github.io/img2gb/cli.html


Hacking
-------

Setup
~~~~~

To work on img2gb first create a virtualenv::

    python3 -m venv __env__

and activate it::

    source __env__/bin/activate

Then install the project with all dev dependencies::

    pip install -e .[dev]


Commands
~~~~~~~~

You can lint the code and check coding style with::

    nox -s lint

You can fix coding style using Black with::

    nox -s black_fix

You can run test on all supported Python versions or on a specific Python
version with::

    nox -s test       # Run on all Python version

    nox -s test-3.9   # Run on Python 3.9
    nox -s test-3.10  # Run on Python 3.10
    nox -s test-3.11  # Run on Python 3.11
    nox -s test-3.12  # Run on Python 3.12
    nox -s test-3.12  # Run on Python 3.13

And you can build the documentation with (result in ``build/html/``)::

    nox -s gendoc


Links
-----

* Examples of GameBoy programs that uses img2gb for graphics:
  * https://github.com/flozz/gameboy-examples/tree/master/05-graphics2
  * https://github.com/flozz/gameboy-examples/tree/master/06-graphics3-background
* Article about the tile encoding and img2gb: https://blog.flozz.fr/2018/11/19/developpement-gameboy-5-creer-des-tilesets/ (French)


Support this project
--------------------

Want to support this project?

* `☕️ Buy me a coffee <https://www.buymeacoffee.com/flozz>`__
* `💵️ Give me a tip on PayPal <https://www.paypal.me/0xflozz>`__
* `❤️ Sponsor me on GitHub <https://github.com/sponsors/flozz>`__


Changelog
---------

* **[NEXT]** (changes on ``master``, but not released yet):

  * Nothing yet ;)

* **v1.3.0:**

  * feat: Added binary export of tilesets and tilemaps (@duysqubix, #44)
  * misc: Added Python 3.13 support (@flozz)
  * misc!: Removed Python 3.8 support (@flozz)

* **v1.2.0:**

  * fix: Fixed wrong version displayed (@flozz, #3)
  * chore: Added Python 3.11 and 3.12 support
  * chore!: Removed Python 2.7 and 3.7 support

* **v1.1.0:**

  * Removes arbitrary size limit for tilmaps
  * Implements ``offset`` option (#2)

* **v1.0.0:**

  * Refacto of the Python API, with new high-level fuction to be easier to use
  * Refacto of the CLI: now tileset and tilemap are generated separately, this allow more options for both and covers more usecases.
  * New option to handle alternative palette
  * New option to handle 8x16px sprites
  * Documentation
  * Unit test (everything is not coverd but it is better than nothing :))

* **v0.10.0:** Adds non-RGB image support (indexed images,...)
* **v0.9.1:** Fixes an issue with Python 3
* **v0.9.0:** Initial release (generates tiles, tilesets and tilemaps)


.. |GitHub| image:: https://img.shields.io/github/stars/flozz/img2gb?label=GitHub&logo=github
   :target: https://github.com/flozz/img2gb

.. |Lint and Tests| image:: https://github.com/flozz/img2gb/actions/workflows/python-ci.yml/badge.svg
   :target: https://github.com/flozz/img2gb/actions

.. |PYPI Version| image:: https://img.shields.io/pypi/v/img2gb.svg
   :target: https://pypi.python.org/pypi/img2gb

.. |License| image:: https://img.shields.io/pypi/l/img2gb.svg
   :target: https://github.com/flozz/img2gb/blob/master/LICENSE

.. |Discord| image:: https://img.shields.io/badge/chat-Discord-8c9eff?logo=discord&logoColor=ffffff
   :target: https://discord.gg/P77sWhuSs4

.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://black.readthedocs.io/en/stable
