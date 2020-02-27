#!/usr/bin/env python

import sys

from setuptools import find_packages, setup

assert sys.version_info >= (3, 6, 0), "choose-place requires Python 3.6+"

setup(
    name="choose-place",
    version="1.0.0",
    description="Choose places for lunch/dinner/etc",
    author="Maurice Bailleu",
    url="https://github.com/mbailleu/lunch",
    packages=["choose_place"],
    package_data={"choose_place": ["data/*.csv", "templates/*.html"]},
    entry_points={"console_scripts": ["choose-place = choose_place:main"]},
    install_requires=["flask"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Utilities",
        "Programming Language :: Python :: 3.6",
    ],
)
