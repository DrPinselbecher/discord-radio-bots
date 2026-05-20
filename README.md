# Discord Radio Bots

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![discord.py](https://img.shields.io/badge/Discord-discord.py-5865F2)
![FFmpeg](https://img.shields.io/badge/Audio-FFmpeg-green)
![Linux](https://img.shields.io/badge/Deployment-Linux_VM-lightgrey)
![Status](https://img.shields.io/badge/Status-In_Development-yellow)

Discord Radio Bots is a lightweight Python-based Discord voice bot setup for running multiple permanent audio radio channels on a single Discord server.

Each bot instance connects to one configured Discord voice channel and plays audio files from one configured folder. The project is designed for small Linux VM deployments and does not require a web framework, database or public HTTP endpoint.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Tech Stack](#tech-stack)
- [Core Features](#core-features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Local Development Setup](#local-development-setup)
- [Environment Configuration](#environment-configuration)
- [Discord Application Setup](#discord-application-setup)
- [Radio Playback Mode](#radio-playback-mode)
- [Deployment on Linux VM](#deployment-on-linux-vm)
- [Systemd Service Setup](#systemd-service-setup)
- [Useful Commands](#useful-commands)
- [Security Notes](#security-notes)
- [Audio File Requirements](#audio-file-requirements)
- [Current Status](#current-status)
- [License](#license)

---

## Project Overview

> [!NOTE]
> This project provides always-online Discord radio channels without requiring a local PC to stay powered on.

The setup supports multiple independent bot instances.

Example setup:

```text
Bot Instance 1  -> Discord Voice Channel 1  -> custom audio folder 1
Bot Instance 2  -> Discord Voice Channel 2  -> custom audio folder 2
Bot Instance 3  -> Discord Voice Channel 3  -> custom audio folder 3
```

Each bot instance uses:

- one Discord bot token
- one fixed Discord voice channel ID
- one configured audio folder
- one separate environment file

This allows multiple independent radio channels to run at the same time on one Discord server.

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

- multiple Discord bot instances on one server
- one bot instance per voice channel
- folder-based audio playback
- radio-like playback behavior
- time-based track position calculation
- automatic reconnect handling
- separate environment files per bot instance
- configurable audio folders
- lightweight Linux VM deployment
- no database required
- no web framework required
- no public HTTP or HTTPS endpoint required

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
├── Voice Channel 1
│       └── Bot Instance 1
│              └── Configured audio folder
│
├── Voice Channel 2
│       └── Bot Instance 2
│              └── Configured audio folder
│
└── Voice Channel 3
        └── Bot Instance 3
               └── Configured audio folder
```

Deployment structure:

```text
Linux VM
│
├── Python virtual environment
├── Discord bot source code
├── Environment files
├── Audio folders
└── systemd services
```

---

## Project Structure

```text
discord-radio-bots/
├── .env.template
├── .gitignore
├── bot.py
├── radio.py
├── README.md
├── requirements.txt
└── music/
    └── .gitkeep
```

The `music/` directory is intentionally kept empty in Git.

Runtime-only files that must not be committed:

```text
.env.bot-1
.env.bot-2
.env.bot-3
.venv/
music/*
```

---

## Local Development Setup

### Prerequisites

| Tool | Purpose |
|---|---|
| Python 3.11+ | Runtime for the bot |
| Git | Version control |
| FFmpeg | Audio playback |
| FFprobe | Audio duration detection |
| Discord Developer Account | Bot application setup |

### 1. Clone Repository

```bash
git clone YOUR_REPOSITORY_URL discord-radio-bots
cd discord-radio-bots
```

### 2. Create Virtual Environment

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

### 3. Install Python Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Verify FFmpeg Installation

```bash
ffmpeg -version
ffprobe -version
```

Both commands must return version information.

### 5. Create Audio Folders

Create one folder per bot instance.

Windows PowerShell:

```powershell
mkdir music\radio-channel-1
mkdir music\radio-channel-2
mkdir music\radio-channel-3
```

macOS / Linux:

```bash
mkdir -p music/radio-channel-1 music/radio-channel-2 music/radio-channel-3
```

Folder names are examples only. Any naming can be used as long as the matching environment file points to the correct folder.

### 6. Add Audio Files

Place at least one supported audio file into each configured folder.

Example:

```text
music/radio-channel-1/
music/radio-channel-2/
music/radio-channel-3/
```

---

## Environment Configuration

This project uses one environment file per bot instance.

Create the files from the template.

Windows PowerShell:

```powershell
Copy-Item .env.template .env.bot-1
Copy-Item .env.template .env.bot-2
Copy-Item .env.template .env.bot-3
```

macOS / Linux:

```bash
cp .env.template .env.bot-1
cp .env.template .env.bot-2
cp .env.template .env.bot-3
```

### Example `.env.bot-1`

```env
DISCORD_TOKEN=YOUR_FIRST_BOT_TOKEN
VOICE_CHANNEL_ID=YOUR_FIRST_VOICE_CHANNEL_ID
MUSIC_FOLDER=./music/radio-channel-1
```

### Example `.env.bot-2`

```env
DISCORD_TOKEN=YOUR_SECOND_BOT_TOKEN
VOICE_CHANNEL_ID=YOUR_SECOND_VOICE_CHANNEL_ID
MUSIC_FOLDER=./music/radio-channel-2
```

### Example `.env.bot-3`

```env
DISCORD_TOKEN=YOUR_THIRD_BOT_TOKEN
VOICE_CHANNEL_ID=YOUR_THIRD_VOICE_CHANNEL_ID
MUSIC_FOLDER=./music/radio-channel-3
```

> [!WARNING]
> Real environment files contain sensitive Discord bot tokens and must never be committed.

---

## Discord Application Setup

Each always-online voice channel requires one separate Discord bot application.

### 1. Create Discord Applications

Open the Discord Developer Portal:

```text
https://discord.com/developers/applications
```

Create one application per planned bot instance.

Recommended neutral naming:

```text
Radio Bot 1
Radio Bot 2
Radio Bot 3
```

### 2. Create Bot Users

For each application:

```text
Application
   |
   v
Bot
   |
   v
Reset Token / Copy Token
```

Copy each token into the matching environment file.

### 3. Configure Installation Permissions

Each bot only needs these permissions:

```text
View Channels
Connect
Speak
```

Administrator permissions are not required.

### 4. Invite Bots to the Discord Server

For each application:

```text
Installation
   |
   v
Guild Install
   |
   v
Scope: bot
   |
   v
Permissions:
- View Channels
- Connect
- Speak
```

Open the generated installation link and invite the bot to the Discord server.

### 5. Copy Voice Channel IDs

Enable Developer Mode in Discord:

```text
User Settings
   |
   v
Advanced
   |
   v
Developer Mode
```

Then right-click the target voice channel:

```text
Copy Channel ID
```

Use the copied ID as:

```env
VOICE_CHANNEL_ID=
```

---

## Radio Playback Mode

The bot does not simply restart playback from the first file.

Instead, the radio logic calculates the current playback position based on system time and the total duration of all tracks in the configured folder.

Playback flow:

```text
Read configured audio folder
   |
   v
Sort audio files alphabetically
   |
   v
Read track durations with FFprobe
   |
   v
Calculate current position inside total station duration
   |
   v
Select matching track
   |
   v
Start playback at calculated timestamp
```

This creates radio-like behavior:

- users joining later hear the current playback position
- bot restarts resume at a calculated radio position
- playback does not always begin with the same file
- each configured folder behaves like a continuous radio loop

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

Recommended minimum VM setup:

| Resource | Value |
|---|---|
| OS | Ubuntu 24.04 |
| CPU | 1 vCPU / OCPU |
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
git clone YOUR_REPOSITORY_URL discord-radio-bots
cd discord-radio-bots
```

### 3. Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Create Audio Folders

```bash
mkdir -p music/radio-channel-1 music/radio-channel-2 music/radio-channel-3
```

The folder names are examples. The actual folders only need to match the `MUSIC_FOLDER` values in the environment files.

### 6. Create Environment Files

```bash
cp .env.template .env.bot-1
cp .env.template .env.bot-2
cp .env.template .env.bot-3
```

Edit each file:

```bash
nano .env.bot-1
nano .env.bot-2
nano .env.bot-3
```

### 7. Upload Audio Files

Audio files are intentionally not part of the Git repository.

Recommended upload methods:

```text
scp
rsync
SFTP
manual upload through your server workflow
```

Example with `scp`:

```bash
scp ./local-audio-file.mp3 ubuntu@YOUR_SERVER_IP:/home/ubuntu/discord-radio-bots/music/radio-channel-1/
```

### 8. Test One Bot Manually

```bash
source .venv/bin/activate
python bot.py .env.bot-1
```

If the bot joins the correct voice channel and plays audio, stop the process:

```text
CTRL + C
```

---

## Systemd Service Setup

For production usage, each bot instance should run as its own systemd service.

### Bot 1 Service

Create:

```bash
sudo nano /etc/systemd/system/discord-radio-bot-1.service
```

Content:

```ini
[Unit]
Description=Discord Radio Bot 1
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/discord-radio-bots
ExecStart=/home/ubuntu/discord-radio-bots/.venv/bin/python bot.py .env.bot-1
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Bot 2 Service

Create:

```bash
sudo nano /etc/systemd/system/discord-radio-bot-2.service
```

Content:

```ini
[Unit]
Description=Discord Radio Bot 2
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/discord-radio-bots
ExecStart=/home/ubuntu/discord-radio-bots/.venv/bin/python bot.py .env.bot-2
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Bot 3 Service

Create:

```bash
sudo nano /etc/systemd/system/discord-radio-bot-3.service
```

Content:

```ini
[Unit]
Description=Discord Radio Bot 3
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/discord-radio-bots
ExecStart=/home/ubuntu/discord-radio-bots/.venv/bin/python bot.py .env.bot-3
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Enable and Start Services

```bash
sudo systemctl daemon-reload

sudo systemctl enable discord-radio-bot-1
sudo systemctl enable discord-radio-bot-2
sudo systemctl enable discord-radio-bot-3

sudo systemctl start discord-radio-bot-1
sudo systemctl start discord-radio-bot-2
sudo systemctl start discord-radio-bot-3
```

---

## Useful Commands

### Start Bot Manually

```bash
python bot.py .env.bot-1
python bot.py .env.bot-2
python bot.py .env.bot-3
```

### Check Service Status

```bash
sudo systemctl status discord-radio-bot-1
sudo systemctl status discord-radio-bot-2
sudo systemctl status discord-radio-bot-3
```

### Follow Logs

```bash
journalctl -u discord-radio-bot-1 -f
journalctl -u discord-radio-bot-2 -f
journalctl -u discord-radio-bot-3 -f
```

### Restart Services

```bash
sudo systemctl restart discord-radio-bot-1
sudo systemctl restart discord-radio-bot-2
sudo systemctl restart discord-radio-bot-3
```

### Stop Services

```bash
sudo systemctl stop discord-radio-bot-1
sudo systemctl stop discord-radio-bot-2
sudo systemctl stop discord-radio-bot-3
```

### Deploy Latest Code

```bash
cd ~/discord-radio-bots
git pull
source .venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart discord-radio-bot-1 discord-radio-bot-2 discord-radio-bot-3
```

---

## Security Notes

- Real `.env` files must never be committed.
- Discord bot tokens must be treated as secrets.
- Bot tokens must be rotated immediately if leaked.
- Audio files should not be committed.
- Discord bots do not require administrator permissions.
- Only the minimum required Discord permissions should be granted.
- The VM does not need public HTTP or HTTPS ports for this project.
- SSH access should be restricted to trusted keys.
- Keep system packages updated.

Recommended `.gitignore`:

```gitignore
.env
.env.*
!.env.template
.venv/
venv/
env/
__pycache__/
*.py[cod]
*$py.class
.pytest_cache/
.mypy_cache/
.ruff_cache/
music/*
!music/.gitkeep
*.log
.DS_Store
Thumbs.db
.vscode/
.idea/
```

---

## Audio File Requirements

This project does not include audio files.

Use only audio files that you are allowed to play on your Discord server.

Recommended file sources:

```text
self-created audio
licensed audio
royalty-free audio
Creative Commons audio
CC0 audio
```

> [!WARNING]
> Downloading, redistributing or streaming copyrighted audio without permission may violate platform terms and copyright law.

---

## Current Status

Implemented:

- Discord bot voice connection
- one bot instance per voice channel
- folder-based audio playback
- configurable audio folder per bot instance
- radio-like playback position calculation
- FFmpeg audio playback
- FFprobe duration detection
- `.env` based configuration
- multi-instance setup through separate environment files
- local Windows development setup
- Linux VM deployment preparation

Planned improvements:

- production systemd deployment
- per-bot logging files
- automatic deployment script
- optional Docker Compose setup
- optional health-check script
- optional track history logging

---

## License

This project is currently not licensed for public reuse.