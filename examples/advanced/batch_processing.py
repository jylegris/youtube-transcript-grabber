#!/usr/bin/env python3
"""
Batch processing example for YouTube Transcript Grabber.

This example shows how to process multiple videos efficiently with
progress tracking, error handling, and result aggregation.
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Optional

from youtube_transcript_grabber import YouTubeTranscriptGrabber


class BatchTranscriptProcessor:
    """Batch processor for YouTube transcripts."""
    
    def __init__(self, headless: bool = True, max_retries: int = 3):
        self.grabber = YouTubeTranscriptGrabber(headless=headless)
        self.max_retries = max_retries
        self.results: Dict[str, dict] = {}
    
    def process_videos(
        self, 
        video_ids: List[str], 
        output_dir: Optional[str] = None
    ) -> Dict[str, dict]:
        """
        Process multiple videos and return results.
        
        Args:
            video_ids: List of YouTube video IDs
            output_dir: Optional directory to save individual transcripts
            
        Returns:
            Dictionary with results for each video
        """
        if output_dir:
            output_path = Path(output_dir)
            output_path.mkdir(exist_ok=True)
        
        print(f"Processing {len(video_ids)} videos...")
        
        for i, video_id in enumerate(video_ids, 1):
            print(f"\n[{i}/{len(video_ids)}] Processing: {video_id}")
            
            result = self._process_single_video(video_id)
            self.results[video_id] = result
            
            # Save individual transcript if output directory specified
            if output_dir and result['success']:
                self._save_transcript(video_id, result['transcript'], output_path)
            
            # Progress indicator
            print(f"✅ Success" if result['success'] else f"❌ Failed: {result['error']}")
            
            # Small delay between requests to be respectful
            if i < len(video_ids):
                time.sleep(2)
        
        self._print_summary()
        return self.results
    
    def _process_single_video(self, video_id: str) -> dict:
        """Process a single video with retry logic."""
        for attempt in range(self.max_retries):
            try:
                transcript = self.grabber.extract_transcript(video_id)
                return {
                    'success': True,
                    'transcript': transcript,
                    'error': None,
                    'attempt': attempt + 1
                }
            except Exception as e:
                if attempt == self.max_retries - 1:
                    return {
                        'success': False,
                        'transcript': None,
                        'error': str(e),
                        'attempt': attempt + 1
                    }
                print(f"  Attempt {attempt + 1} failed: {e}")
                time.sleep(5)  # Wait before retry
        
        return {'success': False, 'transcript': None, 'error': 'Max retries exceeded'}
    
    def _save_transcript(self, video_id: str, transcript: List, output_path: Path):
        """Save transcript to file."""
        filename = f"{video_id}_transcript.txt"
        filepath = output_path / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            for timestamp, text in transcript:
                f.write(f"{timestamp} {text}\n")
    
    def _print_summary(self):
        """Print processing summary."""
        total = len(self.results)
        successful = sum(1 for r in self.results.values() if r['success'])
        failed = total - successful
        
        print(f"\n{'='*50}")
        print(f"BATCH PROCESSING SUMMARY")
        print(f"{'='*50}")
        print(f"Total videos: {total}")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")
        print(f"Success rate: {successful/total*100:.1f}%")
        
        if failed > 0:
            print(f"\nFailed videos:")
            for video_id, result in self.results.items():
                if not result['success']:
                    print(f"  {video_id}: {result['error']}")
    
    def save_results(self, filepath: str):
        """Save results to JSON file."""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        print(f"Results saved to: {filepath}")


def main():
    """Example usage of batch processor."""
    # List of video IDs to process
    video_ids = [
        "Iv-u8hwjHw4",  # Example video 1
        "dQw4w9WgXcQ",  # Example video 2
        "jNQXAC9IVRw",  # Example video 3
        # Add more video IDs here
    ]
    
    # Initialize processor
    processor = BatchTranscriptProcessor(headless=True, max_retries=2)
    
    # Process videos
    results = processor.process_videos(
        video_ids=video_ids,
        output_dir="transcripts"  # Save individual files here
    )
    
    # Save aggregated results
    processor.save_results("batch_results.json")
    
    # Example: Filter successful results
    successful_transcripts = {
        video_id: result['transcript'] 
        for video_id, result in results.items() 
        if result['success']
    }
    
    print(f"\nSuccessfully processed {len(successful_transcripts)} videos")


if __name__ == "__main__":
    main()