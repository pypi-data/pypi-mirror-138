#!/usr/bin/env python
import pathlib
from setuptools import setup, find_packages
from rel import __version__
PKG_NAME = 'ns-rep-imports'
VERSION = __version__
PKG_MAIN = 'rel'

# The directory containing this file
HERE = pathlib.Path(__file__).parent
# The text of the README file
with open(HERE / "README.rst") as fh:
    README = fh.read()

PACKAGES = find_packages(exclude=['build', 'dist', 'env', 'cmd', 'tmp'])

# This call to setup() does all the work
setup(
    name=PKG_NAME,
    version=VERSION,
    python_requires='>=3.6.0',
    description="Namespace Realitive Import Generator",
    long_description_content_type="text/x-rst",
    long_description=README,
    url="https://github.com/Amourspirit/python-ns-rel-imports",
    author=":Barry-Thomas-Paul: Moss",
    author_email='bigbytetech@gmail.com',
    license="MIT",
    packages=PACKAGES,
    keywords=['import', 'namespace', 'rel', 'camel-to-snake'],
    install_requires=[
          'kwargshelper >= 2.7.1',
      ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    include_package_data=True,
)
