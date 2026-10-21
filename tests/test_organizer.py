"""Test suite for Media Organizer Pro."""

import pytest
from pathlib import Path
import tempfile
import shutil
from unittest.mock import patch, MagicMock

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from organizer import MediaOrganizer, FileType
from config import Config
from video_processor import VideoProcessor
from audio_processor import AudioProcessor
from image_processor import ImageProcessor
from classifier import MediaClassifier


class TestMediaType:
    """Test file type classification."""

    def test_video_classification(self):
        """Test video file classification."""
        organizer = MediaOrganizer()
        video_files = [
            Path("test.mp4"),
            Path("test.AVI"),
            Path("test.mkv"),
            Path("test.mov"),
        ]
        for video in video_files:
            assert organizer.classify_file(video) == FileType.VIDEO

    def test_image_classification(self):
        """Test image file classification."""
        organizer = MediaOrganizer()
        image_files = [
            Path("test.jpg"),
            Path("test.PNG"),
            Path("test.gif"),
            Path("test.webp"),
        ]
        for image in image_files:
            assert organizer.classify_file(image) == FileType.IMAGE

    def test_audio_classification(self):
        """Test audio file classification."""
        organizer = MediaOrganizer()
        audio_files = [
            Path("test.mp3"),
            Path("test.wav"),
            Path("test.flac"),
            Path("test.ogg"),
        ]
        for audio in audio_files:
            assert organizer.classify_file(audio) == FileType.AUDIO

    def test_document_classification(self):
        """Test document file classification."""
        organizer = MediaOrganizer()
        doc_files = [
            Path("test.pdf"),
            Path("test.docx"),
            Path("test.txt"),
            Path("test.xlsx"),
        ]
        for doc in doc_files:
            assert organizer.classify_file(doc) == FileType.DOCUMENT

    def test_unknown_classification(self):
        """Test unknown file type classification."""
        organizer = MediaOrganizer()
        unknown_files = [
            Path("test.xyz"),
            Path("test.dat"),
            Path("test.unknown"),
        ]
        for unknown in unknown_files:
            assert organizer.classify_file(unknown) == FileType.UNKNOWN


class TestConfig:
    """Test configuration management."""

    def test_default_config(self):
        """Test default configuration values."""
        config = Config()
        assert config.source_dir == "./input"
        assert config.target_dir == "./output"
        assert config.dry_run is False
        assert config.recursive is True
        assert config.max_file_size_mb == 10240

    def test_custom_config(self):
        """Test custom configuration values."""
        config = Config(
            source_dir="./Videos",
            target_dir="./Organized",
            dry_run=True,
            max_file_size_mb=5000
        )
        assert config.source_dir == "./Videos"
        assert config.target_dir == "./Organized"
        assert config.dry_run is True
        assert config.max_file_size_mb == 5000

    def test_to_dict(self):
        """Test configuration serialization."""
        config = Config(source_dir="./test")
        config_dict = config.to_dict()
        assert config_dict['source_dir'] == "./test"
        assert 'target_dir' in config_dict
        assert 'video_extensions' in config_dict


class TestVideoProcessor:
    """Test video processing."""

    @patch('subprocess.run')
    def test_probe_video_success(self, mock_run):
        """Test successful video probing."""
        mock_result = MagicMock()
        mock_result.stdout = '''
        {
            "format": {
                "duration": "120.5",
                "size": "50000000",
                "bit_rate": "3500000"
            },
            "streams": [
                {
                    "codec_type": "video",
                    "width": 1920,
                    "height": 1080,
                    "codec_name": "h264",
                    "r_frame_rate": "30/1"
                },
                {
                    "codec_type": "audio",
                    "codec_name": "aac"
                }
            ]
        }
        '''
        mock_run.return_value = mock_result

        processor = VideoProcessor()
        video_path = Path("test.mp4")
        info = processor.probe_video(video_path)

        assert info is not None
        assert info.duration_seconds == pytest.approx(120.5)
        assert info.resolution == (1920, 1080)
        assert info.codec == "h264"
        assert info.has_audio is True

    @patch('subprocess.run')
    def test_probe_video_failure(self, mock_run):
        """Test video probing failure."""
        mock_run.side_effect = Exception("FFprobe error")
        processor = VideoProcessor()
        info = processor.probe_video(Path("invalid.mp4"))
        assert info is None


