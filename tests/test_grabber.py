"""
Tests for YouTubeTranscriptGrabber class.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from youtube_transcript_grabber.grabber import YouTubeTranscriptGrabber
from youtube_transcript_grabber.exceptions import (
    TranscriptNotFoundError,
    VideoNotFoundError,
    BrowserError,
)


class TestYouTubeTranscriptGrabber:
    """Test cases for YouTubeTranscriptGrabber."""

    def test_init_default_params(self):
        """Test initialization with default parameters."""
        grabber = YouTubeTranscriptGrabber()
        assert grabber.headless is True
        assert grabber.browser_type == "chromium"
        assert grabber.timeout == 30000
        assert grabber.slow_mo == 100

    def test_init_custom_params(self):
        """Test initialization with custom parameters."""
        grabber = YouTubeTranscriptGrabber(
            headless=False,
            browser_type="firefox",
            timeout=60000,
            slow_mo=200
        )
        assert grabber.headless is False
        assert grabber.browser_type == "firefox"
        assert grabber.timeout == 60000
        assert grabber.slow_mo == 200

    @patch('youtube_transcript_grabber.grabber.sync_playwright')
    def test_extract_transcript_success(self, mock_playwright):
        """Test successful transcript extraction."""
        # Mock playwright components
        mock_p = Mock()
        mock_browser = Mock()
        mock_context = Mock()
        mock_page = Mock()
        
        mock_playwright.return_value.__enter__.return_value = mock_p
        mock_p.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page
        
        # Mock page interactions
        mock_page.goto.return_value = None
        mock_page.wait_for_load_state.return_value = None
        mock_page.wait_for_selector.return_value = Mock()
        mock_page.click.return_value = None
        mock_page.get_by_role.return_value.wait_for.return_value = None
        mock_page.get_by_role.return_value.click.return_value = None
        mock_page.wait_for_timeout.return_value = None
        
        # Mock transcript segments
        mock_segment1 = Mock()
        mock_segment1.query_selector.side_effect = [
            Mock(inner_text=Mock(return_value="0:00")),  # timestamp
            Mock(inner_text=Mock(return_value="Hello world"))  # text
        ]
        
        mock_segment2 = Mock()
        mock_segment2.query_selector.side_effect = [
            Mock(inner_text=Mock(return_value="0:05")),  # timestamp
            Mock(inner_text=Mock(return_value="This is a test"))  # text
        ]
        
        mock_page.query_selector_all.return_value = [mock_segment1, mock_segment2]
        
        grabber = YouTubeTranscriptGrabber()
        result = grabber.extract_transcript("test_video_id")
        
        assert result == [("0:00", "Hello world"), ("0:05", "This is a test")]
        mock_page.goto.assert_called_once_with(
            "https://www.youtube.com/watch?v=test_video_id", 
            timeout=30000
        )

    @patch('youtube_transcript_grabber.grabber.sync_playwright')
    def test_extract_transcript_video_not_found(self, mock_playwright):
        """Test video not found error."""
        mock_p = Mock()
        mock_browser = Mock()
        mock_context = Mock()
        mock_page = Mock()
        
        mock_playwright.return_value.__enter__.return_value = mock_p
        mock_p.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page
        
        # Mock page interactions
        mock_page.goto.return_value = None
        mock_page.wait_for_load_state.return_value = None
        mock_page.wait_for_selector.side_effect = Exception("Not found")
        
        grabber = YouTubeTranscriptGrabber()
        
        with pytest.raises(VideoNotFoundError):
            grabber.extract_transcript("invalid_video_id")

    @patch('youtube_transcript_grabber.grabber.sync_playwright')
    def test_extract_transcript_no_transcript_button(self, mock_playwright):
        """Test transcript not found error when button doesn't exist."""
        mock_p = Mock()
        mock_browser = Mock()
        mock_context = Mock()
        mock_page = Mock()
        
        mock_playwright.return_value.__enter__.return_value = mock_p
        mock_p.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page
        
        # Mock successful navigation but no transcript button
        mock_page.goto.return_value = None
        mock_page.wait_for_load_state.return_value = None
        mock_page.wait_for_selector.return_value = Mock()  # Video exists
        mock_page.click.return_value = None  # Description expand works
        mock_page.get_by_role.return_value.wait_for.side_effect = Exception("No button")
        
        grabber = YouTubeTranscriptGrabber()
        
        with pytest.raises(TranscriptNotFoundError):
            grabber.extract_transcript("no_transcript_video")

    @patch('youtube_transcript_grabber.grabber.sync_playwright')
    def test_extract_transcript_no_segments(self, mock_playwright):
        """Test transcript not found when no segments are found."""
        mock_p = Mock()
        mock_browser = Mock()
        mock_context = Mock()
        mock_page = Mock()
        
        mock_playwright.return_value.__enter__.return_value = mock_p
        mock_p.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page
        
        # Mock successful navigation and button click but no segments
        mock_page.goto.return_value = None
        mock_page.wait_for_load_state.return_value = None
        mock_page.wait_for_selector.return_value = Mock()
        mock_page.click.return_value = None
        mock_page.get_by_role.return_value.wait_for.return_value = None
        mock_page.get_by_role.return_value.click.return_value = None
        mock_page.query_selector_all.return_value = []  # No segments
        
        grabber = YouTubeTranscriptGrabber()
        
        with pytest.raises(TranscriptNotFoundError):
            grabber.extract_transcript("no_segments_video")

    @patch('youtube_transcript_grabber.grabber.sync_playwright')
    def test_extract_transcript_browser_error(self, mock_playwright):
        """Test browser error handling."""
        mock_playwright.side_effect = Exception("Browser launch failed")
        
        grabber = YouTubeTranscriptGrabber()
        
        with pytest.raises(BrowserError):
            grabber.extract_transcript("test_video")

    @patch('youtube_transcript_grabber.grabber.sync_playwright')
    def test_extract_multiple_videos(self, mock_playwright):
        """Test extracting from multiple videos."""
        grabber = YouTubeTranscriptGrabber()
        
        # Mock the extract_transcript method to return consistent results
        with patch.object(grabber, 'extract_transcript') as mock_extract:
            mock_extract.return_value = [("0:00", "Test content")]
            
            result = grabber.extract_multiple(["video1", "video2"])
            
            assert "video1" in result
            assert "video2" in result
            assert result["video1"] == [("0:00", "Test content")]
            assert result["video2"] == [("0:00", "Test content")]
            
            # Verify extract_transcript was called for both videos
            assert mock_extract.call_count == 2

    @patch('youtube_transcript_grabber.grabber.sync_playwright')
    def test_extract_multiple_videos_with_failures(self, mock_playwright):
        """Test extracting from multiple videos with some failures."""
        grabber = YouTubeTranscriptGrabber()
        
        # Mock the extract_transcript method to simulate mixed results
        with patch.object(grabber, 'extract_transcript') as mock_extract:
            mock_extract.side_effect = [
                [("0:00", "Success")],  # First video succeeds
                Exception("Failed"),    # Second video fails
            ]
            
            result = grabber.extract_multiple(["video1", "video2"])
            
            assert result["video1"] == [("0:00", "Success")]
            assert result["video2"] == []

    def test_different_browser_types(self):
        """Test initialization with different browser types."""
        for browser_type in ["chromium", "firefox", "webkit"]:
            grabber = YouTubeTranscriptGrabber(browser_type=browser_type)
            assert grabber.browser_type == browser_type