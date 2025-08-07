"""
Main YouTube transcript grabber implementation using Playwright.
"""

import json
import time
from typing import Dict, List, Optional, Tuple
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page

from .exceptions import (
    TranscriptNotFoundError,
    VideoNotFoundError, 
    BrowserError,
    TimeoutError,
)


class YouTubeTranscriptGrabber:
    """
    A robust YouTube transcript extractor using Playwright browser automation.
    
    This class navigates YouTube's web interface to extract transcripts with
    timestamps, mimicking human user interactions to avoid detection.
    """
    
    def __init__(
        self,
        headless: bool = True,
        browser_type: str = "chromium",
        timeout: int = 30000,
        slow_mo: int = 100,
    ):
        """
        Initialize the YouTube Transcript Grabber.
        
        Args:
            headless: Run browser in headless mode (default: True)
            browser_type: Browser to use ('chromium', 'firefox', 'webkit')
            timeout: Timeout in milliseconds for operations
            slow_mo: Delay in milliseconds between actions
        """
        self.headless = headless
        self.browser_type = browser_type
        self.timeout = timeout
        self.slow_mo = slow_mo
        
    def extract_transcript(
        self, 
        video_id: str
    ) -> List[Tuple[str, str]]:
        """
        Extract transcript from a YouTube video.
        
        Args:
            video_id: YouTube video ID (e.g., "uuyiUxsyywM")
            
        Returns:
            List of (timestamp, text) tuples
            
        Raises:
            VideoNotFoundError: If video is not accessible
            TranscriptNotFoundError: If no transcript is available
            BrowserError: If browser automation fails
        """
        url = f"https://www.youtube.com/watch?v={video_id}"
        
        try:
            with sync_playwright() as p:
                # Launch browser
                browser_launcher = getattr(p, self.browser_type)
                browser = browser_launcher.launch(
                    headless=self.headless,
                    slow_mo=self.slow_mo
                )
                
                context = browser.new_context()
                page = context.new_page()
                
                try:
                    # Navigate to video
                    print(f"Navigating to: {url}")
                    page.goto(url, timeout=self.timeout)
                    
                    # Wait for page to load completely
                    page.wait_for_load_state("networkidle", timeout=self.timeout)
                    
                    # Check if video exists (look for title)
                    try:
                        title = page.wait_for_selector(
                            'h1.style-scope.ytd-watch-metadata',
                            timeout=5000
                        )
                        if not title:
                            raise VideoNotFoundError(f"Video {video_id} not found")
                    except:
                        raise VideoNotFoundError(f"Video {video_id} not accessible")
                    
                    # Click description expander to reveal transcript option
                    print("Expanding description...")
                    try:
                        page.click("#description-inline-expander", timeout=5000)
                        # Wait for description to expand (no fixed delay needed)
                    except:
                        print("Description expander not found, continuing...")
                    
                    # Wait for transcript button to be available
                    try:
                        page.wait_for_selector("button:has-text('Show transcript')", timeout=15000)
                    except:
                        # Fallback: wait a bit longer for slower loading
                        page.wait_for_timeout(3000)
                    
                    # Click "Show transcript" button
                    print("Looking for transcript button...")
                    try:
                        transcript_button = page.get_by_role("button", name="Show transcript")
                        transcript_button.wait_for(timeout=10000)
                        transcript_button.click()
                        print("Successfully clicked transcript button")
                    except:
                        raise TranscriptNotFoundError(
                            f"No transcript available for video {video_id}"
                        )
                    
                    # Wait for transcript to load
                    print("Waiting for transcript to load...")
                    page.wait_for_selector("ytd-transcript-segment-renderer", timeout=10000)
                    
                    # Extract transcript segments
                    print("Extracting transcript segments...")
                    segments = page.query_selector_all("ytd-transcript-segment-renderer")
                    
                    if not segments:
                        raise TranscriptNotFoundError(
                            f"No transcript segments found for video {video_id}"
                        )
                    
                    print(f"Found {len(segments)} transcript segments")
                    
                    # Parse segments
                    transcript_data = []
                    for i, segment in enumerate(segments):
                        try:
                            # Get timestamp
                            timestamp_elem = segment.query_selector(".segment-timestamp")
                            timestamp = timestamp_elem.inner_text().strip() if timestamp_elem else f"[{i}]"
                            
                            # Get text content  
                            text_elem = segment.query_selector(".segment-text")
                            text = text_elem.inner_text().strip() if text_elem else ""
                            
                            if text:  # Only add if we have text content
                                transcript_data.append((timestamp, text))
                                
                        except Exception as e:
                            print(f"Error extracting segment {i}: {e}")
                            continue
                    
                    if not transcript_data:
                        raise TranscriptNotFoundError(
                            f"No transcript content extracted for video {video_id}"
                        )
                    
                    print(f"Successfully extracted {len(transcript_data)} transcript segments")
                    
                    return transcript_data
                    
                finally:
                    browser.close()
                    
        except (TranscriptNotFoundError, VideoNotFoundError):
            raise
        except Exception as e:
            raise BrowserError(f"Browser automation failed: {e}")
    

    
    def extract_multiple(
        self, 
        video_ids: List[str]
    ) -> Dict[str, List[Tuple[str, str]]]:
        """
        Extract transcripts from multiple videos.
        
        Args:
            video_ids: List of YouTube video IDs
            
        Returns:
            Dictionary mapping video IDs to their transcript tuples
        """
        results = {}
        for video_id in video_ids:
            try:
                transcript = self.extract_transcript(video_id)
                results[video_id] = transcript
            except Exception as e:
                print(f"Failed to extract transcript for {video_id}: {e}")
                results[video_id] = []
                
        return results
