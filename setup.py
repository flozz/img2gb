#!/usr/bin/env python

import os

from setuptools import setup, find_packages


long_description = ""
if os.path.isfile("README.rst"):
    long_description = open("README.rst", "r", encoding="UTF-8").read()


setup(
    name="img2gb",
    version="1.3.0",
    description="Converts images to GameBoy tileset",
    url="https://github.com/flozz/img2gb",
    project_urls={
        "Source Code": "https://github.com/flozz/img2gb",
        "Issues": "https://github.com/flozz/img2gb/issues",
        "Chat": "https://discord.gg/P77sWhuSs4",
        "Donate": "https://github.com/flozz/img2gb#support-this-project",
    },
    license="BSD-3-Clause",
    long_description=long_description,
    keywords="gb gameboy image tile tileset tilemap",
    author="Fabien LOISON",
    packages=find_packages(),
    install_requires=[
        "pillow>=5.0.0",
    ],
    extras_require={
        "dev": [
            "nox",
            "flake8",
            "pytest",
            "black",
            "sphinx",
            "sphinx-rtd-theme",
        ]
    },
    entry_points={
        "console_scripts": [
            "img2gb = img2gb.__main__:main",
        ],
    },
)
