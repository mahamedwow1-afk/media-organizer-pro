"""
Media Organizer Pro - Professional Automation Tool
Organizes video, image, and audio files intelligently using FFmpeg and ML.
"""

from pathlib import Path
from datetime import datetime
from enum import Enum
import logging

class FileType(Enum):
    VIDEO = "video"
    IMAGE = "image"
    AUDIO = "audio"
    DOCUMENT = "document"
    UNKNOWN = "unknown"

class MediaOrganizer:
    def __init__(self, config: dict | None = None):
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

    def classify_file(self, file_path: Path) -> FileType:
        """Classify file type based on extension."""
        extensions = {
            FileType.VIDEO: {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'},
            FileType.IMAGE: {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'},
            FileType.AUDIO: {'.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma'},
            FileType.DOCUMENT: {'.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx'},
        }

        suffix = file_path.suffix.lower()
        for ftype, exts in extensions.items():
            if suffix in exts:
                return ftype
        return FileType.UNKNOWN

    def generate_folder_name(self, file_path: Path, ftype: FileType) -> str:
        """Generate meaningful folder name for the file."""
        date = file_path.stat().st_mtime
        dt = datetime.fromtimestamp(date)
        return dt.strftime(f"{ftype.value.title()}/{%Y}/%B")
