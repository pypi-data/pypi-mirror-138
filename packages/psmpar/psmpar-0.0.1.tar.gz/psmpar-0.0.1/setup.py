#!/usr/bin/env python

from setuptools import setup
from os import path
import os
import codecs


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")
version = get_version("psmpar/__init__.py")

# long_description = ("psmpar is a machine learning model to predict secondary metabolism potential "
#                     "of a single bacteria strain or bacteria communities using 16S rRNA or amplicans.")

setup(name='psmpar',
      version=version,
      license="GPL",
      description=('psmpar: prediction of secondary metabolism potential using amplicons based on machine learning'),
      author = "Zhen-Yi Zhou",
      author_email="gavinchou64@gmail.com",
      url='https://github.com/BioGavin/ML-PSMPA.git',
      classifiers=["Programming Language :: Python :: 3.8",
                   "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
                   "Operating System :: OS Independent"],
      packages=['psmpar'],
      scripts=['script/psmpar'],
      # include_package_data=True,
      python_requires=">=3.8",
      # package_data={'psmpar': ['Rscripts/*.R',
      #                         'default_files/bacteria/*.gz',
      #                         'default_files/bacteria/pro_ref/*',
      #                         'default_files/psmpa2/*.tsv.gz',
      #                         'default_files/psmpa2/database/*' ]},
      # long_description=long_description
      )
