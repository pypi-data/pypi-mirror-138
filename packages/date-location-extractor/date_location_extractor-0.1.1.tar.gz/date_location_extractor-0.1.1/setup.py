"""Setup script for date_location_extractor"""

import pathlib

from setuptools import setup

HERE = pathlib.Path(__file__).resolve().parent

README = (HERE / "README.md").read_text()

setup(
    name="date_location_extractor",
    version="0.1.1",
    description="Extract date and location from a list of strings",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/elitepc/date_location_extractor",
    author="elitepc",
    author_email="",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=["date_location_extractor"],
    include_package_data=True,
    install_requires=[
        "datefinder>=0.7.1",
        "geotext>=0.4.0",
        "python-dateutil>=2.8.2"
    ],
    tests_require=[
        "pytest>=7.0.1"
    ],
)
