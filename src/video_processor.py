"""Video processor using FFmpeg for analyzing and organizing video files."""

import subprocess
import json
from pathlib import Path
from dataclasses import dataclass
from typing import Optional
import logging

logger = logging.getLogger(__name__)

@dataclass
class VideoInfo:
    """Container for video file metadata."""
    path: Path
    duration_seconds: float
    resolution: tuple[int, int]
    codec: str
    bitrate: int
    fps: float
    file_size_bytes: int
    has_audio: bool

    @property
    def duration_str(self) -> str:
        """Format duration as HH:MM:SS."""
        seconds = int(self.duration_seconds)
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    @property
    def resolution_str(self) -> str:
        return f"{self.resolution[0]}x{self.resolution[1]}"

class VideoProcessor:
    """Process and analyze video files using FFmpeg."""

    def __init__(self, ffmpeg_path: Optional[str] = None):
        self.ffmpeg_path = ffmpeg_path or "ffmpeg"
        self.ffprobe_path = ffmpeg_path.replace("ffmpeg", "ffprobe") if ffmpeg_path else "ffprobe"

    def probe_video(self, video_path: Path) -> Optional[VideoInfo]:
        """Extract video metadata using ffprobe."""
        try:
            cmd = [
                self.ffprobe_path,
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format',
                '-show_streams',
                str(video_path)
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            data = json.loads(result.stdout)

            video_stream = self._find_video_stream(data)
            if not video_stream:
                logger.warning(f"No video stream found in {video_path}")
                return None

            format_data = data['format']
            resolution = self._parse_resolution(video_stream)
            codec = video_stream.get('codec_name', 'unknown')

            return VideoInfo(
                path=video_path,
                duration_seconds=float(format_data.get('duration', 0)),
                resolution=resolution,
                codec=codec,
                bitrate=int(format_data.get('bit_rate', 0)),
                fps=float(video_stream.get('r_frame_rate', '0/1').split('/')[0]) /
                    float(video_stream.get('r_frame_rate', '0/1').split('/')[1]) if '/' in video_stream.get('r_frame_rate', '0/1') else 0,
                file_size_bytes=int(format_data.get('size', 0)),
                has_audio='audio' in data.get('streams', [])
            )

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to probe video {video_path}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error processing {video_path}: {e}")
            return None

    def _find_video_stream(self, data: dict) -> dict:
        """Find the first video stream in the probe data."""
        for stream in data.get('streams', []):
            if stream.get('codec_type') == 'video':
                return stream
        return {}

    def _parse_resolution(self, stream: dict) -> tuple[int, int]:
        """Parse resolution from video stream."""
        width = int(stream.get('width', 0))
        height = int(stream.get('height', 0))
        return (width, height) if width > 0 and height > 0 else (0, 0)

    def trim_video(self, input_path: Path, output_path: Path, start: float, end: float) -> bool:
        """Trim a video file to the specified time range."""
        cmd = [
            self.ffmpeg_path,
            '-y',
            '-ss', str(start),
            '-i', str(input_path),
            '-to', str(end),
            '-c', 'copy',
            str(output_path)
        ]
        try:
            subprocess.run(cmd, capture_output=True, check=True)
            return True
        except subprocess.CalledProcessError:
            return False
