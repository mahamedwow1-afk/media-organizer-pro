# Media Organizer Pro

<div align="center">

![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)
![GitHub Stars](https://img.shields.io/github/stars/mahamedwow1-afk/media-organizer-pro?style=for-the-badge)
![GitHub Forks](https://img.shields.io/github/forks/mahamedwow1-afk/media-organizer-pro?style=for-the-badge)

**Intelligent media file organization tool built with Python.**

Automatically organizes your video, image, and audio files into structured folders using metadata analysis and machine learning.

[🚀 Demo](#-demo) • [📖 Installation](#-installation) • [⚙️ Configuration](#-configuration) • [🤝 Contributing](#-contributing)

</div>

---

## 🎯 Features

| Feature | Description |
|---------|-------------|
| 🎬 **Video Analysis** | Extract metadata (resolution, duration, codec, FPS) using FFmpeg |
| 🎵 **Audio Processing** | Analyze bitrate, sample rate, channels, and quality |
| 🖼️ **Image Classification** | Detect resolution, megapixels, and animated GIFs |
| 🤖 **ML Classification** | Optional machine learning for content-aware organization |
| ⚙️ **Configurable** | YAML-based configuration for custom workflows |
| 🔍 **Dry-Run Mode** | Preview changes before applying them |
| 📊 **Statistics** | Detailed reporting of organization results |
| 🔄 **Recursive Search** | Organize entire directory trees |

---

## 📸 Demo

```bash
$ python main.py --source ./Downloads --target ./Organized --verbose

[INFO] Starting media organization...
[INFO] Source: ./Downloads
[INFO] Target: ./Organized
[DEBUG] Video: vacation.mp4 - 1920x1080 @ 02:15:30
[DEBUG] Audio: podcast.mp3 - 04:32 - High Quality
[DEBUG] Image: photo.jpg - 4032x3024
[INFO] ==================================================
[INFO] ORGANIZATION STATISTICS
[INFO] ==================================================
[INFO] Total files scanned: 156
[INFO] Videos:     45
[INFO] Images:     78
[INFO] Audios:     23
[INFO] Moved:      146
[INFO] Skipped:    3
[INFO] Errors:     0
[INFO] ==================================================
[INFO] Organization completed successfully!
```

---

## 📦 Installation

### Prerequisites

- Python 3.9 or higher
- FFmpeg (for video/audio processing)
- [Optional] TensorFlow (for ML classification)

### Quick Install

```bash
# Clone the repository
git clone https://github.com/mahamedwow1-afk/media-organizer-pro.git
cd media-organizer-pro

# Install dependencies
pip install -r requirements.txt

# Optional: Install FFmpeg (if not already installed)
# Windows: choco install ffmpeg
# macOS: brew install ffmpeg
# Linux: sudo apt install ffmpeg
```

### Development Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest
```

---

## ⚙️ Configuration

Create a `config.yaml` file in the project root:

```yaml
source_dir: "./Downloads"
target_dir: "./Organized"
recursive: true
dry_run: false
max_file_size_mb: 10240

video_extensions:
  - ".mp4"
  - ".avi"
  - ".mkv"
  - ".mov"

image_extensions:
  - ".jpg"
  - ".jpeg"
  - ".png"
  - ".gif"

audio_extensions:
  - ".mp3"
  - ".wav"
  - ".flac"

# Enable ML classification (requires tensorflow)
use_ml_classification: false
```

---

## 🚀 Usage

### Basic Usage

```bash
# Organize files from Downloads to Organized folder
python main.py --source ./Downloads --target ./Organized

# Recursive mode (default)
python main.py --source ./Media --recursive

# Dry-run mode (preview only)
python main.py --source ./Downloads --dry-run

# With custom configuration
python main.py --source ./Videos --config config.yaml --verbose

# Show statistics after completion
python main.py --source ./Photos --target ./Images --stats
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--source, -s` | Source directory | Required |
| `--target, -t` | Target directory | `./{source}_organized` |
| `--config, -c` | YAML config file | None |
| `--dry-run, -d` | Preview without moving | `False` |
| `--recursive, -r` | Search subdirectories | `True` |
| `--verbose, -v` | Enable debug logging | `False` |
| `--max-size, -m` | Max file size (MB) | `10240` |
| `--stats` | Show statistics | `False` |

---

## 📁 Project Structure

```
media-organizer-pro/
├── main.py                  # Entry point
├── src/
│   ├── __init__.py          # Package init
│   ├── organizer.py         # Main organization logic
│   ├── video_processor.py   # Video metadata extraction
│   ├── audio_processor.py   # Audio metadata extraction
│   ├── image_processor.py   # Image analysis
│   ├── classifier.py        # ML-based classification
│   ├── config.py            # Configuration management
│   └── logger.py            # Logging setup
├── tests/
│   └── test_organizer.py    # Test suite
├── config.yaml              # Example configuration
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test class
pytest tests/test_organizer.py::TestMediaType -v

# Run with verbose output
pytest -v -s
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Mahamed Yasser**
- Python Developer & Video Editor
- Qalyubia, Egypt
- [GitHub Profile](https://github.com/mahamedwow1-afk)

---

## 🙏 Acknowledgments

- [FFmpeg](https://ffmpeg.org/) - For powerful multimedia processing
- [Python](https://www.python.org/) - The backbone of this project
- [GitHub](https://github.com) - For hosting and collaboration

---

<div align="center">

Made with ❤️ by [Mahamed Yasser](https://github.com/mahamedwow1-afk)

</div>
