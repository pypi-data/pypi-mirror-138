import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pynchaosDump",
    version = "0.0.1",
    author = "Andrea Michelotti",
    author_email = "andrea.michelotti@lnf.infn.it",
    description = ("Dumps dataset of !CHAOS to local disk"),
    license = "BSD",
    keywords = "!CHAOS utility",
    install_requires = ['confluent_kafka','bson'],
    # url = "http://packages.python.org/an_example_pypi_project",
    # packages=['pynchaosDump'],
   # long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ]
)