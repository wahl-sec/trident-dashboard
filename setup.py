#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as README:
    long_description = README.read()

setuptools.setup(
    name="trident-dashboard",
    version="0.1-DEV",
    author="Jacob Wahlman",
    description="Trident Dashboard: Visualize Trident",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/wahl-sec/trident-dashboard",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operation System :: OS Independent"
    ],
    python_requires=">=3.7",
    install_requires=[
        "flask"
    ],
    extras_require= {
        "dev": ["pytest", "setuptools", "wheel"]
    },
    include_package_data=True,
    zip_safe=False
)