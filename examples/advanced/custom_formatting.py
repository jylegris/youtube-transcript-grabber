#!/usr/bin/env python3
"""
Custom formatting example for YouTube Transcript Grabber.

This example demonstrates different ways to format and process
transcript data for various use cases.
"""

import json
import re
from typing import List, Tuple, Dict, Any

from youtube_transcript_grabber import YouTubeTranscriptGrabber


class TranscriptFormatter:
    """Custom transcript formatter with multiple output options."""
    
    def __init__(self):
        self.grabber = YouTubeTranscriptGrabber(headless=True)
    
    def get_transcript(self, video_id: str) -> List[Tuple[str, str]]:
        """Get raw transcript data."""
        return self.grabber.extract_transcript(video_id)
    
    def format_plain_text(self, transcript: List[Tuple[str, str]]) -> str:
        """Format as plain text without timestamps."""
        return " ".join([text for _, text in transcript])
    
    def format_timestamped_text(self, transcript: List[Tuple[str, str]]) -> str:
        """Format as timestamped text."""
        return "\n".join([f"[{timestamp}] {text}" for timestamp, text in transcript])
    
    def format_srt_subtitles(self, transcript: List[Tuple[str, str]]) -> str:
        """Format as SRT subtitle file."""
        srt_content = []
        
        for i, (timestamp, text) in enumerate(transcript, 1):
            # Convert timestamp to SRT format
            start_time = self._convert_timestamp_to_srt(timestamp)
            
            # Estimate end time (start of next segment or +3 seconds)
            if i < len(transcript):
                next_timestamp = transcript[i][0]
                end_time = self._convert_timestamp_to_srt(next_timestamp)
            else:
                # Add 3 seconds for the last segment
                end_time = self._add_seconds_to_srt_time(start_time, 3)
            
            srt_content.append(f"{i}")
            srt_content.append(f"{start_time} --> {end_time}")
            srt_content.append(text)
            srt_content.append("")  # Empty line between entries
        
        return "\n".join(srt_content)
    
    def format_json_detailed(self, transcript: List[Tuple[str, str]], video_id: str) -> str:
        """Format as detailed JSON with metadata."""
        data = {
            "video_id": video_id,
            "video_url": f"https://www.youtube.com/watch?v={video_id}",
            "transcript_count": len(transcript),
            "total_text_length": sum(len(text) for _, text in transcript),
            "segments": [
                {
                    "index": i,
                    "timestamp": timestamp,
                    "text": text,
                    "text_length": len(text),
                    "word_count": len(text.split())
                }
                for i, (timestamp, text) in enumerate(transcript)
            ]
        }
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    def format_word_frequency(self, transcript: List[Tuple[str, str]]) -> Dict[str, int]:
        """Analyze word frequency in the transcript."""
        # Combine all text
        all_text = " ".join([text.lower() for _, text in transcript])
        
        # Clean text and split into words
        words = re.findall(r'\b\w+\b', all_text)
        
        # Count frequency
        word_freq = {}
        for word in words:
            if len(word) > 2:  # Skip very short words
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Sort by frequency
        return dict(sorted(word_freq.items(), key=lambda x: x[1], reverse=True))
    
    def format_chapter_summary(self, transcript: List[Tuple[str, str]], 
                             chapter_length: int = 10) -> List[Dict[str, Any]]:
        """Break transcript into chapters/segments."""
        chapters = []
        
        for i in range(0, len(transcript), chapter_length):
            chapter_segments = transcript[i:i + chapter_length]
            
            start_time = chapter_segments[0][0]
            end_time = chapter_segments[-1][0] if len(chapter_segments) > 1 else start_time
            
            chapter_text = " ".join([text for _, text in chapter_segments])
            
            chapters.append({
                "chapter": i // chapter_length + 1,
                "start_time": start_time,
                "end_time": end_time,
                "segment_count": len(chapter_segments),
                "text": chapter_text[:200] + "..." if len(chapter_text) > 200 else chapter_text,
                "full_text": chapter_text
            })
        
        return chapters
    
    def _convert_timestamp_to_srt(self, timestamp: str) -> str:
        """Convert timestamp format to SRT format."""
        # Handle different timestamp formats
        if ":" in timestamp:
            parts = timestamp.split(":")
            if len(parts) == 2:  # MM:SS
                minutes, seconds = parts
                return f"00:{minutes.zfill(2)}:{seconds.zfill(2)},000"
            elif len(parts) == 3:  # HH:MM:SS
                hours, minutes, seconds = parts
                return f"{hours.zfill(2)}:{minutes.zfill(2)}:{seconds.zfill(2)},000"
        
        # Fallback for numeric timestamps
        return "00:00:00,000"
    
    def _add_seconds_to_srt_time(self, srt_time: str, seconds: int) -> str:
        """Add seconds to SRT time format."""
        # Simple implementation - just add 3 seconds
        parts = srt_time.split(":")
        if len(parts) == 3:
            sec_part = parts[2].split(",")[0]
            new_seconds = int(sec_part) + seconds
            if new_seconds >= 60:
                new_seconds -= 60
                minutes = int(parts[1]) + 1
                if minutes >= 60:
                    minutes -= 60
                    hours = int(parts[0]) + 1
                    return f"{hours:02d}:{minutes:02d}:{new_seconds:02d},000"
                return f"{parts[0]}:{minutes:02d}:{new_seconds:02d},000"
            return f"{parts[0]}:{parts[1]}:{new_seconds:02d},000"
        return srt_time


