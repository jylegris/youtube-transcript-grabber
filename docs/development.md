# Development Guide

Guide for developers wanting to contribute to or understand the YouTube Transcript Grabber project.

## Project Architecture

### Overview

The project follows a modular architecture with clear separation of concerns:

```
src/youtube_transcript_grabber/
├── __init__.py          # Package initialization and exports
├── grabber.py           # Core transcript extraction logic
├── cli.py              # Command-line interface
└── exceptions.py       # Custom exception definitions
```

### Core Components

#### 1. YouTubeTranscriptGrabber (`grabber.py`)

The main class responsible for:
- Browser automation using Playwright
- YouTube page navigation
- DOM element interaction
- Transcript data extraction
- Error handling and retries

**Key methods:**
- `extract_transcript()`: Single video processing
- `extract_multiple()`: Batch processing
- Internal helper methods for navigation and parsing

#### 2. Command Line Interface (`cli.py`)

Built with Click framework, provides:
- Argument parsing and validation
- Output formatting (text, JSON, raw)
- File I/O operations
- User-friendly error messages

#### 3. Exception Hierarchy (`exceptions.py`)

Custom exception classes for specific error conditions:
- `YouTubeTranscriptGrabberError`: Base exception
- `TranscriptNotFoundError`: No transcript available
- `VideoNotFoundError`: Video not accessible
- `BrowserError`: Browser automation issues

## Development Setup

### Prerequisites

- Python 3.8+
- Git
- Virtual environment tool (venv, virtualenv, or conda)

### Initial Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/youtube-transcript-grabber.git
   cd youtube-transcript-grabber
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies:**
   ```bash
   pip install -e .[dev]
   playwright install chromium
   ```

4. **Verify installation:**
   ```bash
   youtube-transcript-grabber --help
   pytest --version
   black --version
   ```

### Development Dependencies

The development environment includes:

- **pytest**: Testing framework
- **pytest-asyncio**: Async testing support
- **black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking
- **pre-commit**: Git hooks for quality assurance

### Code Quality Tools

#### Formatting with Black

```bash
# Format all code
black src/ tests/ examples/

# Check formatting without changing files
black --check src/
```

#### Import Sorting with isort

```bash
# Sort imports
isort src/ tests/ examples/

# Check import sorting
isort --check-only src/
```

#### Linting with flake8

```bash
# Run linter
flake8 src/ tests/

# With specific configuration
flake8 --max-line-length=88 --extend-ignore=E203,W503 src/
```

#### Type Checking with mypy

```bash
# Type check
mypy src/youtube_transcript_grabber

# With specific configuration
mypy --ignore-missing-imports src/
```

## Testing

### Test Structure

```
tests/
├── __init__.py
├── test_grabber.py      # Core grabber functionality
├── test_cli.py          # CLI interface tests
├── test_exceptions.py   # Exception handling tests
└── fixtures/           # Test data and fixtures
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=youtube_transcript_grabber

# Run specific test file
pytest tests/test_grabber.py

# Run with verbose output
pytest -v

# Run in parallel (if pytest-xdist installed)
pytest -n auto
```

### Test Categories

1. **Unit Tests**: Test individual functions and methods
2. **Integration Tests**: Test browser automation workflows
3. **CLI Tests**: Test command-line interface
4. **Error Handling Tests**: Test exception scenarios

### Writing Tests

Example test structure:

```python
import pytest
from youtube_transcript_grabber import YouTubeTranscriptGrabber
from youtube_transcript_grabber.exceptions import VideoNotFoundError

class TestYouTubeTranscriptGrabber:
    
    def test_extract_transcript_success(self):
        """Test successful transcript extraction."""
        grabber = YouTubeTranscriptGrabber(headless=True)
        transcript = grabber.extract_transcript("valid_video_id")
        
        assert isinstance(transcript, list)
        assert len(transcript) > 0
        assert all(isinstance(segment, tuple) for segment in transcript)
    
    def test_extract_transcript_invalid_video(self):
        """Test extraction with invalid video ID."""
        grabber = YouTubeTranscriptGrabber(headless=True)
        
        with pytest.raises(VideoNotFoundError):
            grabber.extract_transcript("invalid_video_id")
```

## Browser Automation Details

### Playwright Integration

The project uses Playwright for browser automation:

