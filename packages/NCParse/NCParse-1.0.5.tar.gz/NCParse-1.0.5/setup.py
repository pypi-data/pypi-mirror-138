from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.5'
DESCRIPTION = 'CNC G and M Code code parseer'
LONG_DESCRIPTION = long_description

# Setting up
setup(
    name="NCParse",
    version=VERSION,
    author="Marcus Cymerman",
    author_email="mpcymerman@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=['NCParse'],
    keywords=['python', 'CNC', 'GCode', 'MCode'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)