# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
__version__ = "1.23.1"

setup(
    name="nanocomp",
    version=__version__,  # noqa F821
    description="Comparing runs of Oxford Nanopore sequencing data and alignments",
    long_description=open(path.join(here, "README.md")).read(),
    long_description_content_type="text/markdown",
    url="https://github.com/oschleifer/nanocomp",
    author="adapted from Wouter De Coster",
    author_email="decosterwouter@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ],
    keywords="nanopore sequencing plotting quality control",
    packages=find_packages() + ["scripts"],
    python_requires=">=3",
    install_requires=[
        "pandas",
        "numpy>=1.16.5",
        "nanoget>=1.19.0",
        "nanomath>=1.0.0",
        "NanoPlot>=1.39.0",
        "psutil",
        "plotly>=3.4.2",
        "pyarrow",
    ],
    package_data={"nanocomp": []},
    package_dir={"nanocomp": "nanocomp"},
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "nanocomp=nanocomp.NanoComp:main",
        ],
    },
)
