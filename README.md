# Discord Radio Bots

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![discord.py](https://img.shields.io/badge/Discord-discord.py-5865F2)
![FFmpeg](https://img.shields.io/badge/Audio-FFmpeg-green)
![Opus](https://img.shields.io/badge/Audio-Opus-7A5CFF)
![Linux](https://img.shields.io/badge/Deployment-Linux_VM-lightgrey)
![Status](https://img.shields.io/badge/Status-In_Development-yellow)

Discord Radio Bots is a lightweight Python-based Discord voice bot setup for running multiple permanent audio radio channels on a single Discord server.

Each bot instance connects to one configured Discord voice channel and plays pre-converted `.opus` audio files from one configured folder. The project is designed for small Linux VM deployments and does not require a web framework, database or public HTTP endpoint.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Tech Stack](#tech-stack)
- [Core Features](#core-features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Local Development Setup](#local-development-setup)
- [Opus Conversion Workflow](#opus-conversion-workflow)
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
Bot Instance 1  -> Discord Voice Channel 1  -> configured audio folder 1
Bot Instance 2  -> Discord Voice Channel 2  -> configured audio folder 2
Bot Instance 3  -> Discord Voice Channel 3  -> configured audio folder 3
```

Each bot instance uses:

- one Discord bot token
- one fixed Discord voice channel ID
- one configured audio folder
- one separate environment file
- pre-converted `.opus` audio files

This allows multiple independent radio channels to run at the same time on one Discord server.

---

## Tech Stack

| Area | Technology |
|---|---|
| Language | Python 3.11+ |
| Discord Library | discord.py |
| Voice Support | discord.py[voice] / PyNaCl |
| Audio Playback | FFmpeg |
| Audio Runtime Format | Opus |
| Audio Metadata | FFprobe |
| Environment Handling | python-dotenv |
| Deployment Target | Linux VM |
| Process Management | systemd |

---

## Core Features

- multiple Discord bot instances on one server
- one bot instance per voice channel
- folder-based audio playback
- Opus-only runtime playback
- FFmpeg Opus playback with `codec="copy"`
- radio-like playback behavior
- time-based track position calculation
- automatic reconnect handling
- separate environment files per bot instance
- configurable audio folders
- lightweight Linux VM deployment
- no database required
- no web framework required
- no public HTTP or HTTPS endpoint required

Supported runtime audio format:

```text
.opus
```

> [!IMPORTANT]
> The bot is optimized for pre-converted Opus audio files. Other audio formats should be converted to `.opus` before deployment.

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
├── Opus audio folders
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
├── converted/
│   └── .gitkeep
└── music/
    └── .gitkeep
```

The `music/` and `converted/` directories are intentionally kept empty in Git.

Runtime-only files that must not be committed:

```text
.env.bot-1
.env.bot-2
.env.bot-3
.env.*
.venv/
music/*
converted/*
```

Recommended runtime folder example:

```text
music/
├── radio-channel-1/
├── radio-channel-2/
└── radio-channel-3/
```

Recommended local conversion folder example:

```text
converted/
├── radio-channel-1_opus/
├── radio-channel-2_opus/
└── radio-channel-3_opus/
```

Folder names are only examples. The actual names only need to match the `MUSIC_FOLDER` values in the environment files.

---

## Local Development Setup

### Prerequisites

| Tool | Purpose |
|---|---|
| Python 3.11+ | Runtime for the bot |
| Git | Version control |
| FFmpeg | Audio conversion and playback |
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

### 5. Create Local Audio Folders

Create one source folder per bot instance.

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

### 6. Add Source Audio Files

Place source audio files into the matching local folder.

Example:

```text
music/radio-channel-1/
music/radio-channel-2/
music/radio-channel-3/
```

These source files are only used locally for conversion and should not be committed.

---

## Opus Conversion Workflow

The bot is optimized for `.opus` files.

Audio files should be converted locally before they are uploaded to the server. This avoids live re-encoding on the VM and reduces CPU usage during playback.

The bot uses:

```python
discord.FFmpegOpusAudio(..., codec="copy")
```

This means the prepared Opus stream is copied directly instead of being encoded again during playback.

### Create Local Conversion Folders

Windows PowerShell:

```powershell
mkdir converted\radio-channel-1_opus
mkdir converted\radio-channel-2_opus
mkdir converted\radio-channel-3_opus
```

macOS / Linux:

```bash
mkdir -p converted/radio-channel-1_opus converted/radio-channel-2_opus converted/radio-channel-3_opus
```

### Convert Audio Files to Opus

Windows PowerShell example for channel 1:

```powershell
Get-ChildItem ".\music\radio-channel-1" -File | ForEach-Object {
    ffmpeg -y -i $_.FullName -vn -c:a libopus -b:a 96k -ar 48000 -ac 2 ".\converted\radio-channel-1_opus\$($_.BaseName).opus"
}
```

Windows PowerShell example for channel 2:

```powershell
Get-ChildItem ".\music\radio-channel-2" -File | ForEach-Object {
    ffmpeg -y -i $_.FullName -vn -c:a libopus -b:a 96k -ar 48000 -ac 2 ".\converted\radio-channel-2_opus\$($_.BaseName).opus"
}
```

Windows PowerShell example for channel 3:

```powershell
Get-ChildItem ".\music\radio-channel-3" -File | ForEach-Object {
    ffmpeg -y -i $_.FullName -vn -c:a libopus -b:a 96k -ar 48000 -ac 2 ".\converted\radio-channel-3_opus\$($_.BaseName).opus"
}
```

### Recommended Opus Settings

| Option | Value | Purpose |
|---|---|---|
| Codec | `libopus` | Converts audio to Opus |
| Bitrate | `96k` | Good balance between quality and file size |
| Sample Rate | `48000` | Recommended for Discord voice |
| Channels | `2` | Stereo output |
| Video | `-vn` | Removes video streams |

### Important

Only `.opus` files should be placed in the active server music folders when `codec="copy"` is used.

Unsupported runtime files such as `.mp3`, `.m4a`, `.wav`, `.flac` or `.mp4` should be converted locally before upload.

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

### `.env.template`

```env
# Discord bot token for one bot instance.
# Create the token in the Discord Developer Portal.
DISCORD_TOKEN=

# Discord voice channel ID used by this bot instance.
# Enable Discord Developer Mode, right-click the voice channel and copy the channel ID.
VOICE_CHANNEL_ID=

# Path to the audio folder used by this bot instance.
# The folder can be inside ./music/ or an absolute server path.
#
# Examples:
# MUSIC_FOLDER=./music/radio-channel-1
# MUSIC_FOLDER=./music/radio-channel-2
# MUSIC_FOLDER=/home/ubuntu/audio/radio-channel-1
MUSIC_FOLDER=
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
Sort .opus files alphabetically
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
- only the initial start or reconnect jumps into the calculated track position
- following track changes start cleanly from the beginning of the next file

> [!IMPORTANT]
> Stable file ordering is required for predictable radio behavior. Files are sorted alphabetically.

Recommended naming pattern:

```text
001_track_name.opus
002_track_name.opus
003_track_name.opus
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

### 5. Create Runtime Audio Folders

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

Secure the environment files:

```bash
chmod 600 .env.bot-1 .env.bot-2 .env.bot-3
```

### 7. Upload Opus Audio Files

Audio files are intentionally not part of the Git repository.

Convert audio files locally first, then upload the generated `.opus` files to the VM.

PowerShell example for channel 1:

```powershell
scp -r -i "$env:USERPROFILE\.ssh\oracle_discord_music_server" ".\converted\radio-channel-1_opus\*" ubuntu@YOUR_SERVER_IP:/home/ubuntu/discord-radio-bots/music/radio-channel-1/
```

PowerShell example for channel 2:

```powershell
scp -r -i "$env:USERPROFILE\.ssh\oracle_discord_music_server" ".\converted\radio-channel-2_opus\*" ubuntu@YOUR_SERVER_IP:/home/ubuntu/discord-radio-bots/music/radio-channel-2/
```

PowerShell example for channel 3:

```powershell
scp -r -i "$env:USERPROFILE\.ssh\oracle_discord_music_server" ".\converted\radio-channel-3_opus\*" ubuntu@YOUR_SERVER_IP:/home/ubuntu/discord-radio-bots/music/radio-channel-3/
```

Check uploaded files on the VM:

```bash
find /home/ubuntu/discord-radio-bots/music -maxdepth 2 -type f
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

### Check Running Bot Processes

```bash
pgrep -af "python bot.py"
```

### Stop Manual Bot Processes

```bash
pkill -f "python bot.py"
```

---

## Security Notes

- Real `.env` files must never be committed.
- Discord bot tokens must be treated as secrets.
- Bot tokens must be rotated immediately if leaked.
- Audio files should not be committed.
- Converted audio files should not be committed.
- Discord bots do not require administrator permissions.
- Only the minimum required Discord permissions should be granted.
- The VM does not need public HTTP or HTTPS ports for this project.
- SSH access should be restricted to trusted keys.
- Keep system packages updated.

Recommended `.gitignore`:

```gitignore
# Environment files
.env
.env.*
!.env.template

# Python virtual environments
.venv/
venv/
env/

# Python cache files
__pycache__/
*.py[cod]
*$py.class

# Python tooling/cache
.pytest_cache/
.mypy_cache/
.ruff_cache/

# Audio files / runtime music folders
music/*
converted/*
!music/.gitkeep
!converted/.gitkeep

# Logs
*.log

# OS files
.DS_Store
Thumbs.db

# IDE files
.vscode/
.idea/

# Other private notes
notice.md
```

---

## Audio File Requirements

This project does not include audio files.

The runtime music folders on the server should contain `.opus` files only.

Recommended source file types before conversion:

```text
.mp3
.wav
.ogg
.flac
.m4a
.mp4
```

These files should be converted locally to `.opus` before being uploaded to the VM.

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
- Opus-only runtime playback
- FFmpeg Opus playback with `codec="copy"`
- local audio conversion workflow
- radio-like playback position calculation
- FFmpeg audio playback
- FFprobe duration detection
- `.env` based configuration
- multi-instance setup through separate environment files
- ignored runtime audio folders through `.gitkeep` placeholders
- local Windows development setup
- Linux VM deployment preparation
- production-ready systemd service setup

Planned improvements:

- per-bot logging files
- automatic deployment script
- optional Docker Compose setup
- optional health-check script
- optional track history logging

---

## License

This project is currently not licensed for public reuse.