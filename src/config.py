"""Configuration manager for Media Organizer Pro."""

import yaml
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Config:
    source_dir: str = "./input"
    target_dir: str = "./output"
    video_extensions: list[str] = field(default_factory=lambda: ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'])
    image_extensions: list[str] = field(default_factory=lambda: ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'])
    audio_extensions: list[str] = field(default_factory=lambda: ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma'])
    document_extensions: list[str] = field(default_factory=lambda: ['.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx'])
    use_ml_classification: bool = False
    ffmpeg_path: Optional[str] = None
    dry_run: bool = False
    recursive: bool = True
    max_file_size_mb: int = 10240

    @classmethod
    def from_yaml(cls, path: Path) -> 'Config':
        """Load configuration from YAML file."""
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")

        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        return cls(**data)

    def to_dict(self) -> dict:
        """Convert config to dictionary."""
        return {
            'source_dir': self.source_dir,
            'target_dir': self.target_dir,
            'video_extensions': self.video_extensions,
            'image_extensions': self.image_extensions,
            'audio_extensions': self.audio_extensions,
            'document_extensions': self.document_extensions,
            'use_ml_classification': self.use_ml_classification,
            'ffmpeg_path': self.ffmpeg_path,
            'dry_run': self.dry_run,
            'recursive': self.recursive,
            'max_file_size_mb': self.max_file_size_mb,
        }
