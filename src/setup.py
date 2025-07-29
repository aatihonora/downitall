"""Setup"""

import os
import subprocess
from pathlib import Path

from setuptools import setup

this_directory = Path(__file__).parent
long_description = (this_directory / "Readme.md").read_text()

# Set a reasonable umask.
os.umask(0o022)
# Make all local files readable and all directories listable.
subprocess.call(["chmod", "-R", "a+rX", "."])

setup(
    name="downitall_windows",
    version="1.5",
    description="A cli to download and stream all kind of media",
    author="Behram Akhtar/Aatiho Nora",
    author_email="behramakhtar@gmail.com",
    packages=["downitall", "downitall.resources"],
    package_data={"": ["license.txt"]},
    include_package_data=True,
    install_requires=[
        "requests==2.32.4",
        "bs4==0.0.2",
        "selenium==4.9.1",
        "selenium-wire==5.1.0",
        "blinker==1.7.0",
        "cbz-generator==1.0.0",
        "tqdm==4.67.1",
        "gdown==5.2.0",
        "term-image==0.7.2",
        "questionary==2.1.0",
        "ytmusicapi==1.10.3",
        "xdcc-dl==5.2.1",
        "streamlink==7.5.0",
        "m3u-ipytv==0.2.11",
        "setuptools==80.9.0",
        "yt-dlp==2025.6.30",
        "pandas",
    ],  # external packages as dependencies
    scripts=["bin/downitall"],
)