def main():
    """Example usage of custom formatting."""
    video_id = "Iv-u8hwjHw4"  # Replace with actual video ID
    formatter = TranscriptFormatter()
    
    print(f"Processing video: {video_id}")
    
    try:
        # Get transcript
        transcript = formatter.get_transcript(video_id)
        print(f"✅ Successfully extracted {len(transcript)} segments")
        
        # Demonstrate different formats
        print("\n" + "="*60)
        print("1. PLAIN TEXT (first 200 chars)")
        print("="*60)
        plain_text = formatter.format_plain_text(transcript)
        print(plain_text[:200] + "...")
        
        print("\n" + "="*60)
        print("2. TIMESTAMPED TEXT (first 3 segments)")
        print("="*60)
        timestamped = formatter.format_timestamped_text(transcript[:3])
        print(timestamped)
        
        print("\n" + "="*60)
        print("3. SRT SUBTITLES (first 3 segments)")
        print("="*60)
        srt_format = formatter.format_srt_subtitles(transcript[:3])
        print(srt_format)
        
        print("\n" + "="*60)
        print("4. WORD FREQUENCY (top 10)")
        print("="*60)
        word_freq = formatter.format_word_frequency(transcript)
        for word, count in list(word_freq.items())[:10]:
            print(f"{word}: {count}")
        
        print("\n" + "="*60)
        print("5. CHAPTER SUMMARY")
        print("="*60)
        chapters = formatter.format_chapter_summary(transcript, chapter_length=5)
        for chapter in chapters[:3]:  # Show first 3 chapters
            print(f"Chapter {chapter['chapter']}: {chapter['start_time']} - {chapter['end_time']}")
            print(f"  {chapter['text']}")
            print()
        
        # Save different formats to files
        print("💾 Saving formatted outputs...")
        
        with open(f"{video_id}_plain.txt", "w", encoding="utf-8") as f:
            f.write(plain_text)
        
        with open(f"{video_id}_timestamped.txt", "w", encoding="utf-8") as f:
            f.write(formatter.format_timestamped_text(transcript))
        
        with open(f"{video_id}_subtitles.srt", "w", encoding="utf-8") as f:
            f.write(formatter.format_srt_subtitles(transcript))
        
        with open(f"{video_id}_detailed.json", "w", encoding="utf-8") as f:
            f.write(formatter.format_json_detailed(transcript, video_id))
        
        print("✅ All formats saved successfully!")
        
    except Exception as e:
        print(f"❌ Error processing video: {e}")


if __name__ == "__main__":
    main()