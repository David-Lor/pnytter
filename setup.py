import os
# noinspection PyUnresolvedReferences
from setuptools import setup, find_packages


VERSION = "$VERSION$"


with open("README.md", "r") as f:
    readme_content = f.read()


setup(
    name="pnytter",
    license="ISC",
    author="David Lorenzo",
    author_email="17401854+David-Lor@users.noreply.github.com",
    url="https://github.com/David-Lor/pnytter",
    download_url="https://github.com/David-Lor/pnytter/archive/main.zip",
    keywords=["twitter", "nitter", "scraper", "scraping"],
    install_requires=[],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10"
    ],
    description_file="README.md",
    license_files=["LICENSE.md"],
    long_description_content_type="text/markdown",

    version=VERSION,
    long_description=readme_content,
)
