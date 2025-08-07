# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- GitHub Actions CI/CD pipeline
- Comprehensive documentation in `docs/` directory
- Example scripts in `examples/` directory
- Issue and PR templates
- Contributing guidelines
- Code of conduct

### Changed
- Improved project structure for open source development
- Enhanced error handling and user feedback

## [0.1.0] - 2025-01-XX

### Added
- Initial implementation of YouTube transcript extraction
- Support for Chromium, Firefox, and WebKit browsers
- Command-line interface with multiple output formats
- Batch processing capabilities
- Comprehensive error handling with custom exceptions
- Type hints throughout the codebase
- MIT license

### Features
- **Core Functionality**
  - Extract transcripts from YouTube videos using browser automation
  - Support for headless and visible browser modes
  - Configurable timeouts and delays
  - Automatic retry mechanisms

- **Command Line Interface**
  - Simple CLI with `youtube-transcript-grabber` command
  - Multiple output formats: text, JSON, raw
  - File output support
  - Verbose logging option

- **Python API**
  - `YouTubeTranscriptGrabber` class for programmatic access
  - Single and batch video processing
  - Custom exception hierarchy for error handling
  - Type-safe interfaces

- **Browser Support**
  - Chromium (default)
  - Firefox
  - WebKit/Safari

- **Output Formats**
  - Plain text with timestamps
  - JSON structured data
  - Raw Python data structures

### Technical Details
- Built with Playwright for browser automation
- Uses Click for CLI interface
- Follows Python packaging best practices
- Comprehensive type annotations
- Modular, extensible architecture

### Dependencies
- playwright>=1.40.0
- click>=8.0.0
- typing-extensions>=4.0.0

### Development Dependencies
- pytest>=7.0.0
- pytest-asyncio>=0.21.0
- black>=22.0.0
- isort>=5.10.0
- flake8>=4.0.0
- mypy>=0.991
- pre-commit>=2.20.0

[Unreleased]: https://github.com/yourusername/youtube-transcript-grabber/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/yourusername/youtube-transcript-grabber/releases/tag/v0.1.0