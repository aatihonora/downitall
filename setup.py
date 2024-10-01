'''Setup'''
import os
import subprocess
from pathlib import Path

from setuptools import setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Set a reasonable umask.
os.umask(0o022)
# Make all local files readable and all directories listable.
subprocess.call(['chmod', '-R', 'a+rX', '.'])

setup(
    name="downitall",
    version='1.0',
    description='A cli to download and stream all kind of media',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Behram Akhtar/Aatiho Nora',
    author_email='behramakhtar@gmail.com',
    packages=['downitall', 'downitall.resources'],  #same as name
    package_data={'': ['license.txt', 'vlc']},
    include_package_data=True,
    install_requires=['requests', 'bs4', 'selenium', 'pandas', 'cbz-generator', 'tqdm', 'gdown', 'term-image', 'questionary', 'yt-dlp', 'xdcc-dl', 'streamlink', 'm3u-ipytv'], #external packages as dependencies
    scripts=['bin/downitall', 'bin/vlc'],
)
