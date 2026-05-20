import json
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RadioTrack:
    file: Path
    start_seconds: float


def get_audio_duration(file: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "json",
            str(file),
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    data = json.loads(result.stdout)
    return float(data["format"]["duration"])


def get_radio_track(music_folder: str, supported_extensions: set[str]) -> RadioTrack:
    music_path = Path(music_folder)

    if not music_path.exists():
        raise RuntimeError(f"Music folder does not exist: {music_path}")

    files = sorted(
        [
            file
            for file in music_path.iterdir()
            if file.is_file() and file.suffix.lower() in supported_extensions
        ],
        key=lambda file: file.name.lower(),
    )

    if not files:
        raise RuntimeError(f"No music files found in {music_path}")

    durations = [(file, get_audio_duration(file)) for file in files]
    total_duration = sum(duration for _, duration in durations)

    if total_duration <= 0:
        raise RuntimeError("Total playlist duration is invalid.")

    current_position = time.time() % total_duration

    elapsed = 0.0

    for file, duration in durations:
        if elapsed + duration > current_position:
            return RadioTrack(
                file=file,
                start_seconds=current_position - elapsed,
            )

        elapsed += duration

    return RadioTrack(file=durations[0][0], start_seconds=0.0)