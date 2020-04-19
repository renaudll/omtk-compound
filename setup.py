#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="omtk_compound",
    version="0.1",
    description="Lightweight encapsulation framework for Autodesk Maya",
    author="Renaud Lessard Larouche",
    author_email="sigmao@gmail.com",
    url="https://github.com/renaudll/omtk_compound",
    packages=find_packages(where="scripts"),
    package_dir={"": "scripts"},
    install_requires=[],
    extras_require={"test": ["pytest", "pytest-cov", "mock"], "doc": ["sphinx"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Topic :: Multimedia :: Graphics",
    ],
)