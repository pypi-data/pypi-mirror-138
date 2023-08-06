# copied from https://github.com/adrienverge/yamllint/
from setuptools import setup

from pyeit import (
    __author__,
    __author_email__,
    __license__,
    APP_NAME,
    APP_VERSION,
    APP_DESCRIPTION,
)


setup(
    name=APP_NAME,
    version=APP_VERSION,
    author=__author__,
    author_email=__author_email__,
    description=APP_DESCRIPTION.split("\n")[0],
    long_description=APP_DESCRIPTION,
    license=__license__,
)
