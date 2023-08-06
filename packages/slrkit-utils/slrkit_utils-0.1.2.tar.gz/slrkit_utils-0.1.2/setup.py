#!/usr/bin/env python
import pathlib

from setuptools import setup

__version__ = ''
package_name = 'slrkit_utils'

exec(open(pathlib.Path(package_name) / 'version.py').read())

setup(
    name=package_name,
    version=__version__
)
