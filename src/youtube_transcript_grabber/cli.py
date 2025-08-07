"""
Command-line interface for YouTube Transcript Grabber.
"""

import json
import sys
from pathlib import Path
from typing import List, Optional, Tuple

import click

from .grabber import YouTubeTranscriptGrabber
from .exceptions import (
    YouTubeTranscriptGrabberError,
    TranscriptNotFoundError,
    VideoNotFoundError,
)


def format_transcript_text(segments: List[Tuple[str, str]]) -> str:
    """Format transcript segments as plain text."""
    return "\n".join([f"{timestamp} {text}" for timestamp, text in segments])


def format_transcript_json(segments: List[Tuple[str, str]]) -> str:
    """Format transcript segments as JSON."""
    data = [{"timestamp": timestamp, "text": text} for timestamp, text in segments]
    return json.dumps(data, indent=2)


@click.command()
@click.argument("video_id")
@click.option(
    "--output", "-o",
    type=click.Path(),
    help="Output file path (default: print to stdout)"
)
@click.option(
    "--format", "-f",
    type=click.Choice(["text", "json", "raw"]),
    default="text",
    help="Output format (default: text)"
)
@click.option(
    "--headless/--no-headless",
    default=True,
    help="Run browser in headless mode (default: True)"
)
@click.option(
    "--browser",
    type=click.Choice(["chromium", "firefox", "webkit"]),
    default="chromium",
    help="Browser to use (default: chromium)"
)
@click.option(
    "--timeout",
    type=int,
    default=30000,
    help="Timeout in milliseconds (default: 30000)"
)
@click.option(
    "--verbose", "-v",
    is_flag=True,
    help="Enable verbose output"
)
@click.version_option()
def main(
    video_id: str,
    output: Optional[str],
    format: str,
    headless: bool,
    browser: str,
    timeout: int,
    verbose: bool,
) -> None:
    """
    Extract transcript from a YouTube video.
    
    VIDEO_ID can be either a full YouTube URL or just the video ID.
    
    Examples:
    
        youtube-transcript-grabber Iv-u8hwjHw4
        
        youtube-transcript-grabber https://www.youtube.com/watch?v=Iv-u8hwjHw4
        
        youtube-transcript-grabber Iv-u8hwjHw4 --output transcript.txt
        
        youtube-transcript-grabber Iv-u8hwjHw4 --format json --output transcript.json
    """
    # Extract video ID from URL if needed
    if "youtube.com/watch?v=" in video_id:
        video_id = video_id.split("v=")[1].split("&")[0]
    elif "youtu.be/" in video_id:
        video_id = video_id.split("youtu.be/")[1].split("?")[0]
    
    if verbose:
        click.echo(f"Extracting transcript for video: {video_id}")
        click.echo(f"Format: {format}")
        click.echo(f"Browser: {browser} ({'headless' if headless else 'visible'})")
    
    try:
        # Initialize grabber
        grabber = YouTubeTranscriptGrabber(
            headless=headless,
            browser_type=browser,
            timeout=timeout,
        )
        
        # Extract transcript
        if verbose:
            click.echo("Starting extraction...")
            
        segments = grabber.extract_transcript(video_id)
        
        if not segments:
            click.echo("No transcript found for this video.", err=True)
            sys.exit(1)
        
        # Format output
        if format == "json":
            formatted_output = format_transcript_json(segments)
        elif format == "raw":
            formatted_output = repr(segments)
        else:  # text format
            formatted_output = format_transcript_text(segments)
        
        # Output result
        if output:
            output_path = Path(output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(formatted_output)
                
            if verbose:
                click.echo(f"Transcript saved to: {output_path}")
        else:
            click.echo(formatted_output)
            
    except VideoNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except TranscriptNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except YouTubeTranscriptGrabberError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except KeyboardInterrupt:
        click.echo("\nOperation cancelled by user.", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)





if __name__ == "__main__":
    main()
