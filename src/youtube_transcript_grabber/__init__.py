"""
YouTube Transcript Grabber

A robust, browser-based YouTube transcript extractor that navigates 
YouTube's UI like a human to extract accurate transcripts with timestamps.
"""

from .grabber import YouTubeTranscriptGrabber
from .exceptions import (
    YouTubeTranscriptGrabberError,
    TranscriptNotFoundError,
    VideoNotFoundError,
    BrowserError,
)

__version__ = "0.1.0"
__author__ = "Joel Legris"
__email__ = "jylegris@users.noreply.github.com"

__all__ = [
    "YouTubeTranscriptGrabber",
    "YouTubeTranscriptGrabberError", 
    "TranscriptNotFoundError",
    "VideoNotFoundError",
    "BrowserError",
]
