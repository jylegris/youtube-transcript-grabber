"""
Custom exceptions for YouTube Transcript Grabber.
"""


class YouTubeTranscriptGrabberError(Exception):
    """Base exception for YouTube Transcript Grabber."""
    pass


class TranscriptNotFoundError(YouTubeTranscriptGrabberError):
    """Raised when no transcript is found for a video."""
    pass


class VideoNotFoundError(YouTubeTranscriptGrabberError):
    """Raised when the video is not found or accessible."""
    pass


class BrowserError(YouTubeTranscriptGrabberError):
    """Raised when browser automation fails."""
    pass


class TimeoutError(YouTubeTranscriptGrabberError):
    """Raised when operations timeout."""
    pass
