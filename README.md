# Intro
This is an educational CLI program to learn web scraping and Python.

IT DOES NOT HOST ANYTHING.

# How to run it
## Android
### Installation

Step 1: Download Termux from fdroid and install it.

Step 2: Copy and paste 
```
pkg update
termux-setup-storage
pkg install python git x11-repo tur-repo chromium
git clone https://github.com/aatihonora/bookcli/
cd bookcli
pip install -r android_requirements.txt
python bookcli.py
```
### Already installed
```
cd bookcli
python bookcli.py
```
## Window/Linux
### Installation

Step 1: You must have Windows 10 or above and this is a guide for Ubuntu.

Step 2: Only for Window, copy and paste the code below in cmd as admin to install window subsystem linux.
```
wsl --install
```
Step 3: Now write wsl to set it up.

Step 4: From here linux and windows have same process, use these commands to properly install it.
```
sudo apt update
sudo apt install python3 chromium-browser git
git clone https://github.com/aatihonora/bookcli/
cd bookcli
pip install -r win_linux_requirements.txt
python bookcli.py
```
### Already installed
```
cd bookcli
python bookcli.py
```

# Supported Websites 
## Books
1. Libgen 
2. Anna's Archive

## Manga
1. Bato.to
2. Mangasee
3. ComicExtra

## Anime
1. TokyoInsider
2. Nyaa.si
3. Kayoanime


