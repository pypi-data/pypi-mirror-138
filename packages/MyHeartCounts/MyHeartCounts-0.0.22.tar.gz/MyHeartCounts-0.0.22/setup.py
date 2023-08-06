#!/usr/bin/env python
import setuptools

__version__ = "0.0.22"


CLASSIFIERS = [
    "Development Status :: Development in progress",
    "Intended Audience :: Lab members of Ashley lab and anyone with access to My Heart Counts Synapse and Amazon Web Services data",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3.9",
    "Topic :: Scientific/Engineering :: Data Analysis",
    "Topic :: Scientific/Engineering :: Machine Learning",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

setuptools.setup(
    name="MyHeartCounts",
    version=__version__,
    description="Python wrapper to load and analyze studies on My Heart Counts App",
    long_description = "",
    author="A. Javed",
    author_email="alijaved@live.com",
    packages=setuptools.find_packages(),
    zip_safe=True,
    license="",
    download_url = "https://github.com/AshleyLab/MyHeartCounts2.0/archive/refs/tags/v0.0.22.tar.gz",
    url="https://github.com/AshleyLab/MyHeartCounts2.0",
    install_requires=['numpy','synapseclient','datetime','pandas']
)
