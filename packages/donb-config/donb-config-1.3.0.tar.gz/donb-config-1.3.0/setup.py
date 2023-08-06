# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="donb-config",
    version="1.3.0",
    author="Don Beberto",
    author_email="bebert64@gmail.com",
    description="Creation of config files based on a yaml file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    package_data={"": ["py.typed"]},
    packages=setuptools.find_packages(where="."),
    extras_require={
        "yaml": ["ruamel.yaml"],
    }
)
