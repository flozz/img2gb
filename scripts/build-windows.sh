#!/bin/bash

if [ ! -d __env__ ] ; then
    python -m virtualenv __env__
    . __env__/Scripts/activate
    pip install -e .
    pip install pyinstaller
else
    . __env__/Scripts/activate
fi

pyinstaller \
    --onefile \
    --name img2gb-$(python setup.py --version) \
    scripts/img2gb_win.py
