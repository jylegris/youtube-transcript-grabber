"""
Pytest configuration and fixtures for YouTube Transcript Grabber tests.
"""

import pytest
from unittest.mock import Mock


@pytest.fixture
def mock_transcript_segments():
    """Fixture providing mock transcript segments."""
    return [
        ("0:00", "Welcome to this video"),
        ("0:05", "Today we will learn about"),
        ("0:10", "YouTube transcript extraction"),
        ("0:15", "This is a comprehensive guide"),
    ]


@pytest.fixture
def mock_playwright_page():
    """Fixture providing a mock Playwright page object."""
    mock_page = Mock()
    
    # Set up default mock behaviors
    mock_page.goto.return_value = None
    mock_page.wait_for_load_state.return_value = None
    mock_page.click.return_value = None
    mock_page.wait_for_timeout.return_value = None
    
    # Mock successful video title detection
    mock_page.wait_for_selector.return_value = Mock()
    
    # Mock successful transcript button
    mock_page.get_by_role.return_value = Mock()
    mock_page.get_by_role.return_value.wait_for.return_value = None
    mock_page.get_by_role.return_value.click.return_value = None
    
    return mock_page


@pytest.fixture
def mock_playwright_browser(mock_playwright_page):
    """Fixture providing a mock Playwright browser setup."""
    mock_browser = Mock()
    mock_context = Mock()
    
    mock_browser.new_context.return_value = mock_context
    mock_context.new_page.return_value = mock_playwright_page
    mock_browser.close.return_value = None
    
    return mock_browser


@pytest.fixture
def mock_playwright_setup(mock_playwright_browser):
    """Fixture providing complete Playwright mock setup."""
    mock_p = Mock()
    mock_p.chromium.launch.return_value = mock_playwright_browser
    mock_p.firefox.launch.return_value = mock_playwright_browser
    mock_p.webkit.launch.return_value = mock_playwright_browser
    
    return mock_p


@pytest.fixture
def sample_video_id():
    """Fixture providing a sample video ID for testing."""
    return "dQw4w9WgXcQ"


@pytest.fixture
def sample_youtube_urls():
    """Fixture providing sample YouTube URLs for testing."""
    return {
        "full": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "full_with_params": "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=30s&list=PLtest",
        "short": "https://youtu.be/dQw4w9WgXcQ",
        "short_with_params": "https://youtu.be/dQw4w9WgXcQ?t=30s",
    }


@pytest.fixture
def mock_segment_elements(mock_transcript_segments):
    """Fixture providing mock DOM elements for transcript segments."""
    elements = []
    
    for timestamp, text in mock_transcript_segments:
        mock_element = Mock()
        
        # Mock timestamp element
        mock_timestamp_elem = Mock()
        mock_timestamp_elem.inner_text.return_value = timestamp
        
        # Mock text element  
        mock_text_elem = Mock()
        mock_text_elem.inner_text.return_value = text
        
        # Configure query_selector to return appropriate elements
        def mock_query_selector(selector):
            if "timestamp" in selector:
                return mock_timestamp_elem
            elif "text" in selector:
                return mock_text_elem
            return None
            
        mock_element.query_selector.side_effect = mock_query_selector
        elements.append(mock_element)
    
    return elements


@pytest.fixture(autouse=True)
def disable_playwright_install():
    """Automatically disable actual Playwright installations during tests."""
    import os
    os.environ["PYTEST_RUNNING"] = "1"
    yield
    if "PYTEST_RUNNING" in os.environ:
        del os.environ["PYTEST_RUNNING"]