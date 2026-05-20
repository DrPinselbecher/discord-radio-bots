import asyncio
import logging
import os
import sys

import discord
from dotenv import load_dotenv

from radio import get_radio_track


env_file = sys.argv[1] if len(sys.argv) > 1 else ".env"
load_dotenv(env_file)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
VOICE_CHANNEL_ID = os.getenv("VOICE_CHANNEL_ID")
MUSIC_FOLDER = os.getenv("MUSIC_FOLDER")

SUPPORTED_EXTENSIONS = {".mp3", ".wav", ".ogg", ".flac", ".m4a"}

if not DISCORD_TOKEN:
    raise RuntimeError("DISCORD_TOKEN is missing.")

if not VOICE_CHANNEL_ID:
    raise RuntimeError("VOICE_CHANNEL_ID is missing.")

if not MUSIC_FOLDER:
    raise RuntimeError("MUSIC_FOLDER is missing.")


class MusicBot(discord.Client):
    def __init__(self) -> None:
        intents = discord.Intents.none()
        intents.guilds = True
        intents.voice_states = True

        super().__init__(intents=intents)
        self.voice_client_instance: discord.VoiceClient | None = None
        self.music_task_started = False

    async def on_ready(self) -> None:
        logging.info("Logged in as %s", self.user)
        await self.connect_to_channel()

        if not self.music_task_started:
            self.music_task_started = True
            asyncio.create_task(self.play_music_loop())

    async def connect_to_channel(self) -> None:
        channel = await self.fetch_channel(int(VOICE_CHANNEL_ID))

        if not isinstance(channel, discord.VoiceChannel):
            raise RuntimeError("VOICE_CHANNEL_ID must be a voice channel.")

        if self.voice_client_instance and self.voice_client_instance.is_connected():
            return

        self.voice_client_instance = await channel.connect()
        logging.info("Connected to voice channel: %s", channel.name)

    async def play_music_loop(self) -> None:
        while True:
            try:
                if not self.voice_client_instance or not self.voice_client_instance.is_connected():
                    await self.connect_to_channel()

                track = get_radio_track(MUSIC_FOLDER, SUPPORTED_EXTENSIONS)
                await self.play_file(track.file, track.start_seconds)

            except Exception:
                logging.exception("Music loop crashed. Retrying in 10 seconds.")
                await asyncio.sleep(10)

    async def play_file(self, file, start_seconds: float) -> None:
        if not self.voice_client_instance:
            return

        finished = asyncio.Event()
        loop = asyncio.get_running_loop()

        def after_playing(error: Exception | None) -> None:
            if error:
                logging.error("Playback error: %s", error)

            loop.call_soon_threadsafe(finished.set)

        logging.info("Now playing: %s from %.2f seconds", file.name, start_seconds)

        source = discord.FFmpegPCMAudio(
            str(file),
            before_options=f"-ss {start_seconds}",
        )

        self.voice_client_instance.play(source, after=after_playing)
        await finished.wait()


if __name__ == "__main__":
    client = MusicBot()
    client.run(DISCORD_TOKEN)