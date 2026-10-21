"""Image processor for analyzing and organizing image files."""

from pathlib import Path
from dataclasses import dataclass
import logging
from typing import Optional

logger = logging.getLogger(__name__)

@dataclass
class ImageInfo:
    """Container for image file metadata."""
    path: Path
    width: int
    height: int
    format: str
    file_size_bytes: int
    is_animated: bool = False

    @property
    def resolution_str(self) -> str:
        return f"{self.width}x{self.height}"

    @property
    def megapixels(self) -> float:
        return (self.width * self.height) / 1_000_000

    @property
    def quality_label(self) -> str:
        """Return a human-readable quality label."""
        mp = self.megapixels
        if mp >= 12:
            return "High Resolution"
        elif mp >= 5:
            return "Medium Resolution"
        else:
            return "Low Resolution"

class ImageProcessor:
    """Process and analyze image files."""

    def probe_image(self, image_path: Path) -> Optional[ImageInfo]:
        """Extract image metadata."""
        try:
            import PIL
            from PIL import Image
        except ImportError:
            logger.warning("Pillow library not installed. Install with: pip install Pillow")
            return None

        try:
            with Image.open(image_path) as img:
                width, height = img.size
                fmt = img.format or image_path.suffix.lstrip('.')

                is_animated = False
                try:
                    # Check if it's an animated GIF
                    if fmt and fmt.lower() == 'gif':
                        import PIL.GifImagePlugin
                        frame_count = getattr(img, 'n_frames', 1)
                        is_animated = frame_count > 1
                except Exception:
                    pass

                return ImageInfo(
                    path=image_path,
                    width=width,
                    height=height,
                    format=fmt,
                    file_size_bytes=image_path.stat().st_size,
                    is_animated=is_animated
                )
        except Exception as e:
            logger.error(f"Error processing image {image_path}: {e}")
            return None

    def classify_image_quality(self, image_path: Path) -> str:
        """Classify image into quality categories."""
        info = self.probe_image(image_path)
        if not info:
            return "Unknown"

        mp = info.megapixels
        if mp >= 12:
            return "HD+"
        elif mp >= 5:
            return "HD"
        else:
            return "Standard"
