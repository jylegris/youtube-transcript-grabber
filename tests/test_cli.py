"""
Tests for CLI functionality.
"""

import json
import pytest
from unittest.mock import Mock, patch
from click.testing import CliRunner
from youtube_transcript_grabber.cli import main, format_transcript_text, format_transcript_json
from youtube_transcript_grabber.exceptions import (
    TranscriptNotFoundError,
    VideoNotFoundError,
    YouTubeTranscriptGrabberError,
)


class TestCLIFormatters:
    """Test formatting functions."""

    def test_format_transcript_text(self):
        """Test plain text formatting."""
        segments = [("0:00", "Hello world"), ("0:05", "This is a test")]
        result = format_transcript_text(segments)
        expected = "0:00 Hello world\n0:05 This is a test"
        assert result == expected

    def test_format_transcript_json(self):
        """Test JSON formatting."""
        segments = [("0:00", "Hello world"), ("0:05", "This is a test")]
        result = format_transcript_json(segments)
        expected_data = [
            {"timestamp": "0:00", "text": "Hello world"},
            {"timestamp": "0:05", "text": "This is a test"}
        ]
        assert json.loads(result) == expected_data

    def test_format_empty_segments(self):
        """Test formatting with empty segments."""
        segments = []
        assert format_transcript_text(segments) == ""
        assert json.loads(format_transcript_json(segments)) == []


