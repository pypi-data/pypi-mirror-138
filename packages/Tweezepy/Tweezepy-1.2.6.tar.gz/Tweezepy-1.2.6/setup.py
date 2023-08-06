# -*- coding: utf-8 -*-
"""
Created on Tue May  5 16:31:29 2020

Author: Ian L. Morgan
email: ilmorgan@ucsb.edu
"""
import setuptools
import os
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setuptools.setup(name="Tweezepy",
                 version="1.2.6",
                 author="Ian L. Morgan",
                 author_email="ilmorgan@ucsb.edu",
                 description="Single-molecule force spectroscopy calibration",
                 url="https://github.com/ianlmorgan/tweezepy",
                 license="GPLv3",
                 packages=setuptools.find_packages(),
                 include_package_data=True,
                 python_requires = ">=3.6, !=3.10.*",
                 long_description=long_description,
                 long_description_content_type = 'text/markdown',
                 install_requires = ["autograd",
                                     "corner",
                                     "emcee",
                                     "matplotlib",
                                     "numba",
                                     "numpy>=1.15",
                                     "scipy",
                                     ],
                 setup_requires = ["setuptools>=40.6.0"],
                 tests_require=["unittest"],
                 classifiers=["Intended Audience :: Science/Research",
                              "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
                              "Operating System :: OS Independent",
                              "Programming Language :: Python :: 3.6",
                              "Programming Language :: Python :: 3.7",
                              "Programming Language :: Python :: 3.8",
                              "Programming Language :: Python :: 3.9",
                              "Topic :: Scientific/Engineering",
                              ],
                 project_urls = {"Documentation" : "https://tweezepy.readthedocs.org"}
                 ) 