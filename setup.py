import os
# noinspection PyUnresolvedReferences
from setuptools import setup, find_packages


version_file = os.getenv("VERSION_FILE", "").strip()
version = os.getenv("VERSION", "").strip()

if version_file and not version:
    with open(version_file, "r") as f:
        version = f.read().strip()

if not version:
    raise Exception("No version found")


setup(
    name="pnytter",
    version=version,
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
    ]
)