class TestAudioProcessor:
    """Test audio processing."""

    @patch('subprocess.run')
    def test_probe_audio_success(self, mock_run):
        """Test successful audio probing."""
        mock_result = MagicMock()
        mock_result.stdout = '''
        {
            "format": {
                "duration": "240.0",
                "size": "10000000",
                "bit_rate": "320000"
            },
            "streams": [
                {
                    "codec_type": "audio",
                    "codec_name": "mp3",
                    "sample_rate": "44100",
                    "channels": 2
                }
            ]
        }
        '''
        mock_run.return_value = mock_result

        processor = AudioProcessor()
        audio_path = Path("test.mp3")
        info = processor.probe_audio(audio_path)

        assert info is not None
        assert info.duration_seconds == 240.0
        assert info.bitrate == 320000
        assert info.sample_rate == 44100
        assert info.channels == 2
        assert info.quality_label == "High Quality"

    @patch('subprocess.run')
    def test_probe_audio_no_stream(self, mock_run):
        """Test audio probing when no audio stream exists."""
        mock_result = MagicMock()
        mock_result.stdout = '{"streams": []}'
        mock_run.return_value = mock_result

        processor = AudioProcessor()
        info = processor.probe_audio(Path("invalid.mp3"))
        assert info is None


class TestImageProcessor:
    """Test image processing."""

    @patch('PIL.Image.open')
    def test_probe_image_success(self, mock_open):
        """Test successful image probing."""
        mock_img = MagicMock()
        mock_img.size = (1920, 1080)
        mock_img.format = 'JPEG'
        mock_img.__enter__ = MagicMock(return_value=mock_img)
        mock_img.__exit__ = MagicMock(return_value=False)
        mock_open.return_value = mock_img

        with tempfile.NamedTemporaryFile(suffix='.jpg') as tmp:
            processor = ImageProcessor()
            info = processor.probe_image(Path(tmp.name))

            assert info is not None
            assert info.width == 1920
            assert info.height == 1080
            assert info.quality_label == "High Resolution"
            assert info.megapixels == pytest.approx(20.736)

    @patch('PIL.Image.open')
    def test_probe_image_animated_gif(self, mock_open):
        """Test animated GIF detection."""
        mock_img = MagicMock()
        mock_img.size = (480, 360)
        mock_img.format = 'GIF'
        mock_img.n_frames = 10
        mock_img.__enter__ = MagicMock(return_value=mock_img)
        mock_img.__exit__ = MagicMock(return_value=False)
        mock_open.return_value = mock_img

        with tempfile.NamedTemporaryFile(suffix='.gif') as tmp:
            processor = ImageProcessor()
            info = processor.probe_image(Path(tmp.name))

            assert info is not None
            assert info.is_animated is True


class TestClassifier:
    """Test ML classifier."""

    def test_classify_media_placeholder(self):
        """Test classifier placeholder implementation."""
        classifier = MediaClassifier()
        result = classifier.classify_media(Path("test.mp4"))

        assert isinstance(result, dict)
        assert 'categories' in result
        assert 'confidence' in result

    @patch('tensorflow')
    def test_train_placeholder(self, mock_tf):
        """Test training placeholder."""
        classifier = MediaClassifier()
        with tempfile.TemporaryDirectory() as tmpdir:
            result = classifier.train(Path(tmpdir))
            assert result is True


class TestIntegration:
    """Integration tests for the complete system."""

    def test_full_classification_pipeline(self):
        """Test the complete file classification pipeline."""
        organizer = MediaOrganizer()
        processor = VideoProcessor()

        # Test classification
        video_file = Path("sample.mp4")
        file_type = organizer.classify_file(video_file)
        assert file_type == FileType.VIDEO

        # Test folder name generation
        folder_name = organizer.generate_folder_name(video_file, file_type)
        assert "Video" in folder_name

    def test_config_validation(self):
        """Test configuration validation."""
        config = Config()
        assert config.source_dir is not None
        assert config.target_dir is not None
        assert len(config.video_extensions) > 0
        assert len(config.image_extensions) > 0
        assert len(config.audio_extensions) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
