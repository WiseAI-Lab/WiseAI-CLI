#!/usr/bin/env python
import io
from setuptools import setup, find_packages

PROJECT = "wiseai"

with io.open("README.md", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name=PROJECT,
    version="0.0.1",
    description="Deploy the WiseAgent through command line interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="DongboX",
    author_email="sfreebobo@gmail.com",
    url="https://github.com/WiseAI-Lab/wiseai_cli",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    platforms=["Any"],
    scripts=[],
    provides=[],
    install_requires=requirements,
    namespace_packages=[],
    include_package_data=True,
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "wiseai = wiseai.main:main"
        ]
    },
    zip_safe=False,
)
