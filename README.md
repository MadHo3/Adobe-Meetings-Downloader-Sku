# 📥 Adobe Meetings Downloader SKU

> **ابزار خودکار دانلود و تبدیل جلسات ضبط‌شده Adobe Connect مخصوص دانشجویان دانشگاه شهرکرد (SKU)**

[![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FFmpeg](https://img.shields.io/badge/dependency-ffmpeg-orange.svg)](https://ffmpeg.org/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)]()

---

| [English](README.md) | [Persian](README_FA.md) |
| :---: | :---: |

---

<a name="english"></a>

## English

#### 📝 About the Project

A specialized tool designed to automate the process of downloading and converting Adobe Connect recordings from Shahrekord University's (SKU) LMS. It eliminates the manual struggle of piecing together FLV files by handling authentication, downloading, and merging automatically.

#### 📸 Screenshots

|GUI |
|:---:|
| ![GUI Screenshot](screenshots/gui.jpg) |

#### ✨ Key Features

·  Auto-Authenticati
on: Securely logs into the university portal using student credentials
·  Automated Extraction: Downloads the recording ZIP, extracts components, and sorts them
·  Seamless Merging: Uses FFmpeg to merge separate video chunks into a single, playable file
·  Chat Log Recovery: Extracts all session messages and saves them as a text file
·  Screen Share Support: Automatically detects and processes secondary screen-sharing streams
·  User-Friendly GUI: Simple graphical interface for users who prefer not to use the terminal

#### 🚀 Getting Started

Prerequisites

· Python 3.6+
· FFmpeg (Must be added to your system environment variables)


Installation (Linux/macOS)

```bash
git clone https://github.com/MadHo3/Adobe-Meetings-Downloader-Sku.git
cd Adobe-Meetings-Downloader-Sku
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 script.py
```

#### Installation (Windows)

```batch
# Option 1: Run install.bat as Administrator, then launch AdobeDownloaderSku.exe
# Option 2: Using Python directly
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python gui.py
```

#### 📁 Output Structure

```
Adobe-Meetings-Downloader-Sku/
├── videos/          ← Final merged videos
├── chats/           ← Session chat log files
├── downloads/       ← Temporary ZIP files
└── logs/            ← Error reports (if any)
```


#### 🤝 Contributing

Your feedback, ideas, and bug reports help make this tool better. Please share them via the Issues section.


Developed with ❤️ for SKU Students