**Key concepts:**
- **Browser**: The browser instance (Chromium, Firefox, WebKit)
- **Context**: Isolated browser session
- **Page**: Individual tab/page within context

**Navigation flow:**
1. Launch browser with specified options
2. Create new context and page
3. Navigate to YouTube video URL
4. Wait for page load and elements
5. Interact with transcript UI elements
6. Extract transcript data
7. Clean up browser resources

### Element Selection Strategy

The grabber uses multiple selector strategies:

1. **Text-based selectors**: `button:has-text('Show transcript')`
2. **CSS selectors**: `.segment-timestamp`, `.segment-text`
3. **Role-based selectors**: `page.get_by_role("button", name="Show transcript")`

This provides resilience against minor UI changes.

### Error Recovery

Built-in error recovery mechanisms:

- **Retry logic**: Multiple attempts with delays
- **Fallback selectors**: Alternative element selection methods
- **Timeout handling**: Graceful timeout with useful error messages
- **Resource cleanup**: Ensures browser processes are closed

## Contributing Guidelines

### Code Style

- Follow PEP 8 Python style guide
- Use Black for formatting (line length: 88)
- Use meaningful variable and function names
- Add docstrings for all public functions and classes
- Include type hints where appropriate

### Git Workflow

1. **Create feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make changes and test:**
   ```bash
   # Make your changes
   # Run tests
   pytest
   # Check code quality
   black --check src/
   flake8 src/
   mypy src/
   ```

3. **Commit changes:**
   ```bash
   git add .
   git commit -m "Add: descriptive commit message"
   ```

4. **Push and create PR:**
   ```bash
   git push origin feature/your-feature-name
   # Create pull request on GitHub
   ```

### Commit Message Format

Use conventional commit format:

- `Add:` New features
- `Fix:` Bug fixes
- `Update:` Modifications to existing features
- `Remove:` Removing features or files
- `Docs:` Documentation changes
- `Test:` Test-related changes

### Pull Request Guidelines

- Provide clear description of changes
- Include tests for new functionality
- Update documentation if needed
- Ensure all CI checks pass
- Link to related issues

## Release Process

### Version Management

- Follow semantic versioning (SemVer)
- Update version in `pyproject.toml`
- Create git tag for releases
- Maintain CHANGELOG.md

### Release Steps

1. **Update version and changelog**
2. **Create release branch:**
   ```bash
   git checkout -b release/v1.2.0
   ```
3. **Final testing and cleanup**
4. **Create PR to main branch**
5. **Tag release after merge:**
   ```bash
   git tag v1.2.0
   git push origin v1.2.0
   ```
6. **GitHub Actions will handle PyPI deployment**

## Debugging Tips

### Local Development

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Use visible browser for debugging
grabber = YouTubeTranscriptGrabber(
    headless=False,
    slow_mo=1000,  # Slow down actions
    timeout=60000  # Longer timeout
)

# Take screenshots for debugging
# Add to grabber code: page.screenshot(path="debug.png")
```

### Common Development Issues

1. **Selector not found**: YouTube UI changed
   - Inspect element in browser
   - Update selectors in code
   - Test with multiple videos

2. **Tests failing**: Environment or network issues
   - Check test video availability
   - Verify network connectivity
   - Update test expectations

3. **Type errors**: Missing or incorrect type hints
   - Add proper type annotations
   - Import types from typing module
   - Run mypy to catch issues

## Performance Considerations

### Optimization Strategies

- **Minimize browser interactions**: Batch operations when possible
- **Use efficient selectors**: Prefer ID and class selectors over text
- **Implement caching**: Store results for repeated requests
- **Add rate limiting**: Respect YouTube's servers

### Memory Management

- **Close browser contexts**: Ensure proper cleanup
- **Process data incrementally**: Don't hold large datasets in memory
- **Use generators**: For large batch operations

## Security Considerations

### Best Practices

- **No credential storage**: Never store YouTube credentials
- **Respect robots.txt**: Follow YouTube's usage guidelines
- **Rate limiting**: Implement reasonable delays between requests
- **Error handling**: Don't expose internal details in error messages

### Privacy

- **No data collection**: Don't store user data or viewing habits
- **Minimal logging**: Only log what's necessary for debugging
- **Secure defaults**: Use secure configuration options