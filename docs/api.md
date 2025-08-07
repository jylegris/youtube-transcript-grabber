# API Reference

Complete API documentation for YouTube Transcript Grabber.

## YouTubeTranscriptGrabber

Main class for extracting transcripts from YouTube videos.

### Constructor

```python
YouTubeTranscriptGrabber(
    headless: bool = True,
    browser_type: str = "chromium",
    timeout: int = 30000,
    slow_mo: int = 100,
)
```

**Parameters:**
- `headless` (bool): Run browser in headless mode. Default: `True`
- `browser_type` (str): Browser to use. Options: `"chromium"`, `"firefox"`, `"webkit"`. Default: `"chromium"`
- `timeout` (int): Timeout in milliseconds for operations. Default: `30000`
- `slow_mo` (int): Delay in milliseconds between actions. Default: `100`

### Methods

#### extract_transcript()

```python
extract_transcript(video_id: str) -> List[Tuple[str, str]]
```

Extract transcript from a YouTube video.

**Parameters:**
- `video_id` (str): YouTube video ID (e.g., "Iv-u8hwjHw4")

**Returns:**
- `List[Tuple[str, str]]`: List of (timestamp, text) tuples

**Raises:**
- `VideoNotFoundError`: If video is not accessible
- `TranscriptNotFoundError`: If no transcript is available
- `BrowserError`: If browser automation fails

**Example:**
```python
grabber = YouTubeTranscriptGrabber()
transcript = grabber.extract_transcript("Iv-u8hwjHw4")
for timestamp, text in transcript:
    print(f"{timestamp}: {text}")
```

#### extract_multiple()

```python
extract_multiple(video_ids: List[str]) -> Dict[str, List[Tuple[str, str]]]
```

Extract transcripts from multiple videos.

**Parameters:**
- `video_ids` (List[str]): List of YouTube video IDs

**Returns:**
- `Dict[str, List[Tuple[str, str]]]`: Dictionary mapping video IDs to their transcript tuples

**Example:**
```python
grabber = YouTubeTranscriptGrabber()
results = grabber.extract_multiple(["Iv-u8hwjHw4", "dQw4w9WgXcQ"])
for video_id, transcript in results.items():
    print(f"Video {video_id}: {len(transcript)} segments")
```

## Exceptions

All exceptions inherit from `YouTubeTranscriptGrabberError`.

### YouTubeTranscriptGrabberError

Base exception for all YouTube Transcript Grabber errors.

### TranscriptNotFoundError

Raised when no transcript is found for a video.

**Common causes:**
- Video doesn't have transcripts enabled
- Video is private or removed
- Transcript feature is disabled by the creator

### VideoNotFoundError

Raised when the video is not found or accessible.

**Common causes:**
- Invalid video ID
- Video is private or deleted
- Geographic restrictions

### BrowserError

Raised when browser automation fails.

**Common causes:**
- Browser not installed properly
- Network connectivity issues
- YouTube layout changes

## Command Line Interface

The CLI is available through the `youtube-transcript-grabber` or `ytg` commands.

### Basic Usage

```bash
youtube-transcript-grabber VIDEO_ID [OPTIONS]
```

### Options

- `--output, -o PATH`: Output file path (default: stdout)
- `--format, -f [text|json|raw]`: Output format (default: text)
- `--headless/--no-headless`: Run browser in headless mode (default: True)
- `--browser [chromium|firefox|webkit]`: Browser to use (default: chromium)
- `--timeout INTEGER`: Timeout in milliseconds (default: 30000)
- `--verbose, -v`: Enable verbose output

### Examples

```bash
# Basic extraction
youtube-transcript-grabber Iv-u8hwjHw4

# Save to file
youtube-transcript-grabber Iv-u8hwjHw4 --output transcript.txt

# JSON format
youtube-transcript-grabber Iv-u8hwjHw4 --format json

# Visible browser for debugging
youtube-transcript-grabber Iv-u8hwjHw4 --no-headless --verbose
```

## Type Definitions

### Transcript Segment

```python
Tuple[str, str]
# (timestamp, text)
# Example: ("0:05", "Hello and welcome to this video")
```

### Transcript Data

```python
List[Tuple[str, str]]
# List of transcript segments
# Example: [("0:00", "Welcome"), ("0:05", "Today we'll learn")]
```

## Error Handling Best Practices

```python
from youtube_transcript_grabber import (
    YouTubeTranscriptGrabber,
    TranscriptNotFoundError,
    VideoNotFoundError,
    BrowserError
)

grabber = YouTubeTranscriptGrabber()

try:
    transcript = grabber.extract_transcript("video_id")
    if not transcript:
        print("No transcript content found")
    else:
        print(f"Found {len(transcript)} segments")
        
except TranscriptNotFoundError:
    print("This video doesn't have transcripts available")
except VideoNotFoundError:
    print("Video not found or not accessible")
except BrowserError as e:
    print(f"Browser automation failed: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Configuration Examples

### Performance Optimization

```python
# Fast extraction (headless, short timeout)
grabber = YouTubeTranscriptGrabber(
    headless=True,
    timeout=15000,
    slow_mo=50
)

# Reliable extraction (longer timeout, slower)
grabber = YouTubeTranscriptGrabber(
    headless=True,
    timeout=45000,
    slow_mo=200
)
```

### Debugging Setup

```python
# Visible browser for debugging
grabber = YouTubeTranscriptGrabber(
    headless=False,
    slow_mo=1000,  # Very slow for observation
    timeout=60000
)
```

### Different Browsers

```python
# Firefox
grabber = YouTubeTranscriptGrabber(browser_type="firefox")

# WebKit (Safari-like)
grabber = YouTubeTranscriptGrabber(browser_type="webkit")
```