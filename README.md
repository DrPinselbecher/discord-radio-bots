# Discord Music Radio Bots

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![discord.py](https://img.shields.io/badge/Discord-discord.py-5865F2)
![FFmpeg](https://img.shields.io/badge/Audio-FFmpeg-green)
![Platform](https://img.shields.io/badge/Platform-Linux_VM-lightgrey)
![Status](https://img.shields.io/badge/Status-In_Development-yellow)

Discord Music Radio Bots is a Python-based Discord voice bot setup for running multiple permanent music radio channels on one Discord server.

Each bot connects to one dedicated Discord voice channel and plays music from a matching folder. The project is designed for deployment on a small Linux VM, such as Oracle Cloud Always Free.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Tech Stack](#tech-stack)
- [Core Features](#core-features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Local Setup](#local-setup)
- [Environment Files](#environment-files)
- [Discord Bot Setup](#discord-bot-setup)
- [Radio Mode](#radio-mode)
- [Deployment on Linux VM](#deployment-on-linux-vm)
- [Systemd Services](#systemd-services)
- [Useful Commands](#useful-commands)
- [Security Notes](#security-notes)
- [Music Licensing](#music-licensing)
- [Current Status](#current-status)
- [License](#license)

---

## Project Overview

> [!NOTE]
> This project is intended for private Discord servers that need simple always-online music radio channels without running a local PC.

The setup uses three separate Discord bot accounts:

```text
Lofi Radio      -> music/lofi/
Elevator Radio  -> music/elevator/
Tavern Radio    -> music/tavern/
```

Each bot uses:

- one Discord bot token
- one fixed Discord voice channel
- one music folder
- one separate environment file

This allows three independent music channels to run at the same time on one Discord server.

---

## Tech Stack

| Area | Technology |
|---|---|
| Language | Python 3.11+ |
| Discord Library | discord.py |
| Voice Support | discord.py[voice] / PyNaCl |
| Audio Playback | FFmpeg |
| Audio Metadata | FFprobe |
| Environment Handling | python-dotenv |
| Deployment Target | Linux VM |
| Process Management | systemd |

---

## Core Features

- multiple Discord music bots on one server
- one bot per voice channel
- permanent voice-channel connection
- local folder-based music playback
- radio-like playback behavior
- time-based track position calculation
- automatic reconnect handling
- separate `.env` files per bot
- simple deployment on a small Linux VM
- no web framework required
- no database required

Supported audio formats:

```text
.mp3
.wav
.ogg
.flac
.m4a
```

---

## Architecture

```text
Discord Server
│
├── Voice Channel: Lofi
│       └── Lofi Radio Bot
│              └── music/lofi/
│
├── Voice Channel: Elevator
│       └── Elevator Radio Bot
│              └── music/elevator/
│
└── Voice Channel: Tavern
        └── Tavern Radio Bot
               └── music/tavern/
```

Deployment structure:

```text
Oracle Cloud VM / Linux Server
│
├── Python virtual environment
├── Discord bot source code
├── Music folders
├── Environment files
└── systemd services
```

---

## Project Structure

```text
discord-music-bots/
├── .env.example
├── .gitignore
├── bot.py
├── radio.py
├── README.md
├── requirements.txt
└── music/
    ├── lofi/
    ├── elevator/
    └── tavern/
```

Local-only files that must not be committed:

```text
.env.lofi
.env.elevator
.env.tavern
.venv/
music/
```

---

## Local Setup

### 1. Create Virtual Environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Check FFmpeg and FFprobe

FFmpeg and FFprobe must be installed and available in the system path.

```bash
ffmpeg -version
ffprobe -version
```

### 4. Create Music Folders

```bash
mkdir -p music/lofi music/elevator music/tavern
```

On Windows PowerShell:

```powershell
mkdir music\lofi
mkdir music\elevator
mkdir music\tavern
```

### 5. Add Test Music

Place at least one supported audio file into the matching folder:

```text
music/lofi/
music/elevator/
music/tavern/
```

---

## Environment Files

Each bot uses its own environment file.

### `.env.example`

```env
DISCORD_TOKEN=
VOICE_CHANNEL_ID=
MUSIC_FOLDER=
```

### `.env.lofi`

```env
DISCORD_TOKEN=YOUR_LOFI_BOT_TOKEN
VOICE_CHANNEL_ID=YOUR_LOFI_VOICE_CHANNEL_ID
MUSIC_FOLDER=./music/lofi
```

### `.env.elevator`

```env
DISCORD_TOKEN=YOUR_ELEVATOR_BOT_TOKEN
VOICE_CHANNEL_ID=YOUR_ELEVATOR_VOICE_CHANNEL_ID
MUSIC_FOLDER=./music/elevator
```

### `.env.tavern`

```env
DISCORD_TOKEN=YOUR_TAVERN_BOT_TOKEN
VOICE_CHANNEL_ID=YOUR_TAVERN_VOICE_CHANNEL_ID
MUSIC_FOLDER=./music/tavern
```

> [!WARNING]
> Real `.env` files contain sensitive bot tokens and must never be committed.

---

## Discord Bot Setup

Three separate Discord applications are required.

Recommended bot names:

```text
Lofi Radio
Elevator Radio
Tavern Radio
```

Each bot needs the following Discord permissions:

```text
View Channels
Connect
Speak
```

Administrator permissions are not required.

### Required Discord IDs

For each bot, copy the matching voice channel ID:

```text
Lofi Voice Channel ID
Elevator Voice Channel ID
Tavern Voice Channel ID
```

To copy channel IDs, enable Developer Mode in Discord:

```text
User Settings
   |
   v
Advanced
   |
   v
Developer Mode
```

Then right-click the voice channel and select:

```text
Copy Channel ID
```

---

## Radio Mode

The bot does not simply restart the playlist from the first track.

Instead, the radio logic calculates the current playback position based on the current system time.

Example:

```text
Current time
   |
   v
Calculate position inside full playlist duration
   |
   v
Select matching track
   |
   v
Start playback at the correct timestamp
```

This creates radio-like behavior:

- users joining later hear the current track position
- the bot can restart and resume at a calculated radio position
- playback does not always begin with the same first song
- all tracks are processed in a stable sorted order

> [!IMPORTANT]
> Stable file ordering is required for predictable radio behavior. Files are sorted alphabetically.

Recommended naming pattern:

```text
001_track_name.mp3
002_track_name.mp3
003_track_name.mp3
```

---

## Deployment on Linux VM

This project is designed to run on a small Linux VM.

Recommended minimum setup:

| Resource | Value |
|---|---|
| OS | Ubuntu 24.04 |
| CPU | 1 OCPU |
| RAM | 1 GB |
| Swap | 2 GB |
| Storage | 40 GB+ |

### 1. Install System Packages

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y ffmpeg python3 python3-venv python3-pip git
```

### 2. Clone Repository

```bash
git clone YOUR_REPOSITORY_URL discord-music-bots
cd discord-music-bots
```

### 3. Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Create Music Folders

```bash
mkdir -p music/lofi music/elevator music/tavern
```

### 6. Create Environment Files

Create the real environment files only on the VM:

```bash
nano .env.lofi
nano .env.elevator
nano .env.tavern
```

These files must contain the real bot tokens and channel IDs.

### 7. Test One Bot Manually

```bash
source .venv/bin/activate
python bot.py .env.lofi
```

If the bot joins the correct voice channel and plays music, stop the process with:

```text
CTRL + C
```

---

## Systemd Services

For production usage, each bot should run as its own systemd service.

### Lofi Service

Create:

```bash
sudo nano /etc/systemd/system/discord-lofi.service
```

Content:

```ini
[Unit]
Description=Discord Lofi Radio Bot
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/discord-music-bots
ExecStart=/home/ubuntu/discord-music-bots/.venv/bin/python bot.py .env.lofi
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Elevator Service

Create:

```bash
sudo nano /etc/systemd/system/discord-elevator.service
```

Content:

```ini
[Unit]
Description=Discord Elevator Radio Bot
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/discord-music-bots
ExecStart=/home/ubuntu/discord-music-bots/.venv/bin/python bot.py .env.elevator
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Tavern Service

Create:

```bash
sudo nano /etc/systemd/system/discord-tavern.service
```

Content:

```ini
[Unit]
Description=Discord Tavern Radio Bot
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/discord-music-bots
ExecStart=/home/ubuntu/discord-music-bots/.venv/bin/python bot.py .env.tavern
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Enable and Start Services

```bash
sudo systemctl daemon-reload

sudo systemctl enable discord-lofi
sudo systemctl enable discord-elevator
sudo systemctl enable discord-tavern

sudo systemctl start discord-lofi
sudo systemctl start discord-elevator
sudo systemctl start discord-tavern
```

---

## Useful Commands

### Start Bot Locally

```bash
python bot.py .env.lofi
```

```bash
python bot.py .env.elevator
```

```bash
python bot.py .env.tavern
```

### Check Service Status

```bash
sudo systemctl status discord-lofi
sudo systemctl status discord-elevator
sudo systemctl status discord-tavern
```

### Follow Logs

```bash
journalctl -u discord-lofi -f
```

```bash
journalctl -u discord-elevator -f
```

```bash
journalctl -u discord-tavern -f
```

### Restart Services

```bash
sudo systemctl restart discord-lofi
sudo systemctl restart discord-elevator
sudo systemctl restart discord-tavern
```

### Stop Services

```bash
sudo systemctl stop discord-lofi
sudo systemctl stop discord-elevator
sudo systemctl stop discord-tavern
```

### Pull Latest Code on VM

```bash
cd ~/discord-music-bots
git pull
source .venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart discord-lofi discord-elevator discord-tavern
```

---

## Security Notes

- Bot tokens must never be committed.
- Real `.env` files must stay on the server only.
- The `music/` folder should not be committed.
- Administrator permissions are not required for Discord bots.
- Only the required Discord permissions should be granted.
- The VM does not need public HTTP or HTTPS ports for the bots.
- SSH access should be limited to trusted keys.
- Secrets should be rotated immediately if they are leaked.

Recommended `.gitignore`:

```gitignore
.env
.env.*
.venv/
__pycache__/
*.pyc
music/
```

---

## Music Licensing

This project does not include music files.

Use only music that you are allowed to play in your Discord server.

Recommended sources:

```text
own music
licensed music
royalty-free music
Creative Commons music
CC0 music
```

> [!WARNING]
> Downloading or streaming copyrighted music without permission may violate platform terms and copyright law.

---

## Current Status

Implemented:

- Discord bot voice connection
- one bot per voice channel
- local music folder playback
- radio-like playback position calculation
- `.env` based configuration
- multi-bot setup through separate environment files
- FFmpeg audio playback
- FFprobe duration detection
- local Windows development setup
- Linux VM deployment preparation

Planned improvements:

- systemd deployment on VM
- automatic service restart validation
- improved logging per bot
- optional Docker Compose setup
- optional track history logging
- optional health-check script

---

## License

This project is currently not licensed for public reuse.