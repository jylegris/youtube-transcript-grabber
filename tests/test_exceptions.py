"""
Tests for exception classes.
"""

import pytest
from youtube_transcript_grabber.exceptions import (
    YouTubeTranscriptGrabberError,
    TranscriptNotFoundError,
    VideoNotFoundError,
    BrowserError,
    TimeoutError,
)


class TestExceptions:
    """Test custom exception classes."""

    def test_base_exception(self):
        """Test base YouTubeTranscriptGrabberError."""
        message = "Base error message"
        error = YouTubeTranscriptGrabberError(message)
        
        assert str(error) == message
        assert isinstance(error, Exception)

    def test_transcript_not_found_error(self):
        """Test TranscriptNotFoundError inheritance and functionality."""
        message = "Transcript not found"
        error = TranscriptNotFoundError(message)
        
        assert str(error) == message
        assert isinstance(error, YouTubeTranscriptGrabberError)
        assert isinstance(error, Exception)

    def test_video_not_found_error(self):
        """Test VideoNotFoundError inheritance and functionality."""
        message = "Video not found"
        error = VideoNotFoundError(message)
        
        assert str(error) == message
        assert isinstance(error, YouTubeTranscriptGrabberError)
        assert isinstance(error, Exception)

    def test_browser_error(self):
        """Test BrowserError inheritance and functionality."""
        message = "Browser error occurred"
        error = BrowserError(message)
        
        assert str(error) == message
        assert isinstance(error, YouTubeTranscriptGrabberError)
        assert isinstance(error, Exception)

    def test_timeout_error(self):
        """Test TimeoutError inheritance and functionality."""
        message = "Operation timed out"
        error = TimeoutError(message)
        
        assert str(error) == message
        assert isinstance(error, YouTubeTranscriptGrabberError)
        assert isinstance(error, Exception)

    def test_exception_with_no_message(self):
        """Test exceptions can be created without message."""
        error = YouTubeTranscriptGrabberError()
        assert str(error) == ""

    def test_exception_hierarchy(self):
        """Test that all exceptions inherit from base exception."""
        base_error = YouTubeTranscriptGrabberError("base")
        transcript_error = TranscriptNotFoundError("transcript")
        video_error = VideoNotFoundError("video")
        browser_error = BrowserError("browser")
        timeout_error = TimeoutError("timeout")

        # Test isinstance relationships
        assert isinstance(transcript_error, YouTubeTranscriptGrabberError)
        assert isinstance(video_error, YouTubeTranscriptGrabberError)
        assert isinstance(browser_error, YouTubeTranscriptGrabberError)
        assert isinstance(timeout_error, YouTubeTranscriptGrabberError)

        # Test they are all exceptions
        for error in [base_error, transcript_error, video_error, browser_error, timeout_error]:
            assert isinstance(error, Exception)

    def test_exception_raising(self):
        """Test that exceptions can be properly raised and caught."""
        
        # Test raising and catching specific exception
        with pytest.raises(TranscriptNotFoundError) as exc_info:
            raise TranscriptNotFoundError("Test transcript error")
        assert str(exc_info.value) == "Test transcript error"

        # Test catching by base class
        with pytest.raises(YouTubeTranscriptGrabberError):
            raise VideoNotFoundError("Test video error")

        # Test catching by Exception base class
        with pytest.raises(Exception):
            raise BrowserError("Test browser error")

    def test_exception_args(self):
        """Test exception arguments handling."""
        error = TranscriptNotFoundError("message", "extra_arg")
        assert error.args == ("message", "extra_arg")

    def test_exception_with_formatted_string(self):
        """Test exceptions with formatted string messages."""
        video_id = "test123"
        error = VideoNotFoundError(f"Video {video_id} not found")
        assert str(error) == "Video test123 not found"

    def test_exception_comparison(self):
        """Test that exceptions with same message compare as expected."""
        error1 = TranscriptNotFoundError("same message")
        error2 = TranscriptNotFoundError("same message")
        error3 = TranscriptNotFoundError("different message")
        
        # Same type and message should have same string representation
        assert str(error1) == str(error2)
        assert str(error1) != str(error3)

    def test_exception_repr(self):
        """Test exception representation."""
        error = VideoNotFoundError("test message")
        repr_str = repr(error)
        assert "VideoNotFoundError" in repr_str
        assert "test message" in repr_str