class TestCLIMain:
    """Test main CLI function."""

    def test_video_id_extraction_from_full_url(self):
        """Test extracting video ID from full YouTube URL."""
        runner = CliRunner()
        
        with patch('youtube_transcript_grabber.cli.YouTubeTranscriptGrabber') as mock_grabber_class:
            mock_grabber = Mock()
            mock_grabber_class.return_value = mock_grabber
            mock_grabber.extract_transcript.return_value = [("0:00", "Test")]
            
            result = runner.invoke(main, [
                'https://www.youtube.com/watch?v=test123',
                '--verbose'
            ])
            
            assert result.exit_code == 0
            mock_grabber.extract_transcript.assert_called_once_with('test123')

    def test_video_id_extraction_from_short_url(self):
        """Test extracting video ID from short YouTube URL."""
        runner = CliRunner()
        
        with patch('youtube_transcript_grabber.cli.YouTubeTranscriptGrabber') as mock_grabber_class:
            mock_grabber = Mock()
            mock_grabber_class.return_value = mock_grabber
            mock_grabber.extract_transcript.return_value = [("0:00", "Test")]
            
            result = runner.invoke(main, ['https://youtu.be/test456'])
            
            assert result.exit_code == 0
            mock_grabber.extract_transcript.assert_called_once_with('test456')

    def test_plain_video_id(self):
        """Test using plain video ID."""
        runner = CliRunner()
        
        with patch('youtube_transcript_grabber.cli.YouTubeTranscriptGrabber') as mock_grabber_class:
            mock_grabber = Mock()
            mock_grabber_class.return_value = mock_grabber
            mock_grabber.extract_transcript.return_value = [("0:00", "Test")]
            
            result = runner.invoke(main, ['direct_video_id'])
            
            assert result.exit_code == 0
            mock_grabber.extract_transcript.assert_called_once_with('direct_video_id')

    def test_successful_extraction_text_format(self):
        """Test successful transcript extraction in text format."""
        runner = CliRunner()
        
        with patch('youtube_transcript_grabber.cli.YouTubeTranscriptGrabber') as mock_grabber_class:
            mock_grabber = Mock()
            mock_grabber_class.return_value = mock_grabber
            mock_grabber.extract_transcript.return_value = [
                ("0:00", "Hello"),
                ("0:05", "World")
            ]
            
            result = runner.invoke(main, ['test_video', '--format', 'text'])
            
            assert result.exit_code == 0
            assert "0:00 Hello" in result.output
            assert "0:05 World" in result.output

    def test_successful_extraction_json_format(self):
        """Test successful transcript extraction in JSON format."""
        runner = CliRunner()
        
        with patch('youtube_transcript_grabber.cli.YouTubeTranscriptGrabber') as mock_grabber_class:
            mock_grabber = Mock()
            mock_grabber_class.return_value = mock_grabber
            mock_grabber.extract_transcript.return_value = [("0:00", "Test")]
            
            result = runner.invoke(main, ['test_video', '--format', 'json'])
            
            assert result.exit_code == 0
            output_data = json.loads(result.output.strip())
            assert output_data == [{"timestamp": "0:00", "text": "Test"}]

    def test_successful_extraction_raw_format(self):
        """Test successful transcript extraction in raw format."""
        runner = CliRunner()
        
        with patch('youtube_transcript_grabber.cli.YouTubeTranscriptGrabber') as mock_grabber_class:
            mock_grabber = Mock()
            mock_grabber_class.return_value = mock_grabber
            mock_grabber.extract_transcript.return_value = [("0:00", "Test")]
            
            result = runner.invoke(main, ['test_video', '--format', 'raw'])
            
            assert result.exit_code == 0
            assert "[('0:00', 'Test')]" in result.output

    def test_output_to_file(self):
        """Test saving output to file."""
        runner = CliRunner()
        
        with patch('youtube_transcript_grabber.cli.YouTubeTranscriptGrabber') as mock_grabber_class:
            mock_grabber = Mock()
            mock_grabber_class.return_value = mock_grabber
            mock_grabber.extract_transcript.return_value = [("0:00", "Test")]
            
            with runner.isolated_filesystem():
                result = runner.invoke(main, [
                    'test_video',
                    '--output', 'transcript.txt'
                ])
                
                assert result.exit_code == 0
                
                with open('transcript.txt', 'r') as f:
                    content = f.read()
                    assert "0:00 Test" in content

    def test_verbose_output(self):
        """Test verbose output mode."""
        runner = CliRunner()
        
        with patch('youtube_transcript_grabber.cli.YouTubeTranscriptGrabber') as mock_grabber_class:
            mock_grabber = Mock()
            mock_grabber_class.return_value = mock_grabber
            mock_grabber.extract_transcript.return_value = [("0:00", "Test")]
            
            result = runner.invoke(main, [
                'test_video',
                '--verbose',
                '--browser', 'firefox',
                '--no-headless'
            ])
            
            assert result.exit_code == 0
            assert "Extracting transcript for video: test_video" in result.output
            assert "Format: text" in result.output
            assert "Browser: firefox (visible)" in result.output

    def test_browser_options(self):
        """Test different browser options."""
        runner = CliRunner()
        
        with patch('youtube_transcript_grabber.cli.YouTubeTranscriptGrabber') as mock_grabber_class:
            mock_grabber = Mock()
            mock_grabber_class.return_value = mock_grabber
            mock_grabber.extract_transcript.return_value = [("0:00", "Test")]
            
            result = runner.invoke(main, [
                'test_video',
                '--browser', 'webkit',
                '--timeout', '60000'
            ])
            
            assert result.exit_code == 0
            mock_grabber_class.assert_called_once_with(
                headless=True,
                browser_type='webkit',
                timeout=60000
            )

    def test_video_not_found_error(self):
        """Test handling of video not found error."""
        runner = CliRunner()
        
        with patch('youtube_transcript_grabber.cli.YouTubeTranscriptGrabber') as mock_grabber_class:
            mock_grabber = Mock()
            mock_grabber_class.return_value = mock_grabber
            mock_grabber.extract_transcript.side_effect = VideoNotFoundError("Video not found")
            
            result = runner.invoke(main, ['invalid_video'])
            
            assert result.exit_code == 1
            assert "Error: Video not found" in result.output

    def test_transcript_not_found_error(self):
        """Test handling of transcript not found error."""
        runner = CliRunner()
        
        with patch('youtube_transcript_grabber.cli.YouTubeTranscriptGrabber') as mock_grabber_class:
            mock_grabber = Mock()
            mock_grabber_class.return_value = mock_grabber
            mock_grabber.extract_transcript.side_effect = TranscriptNotFoundError("No transcript")
            
            result = runner.invoke(main, ['no_transcript_video'])
            
            assert result.exit_code == 1
            assert "Error: No transcript" in result.output

    def test_general_grabber_error(self):
        """Test handling of general grabber error."""
        runner = CliRunner()
        
        with patch('youtube_transcript_grabber.cli.YouTubeTranscriptGrabber') as mock_grabber_class:
            mock_grabber = Mock()
            mock_grabber_class.return_value = mock_grabber
            mock_grabber.extract_transcript.side_effect = YouTubeTranscriptGrabberError("General error")
            
            result = runner.invoke(main, ['error_video'])
            
            assert result.exit_code == 1
            assert "Error: General error" in result.output

    def test_keyboard_interrupt(self):
        """Test handling of keyboard interrupt."""
        runner = CliRunner()
        
        with patch('youtube_transcript_grabber.cli.YouTubeTranscriptGrabber') as mock_grabber_class:
            mock_grabber = Mock()
            mock_grabber_class.return_value = mock_grabber
            mock_grabber.extract_transcript.side_effect = KeyboardInterrupt()
            
            result = runner.invoke(main, ['test_video'])
            
            assert result.exit_code == 1
            assert "Operation cancelled by user" in result.output

    def test_unexpected_error(self):
        """Test handling of unexpected error."""
        runner = CliRunner()
        
        with patch('youtube_transcript_grabber.cli.YouTubeTranscriptGrabber') as mock_grabber_class:
            mock_grabber = Mock()
            mock_grabber_class.return_value = mock_grabber
            mock_grabber.extract_transcript.side_effect = RuntimeError("Unexpected error")
            
            result = runner.invoke(main, ['test_video'])
            
            assert result.exit_code == 1
            assert "Unexpected error: Unexpected error" in result.output

    def test_unexpected_error_with_verbose(self):
        """Test handling of unexpected error in verbose mode."""
        runner = CliRunner()
        
        with patch('youtube_transcript_grabber.cli.YouTubeTranscriptGrabber') as mock_grabber_class:
            mock_grabber = Mock()
            mock_grabber_class.return_value = mock_grabber
            mock_grabber.extract_transcript.side_effect = RuntimeError("Unexpected error")
            
            result = runner.invoke(main, ['test_video', '--verbose'])
            
            assert result.exit_code == 1
            assert "Unexpected error: Unexpected error" in result.output

    def test_empty_transcript_result(self):
        """Test handling of empty transcript result."""
        runner = CliRunner()
        
        with patch('youtube_transcript_grabber.cli.YouTubeTranscriptGrabber') as mock_grabber_class:
            mock_grabber = Mock()
            mock_grabber_class.return_value = mock_grabber
            mock_grabber.extract_transcript.return_value = []
            
            result = runner.invoke(main, ['test_video'])
            
            assert result.exit_code == 1
            assert "No transcript found for this video" in result.output

    def test_url_with_parameters(self):
        """Test URL with additional parameters."""
        runner = CliRunner()
        
        with patch('youtube_transcript_grabber.cli.YouTubeTranscriptGrabber') as mock_grabber_class:
            mock_grabber = Mock()
            mock_grabber_class.return_value = mock_grabber
            mock_grabber.extract_transcript.return_value = [("0:00", "Test")]
            
            result = runner.invoke(main, [
                'https://www.youtube.com/watch?v=test123&t=30s&list=playlist'
            ])
            
            assert result.exit_code == 0
            mock_grabber.extract_transcript.assert_called_once_with('test123')