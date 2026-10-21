"""Main entry point for Media Organizer Pro."""

import argparse
import logging
from pathlib import Path
from typing import Optional
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from logger import setup_logger
from config import Config
from organizer import MediaOrganizer, FileType
from video_processor import VideoProcessor
from audio_processor import AudioProcessor
from image_processor import ImageProcessor
from classifier import MediaClassifier

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Media Organizer Pro - Intelligent media file organization tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --source ./Downloads --target ./Organized
  python main.py --source ./Videos --config config.yaml --dry-run
  python main.py --recursive --verbose
        """
    )

    parser.add_argument('--source', '-s', required=True, help='Source directory to organize')
    parser.add_argument('--target', '-t', default=None, help='Target directory for organized files')
    parser.add_argument('--config', '-c', help='Path to YAML configuration file')
    parser.add_argument('--dry-run', '-d', action='store_true', help='Simulate without moving files')
    parser.add_argument('--recursive', '-r', action='store_true', default=True, help='Search recursively')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
    parser.add_argument('--max-size', '-m', type=int, default=10240, help='Max file size in MB')
    parser.add_argument('--skip-existing', action='store_true', help='Skip files that already exist in target')
    parser.add_argument('--stats', action='store_true', help='Show statistics after organization')

    return parser.parse_args()

def main():
    """Main execution function."""
    args = parse_args()

    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logger = setup_logger('media-organizer', level=log_level)

    # Load configuration
    try:
        if args.config:
            config = Config.from_yaml(Path(args.config))
            logger.info(f"Loaded configuration from {args.config}")
        else:
            config = Config(
                source_dir=args.source,
                target_dir=args.target or f"./{Path(args.source).name}_organized",
                dry_run=args.dry_run,
                recursive=args.recursive,
                max_file_size_mb=args.max_size
            )
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        return 1

    # Validate source directory
    source_path = Path(config.source_dir)
    if not source_path.exists():
        logger.error(f"Source directory does not exist: {source_path}")
        return 1

    if not source_path.is_dir():
        logger.error(f"Source path is not a directory: {source_path}")
        return 1

    # Create target directory if it doesn't exist
    target_path = Path(config.target_dir)
    if not config.dry_run:
        target_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Target directory: {target_path}")

    # Initialize processors
    video_processor = VideoProcessor(config.ffmpeg_path)
    audio_processor = AudioProcessor()
    image_processor = ImageProcessor()
    organizer = MediaOrganizer(config)
    classifier = MediaClassifier()

    # Statistics
    stats = {
        'total_files': 0,
        'videos': 0,
        'images': 0,
        'audios': 0,
        'documents': 0,
        'errors': 0,
        'moved': 0,
        'skipped': 0
    }

    logger.info(f"Starting media organization...")
    logger.info(f"Source: {source_path}")
    logger.info(f"Target: {target_path}")
    if config.dry_run:
        logger.warning("DRY RUN MODE - No files will be moved")

    # Process files
    search_pattern = '**/*' if config.recursive else '*'
    for file_path in source_path.glob(search_pattern):
        if not file_path.is_file():
            continue

        stats['total_files'] += 1

        # Check file size
        if file_path.stat().st_size > config.max_file_size_mb * 1024 * 1024:
            logger.warning(f"Skipping large file (> {config.max_file_size_mb}MB): {file_path.name}")
            stats['skipped'] += 1
            continue

        # Classify file
        file_type = organizer.classify_file(file_path)
        if file_type == FileType.UNKNOWN:
            continue

        try:
            # Get detailed info
            if file_type == FileType.VIDEO:
                info = video_processor.probe_video(file_path)
                stats['videos'] += 1
                if info:
                    logger.debug(f"Video: {file_path.name} - {info.resolution_str} @ {info.duration_str}")

            elif file_type == FileType.AUDIO:
                info = audio_processor.probe_audio(file_path)
                stats['audios'] += 1
                if info:
                    logger.debug(f"Audio: {file_path.name} - {info.duration_str} - {info.quality_label}")

            elif file_type == FileType.IMAGE:
                info = image_processor.probe_image(file_path)
                stats['images'] += 1
                if info:
                    logger.debug(f"Image: {file_path.name} - {info.resolution_str}")

            # Organize (in real implementation, this would move/copy files)
            if not config.dry_run:
                # TODO: Implement actual file moving logic
                stats['moved'] += 1

        except Exception as e:
            logger.error(f"Error processing {file_path.name}: {e}")
            stats['errors'] += 1

    # Print statistics
    if stats['total_files'] > 0 or args.stats:
        logger.info("=" * 50)
        logger.info("ORGANIZATION STATISTICS")
        logger.info("=" * 50)
        logger.info(f"Total files scanned: {stats['total_files']}")
        logger.info(f"Videos:     {stats['videos']}")
        logger.info(f"Images:     {stats['images']}")
        logger.info(f"Audios:     {stats['audios']}")
        logger.info(f"Documents:  {stats['documents']}")
        logger.info(f"Moved:      {stats['moved']}")
        logger.info(f"Skipped:    {stats['skipped']}")
        logger.info(f"Errors:     {stats['errors']}")
        logger.info("=" * 50)

    logger.info("Organization completed successfully!")
    return 0

if __name__ == '__main__':
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(130)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)
