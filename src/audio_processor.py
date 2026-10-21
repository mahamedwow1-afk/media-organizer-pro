"""Audio processor for analyzing and organizing audio files."""

import subprocess
import json
from pathlib import Path
from dataclasses import dataclass
from typing import Optional
import logging

logger = logging.getLogger(__name__)

@dataclass
class AudioInfo:
    """Container for audio file metadata."""
    path: Path
    duration_seconds: float
    bitrate: int
    sample_rate: int
    channels: int
    codec: str
    file_size_bytes: int

    @property
    def duration_str(self) -> str:
        """Format duration as MM:SS."""
        seconds = int(self.duration_seconds)
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes:02d}:{secs:02d}"

    @property
    def quality_label(self) -> str:
        """Return a human-readable quality label."""
        if self.bitrate >= 320000:
            return "High Quality"
        elif self.bitrate >= 192000:
            return "Medium Quality"
        elif self.bitrate >= 128000:
            return "Standard"
        else:
            return "Low Quality"

class AudioProcessor:
    """Process and analyze audio files using ffprobe."""

    def __init__(self, ffprobe_path: str = "ffprobe"):
        self.ffprobe_path = ffprobe_path

    def probe_audio(self, audio_path: Path) -> Optional[AudioInfo]:
        """Extract audio metadata using ffprobe."""
        try:
            cmd = [
                self.ffprobe_path,
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format',
                '-show_streams',
                str(audio_path)
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            data = json.loads(result.stdout)

            audio_stream = self._find_audio_stream(data)
            if not audio_stream:
                logger.warning(f"No audio stream found in {audio_path}")
                return None

            format_data = data['format']

            return AudioInfo(
                path=audio_path,
                duration_seconds=float(format_data.get('duration', 0)),
                bitrate=int(format_data.get('bit_rate', 0)),
                sample_rate=int(audio_stream.get('sample_rate', 0)),
                channels=int(audio_stream.get('channels', 0)),
                codec=audio_stream.get('codec_name', 'unknown'),
                file_size_bytes=int(format_data.get('size', 0))
            )

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to probe audio {audio_path}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error processing {audio_path}: {e}")
            return None

    def _find_audio_stream(self, data: dict) -> dict:
        """Find the first audio stream in the probe data."""
        for stream in data.get('streams', []):
            if stream.get('codec_type') == 'audio':
                return stream
        return {}
