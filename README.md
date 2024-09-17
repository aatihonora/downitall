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
pkg install -y python git openssl x11-repo tur-repo aria2 wget
pkg install -y chromium python-pandas
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
sudo apt install python3 chromium-browser git aria2 wget
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

1. Libgen [Books]
2. Anna's Archive [Books] [Selenium]
3. 1337x [Books] [Courses] [Torrent]

## Manga

1. Bato.to [Manhwa/Manhua]
2. Mangasee [Manga] [Selenium]
3. ComicExtra [Comic]

## Anime

1. TokyoInsider [Anime]
2. Nyaa.si [Anime] [Torrent]
3. Kayoanime [Anime]

## TV-Series/Movies

1. Vadapav [TV-Series/Movies]
2. 1337x [TV-Series/Movies] [Torrent]
3. DocumentayTop [Documentaries] [Torrent]

## Music

1. Lightaudio [Tracks]
2. Bomb-music [Tracks]
3. PlayerFM [Podcasts]
