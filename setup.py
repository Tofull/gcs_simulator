#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md") as readme_file:
    readme = readme_file.read()

with open("requirements.txt") as requirements_file:
    requirements = requirements_file.read().splitlines()


setup(
    name="gcs_simulator",
    version="0.0.1",
    description="Simulator of Google Cloud Storage python API using local folder as 'bucket'.",
    long_description=readme,
    author="Loïc Messal",
    author_email="loic.messal@jakarto.com",
    url="https://github.com/tofull/gcs_simulator",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.7",
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
)
