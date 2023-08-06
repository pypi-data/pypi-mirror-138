from setuptools import setup, find_packages
import os

here = os.path.join(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), "r") as readme_file:
    LONG_DESCRIPTION = readme_file.read()

NAME = "lxe"
AUTHOR = "DaMuffin"
VERSION = "0.0.1"
DESCRIPTION = "lxe is a library that stores different xe files."
LICENSE = "MIT"

KEYWORDS = [
    "lxe",
    "lxe lib",
    "rxe",
    "sxe",
    "mxe",
    "python",
    "python3",
]
CLASSIFIERS = [
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Operating System :: Unix",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: Microsoft :: Windows",
]
REQUIRED_MODULES = ["wheel"]
EXCLUDED_MODULES = ()

setup(
    name=NAME,
    author=AUTHOR,
    version=VERSION,
    url="https://github.com/DaMuffinDev/lxe",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    install_requires=REQUIRED_MODULES,
    python_requires=">=3.10",
    keywords=KEYWORDS,
    classifiers=CLASSIFIERS,
    packages=find_packages(exclude=EXCLUDED_MODULES),
    include_package_data=True
)