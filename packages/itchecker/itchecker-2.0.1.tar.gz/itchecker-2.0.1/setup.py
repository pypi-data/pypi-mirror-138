# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""

import re

from pip._internal.req import parse_requirements
from setuptools import setup

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('itchecker/console_tool.py').read(),
    re.M
).group(1)

with open("README.rst", "rb") as f:
    long_descr = f.read().decode("utf-8")

install_reqs = parse_requirements('itchecker/requirements.txt', session='hack')
reqs = [str(ir.requirement) for ir in install_reqs]

setup(
    name="itchecker",
    packages=["itchecker"],
    entry_points={
        "console_scripts": ['itchecker = itchecker.console_tool:main']
    },
    package_data={'': ['templates/*', 'requirements.txt']},
    version=version,
    description="Python command line application bare bones template.",
    long_description=long_descr,
    author="itolymp",
    author_email="it@itolymp.com",
    install_requires=reqs,
)
