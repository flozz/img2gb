#!/usr/bin/env python

import os

from setuptools import setup, find_packages


long_description = ""
if os.path.isfile("README.rst"):
    long_description = open("README.rst", "r").read()


setup(
    name="img2gb",
    version="1.1.0",
    description="Converts images to GameBoy tileset",
    url="",
    license="BSD-3-Clause",
    long_description=long_description,
    keywords="gb gameboy image tile tileset tilemap",
    author="Fabien LOISON",
    packages=find_packages(),
    setup_requires=["cffi>=1.0.0"],
    install_requires=[
        "pillow>=5.0.0",
    ],
    extras_require={
        "dev": [
            "nox",
            "flake8",
            "pytest",
            "black",
        ]
    },
    entry_points={
        "console_scripts": [
            "img2gb = img2gb.__main__:main",
        ],
    },
)
