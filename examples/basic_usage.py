#!/usr/bin/env python3
"""
Example script showing how to use YouTube Transcript Grabber programmatically.
"""

from youtube_transcript_grabber import YouTubeTranscriptGrabber
from youtube_transcript_grabber.exceptions import TranscriptNotFoundError, VideoNotFoundError

def main():
    # Initialize the grabber
    grabber = YouTubeTranscriptGrabber(
        headless=True,          # Run in background
        browser_type="chromium", # Or "firefox", "webkit"
        timeout=30000,          # 30 second timeout
    )
    
    # Example 1: Basic transcript extraction
    print("=== Example 1: Basic Usage ===")
    try:
        video_id = "Iv-u8hwjHw4"  # Example video
        transcript = grabber.extract_transcript(video_id, format="text")
        
        if transcript:
            lines = transcript.split('\n')
            print(f"✅ Successfully extracted {len(lines)} lines")
            print("First 5 lines:")
            for line in lines[:5]:
                print(f"  {line}")
            print("...")
        
    except VideoNotFoundError:
        print("❌ Video not found or not accessible")
    except TranscriptNotFoundError:
        print("❌ No transcript available for this video")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Example 2: JSON format output
    print("\n=== Example 2: JSON Format ===")
    try:
        transcript_json = grabber.extract_transcript(video_id, format="json")
        print(f"✅ JSON transcript (first 200 chars):")
        print(transcript_json[:200] + "...")
        
    except Exception as e:
        print(f"❌ Error: {e}")

    # Example 3: Raw data format
    print("\n=== Example 3: Raw Data ===")
    try:
        transcript_raw = grabber.extract_transcript(video_id, format="raw")
        if transcript_raw:
            print(f"✅ Raw data: {len(transcript_raw)} segments")
            print("First segment:", transcript_raw[0])
            
    except Exception as e:
        print(f"❌ Error: {e}")

    # Example 4: Multiple videos
    print("\n=== Example 4: Multiple Videos ===")
    video_ids = ["Iv-u8hwjHw4", "dQw4w9WgXcQ"]  # Second one might not work
    results = grabber.extract_multiple(video_ids, format="text")
    
    for vid_id, transcript in results.items():
        if transcript:
            lines = transcript.split('\n')
            print(f"✅ {vid_id}: {len(lines)} lines extracted")
        else:
            print(f"❌ {vid_id}: Failed to extract")

    print("\n🎉 Done!")

if __name__ == "__main__":
    main() 