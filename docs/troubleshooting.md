# Troubleshooting Guide

Common issues and solutions for YouTube Transcript Grabber.

## Installation Issues

### Browser Not Installed

**Error:** `playwright._impl._api_types.Error: Executable doesn't exist`

**Solution:**
```bash
playwright install chromium
# or for all browsers
playwright install
```

### Permission Denied

**Error:** Permission errors when installing or running

**Solution:**
```bash
# Install in user directory
pip install --user youtube-transcript-grabber

# Or use virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install youtube-transcript-grabber
```

## Runtime Issues

### No Transcript Found

**Error:** `TranscriptNotFoundError: No transcript available for video`

**Possible Causes & Solutions:**

1. **Video doesn't have transcripts**
   - Check if transcripts are available manually on YouTube
   - Try with a different video that you know has transcripts

2. **Transcript button not visible**
   - Some videos hide transcripts in different UI elements
   - Try running with `headless=False` to see what's happening

3. **YouTube layout changed**
   - The selectors might be outdated
   - Report this as a bug with the video ID

**Debugging steps:**
```python
# Run with visible browser to see what's happening
grabber = YouTubeTranscriptGrabber(headless=False, slow_mo=1000)
transcript = grabber.extract_transcript("your_video_id")
```

### Video Not Found

**Error:** `VideoNotFoundError: Video not found or accessible`

**Possible Causes & Solutions:**

1. **Invalid video ID**
   - Check that the video ID is correct (11 characters)
   - Extract from full URL: `https://www.youtube.com/watch?v=VIDEO_ID`

2. **Private or deleted video**
   - Video might be private, unlisted, or deleted
   - Try with a public video

3. **Geographic restrictions**
   - Video might not be available in your region
   - Try with a VPN or different video

### Browser Timeout

**Error:** `TimeoutError` or operations hanging

**Solutions:**

1. **Increase timeout:**
   ```python
   grabber = YouTubeTranscriptGrabber(timeout=60000)  # 60 seconds
   ```

2. **Check internet connection:**
   ```bash
   ping youtube.com
   ```

3. **Reduce concurrent operations:**
   - Don't run multiple grabbers simultaneously
   - Add delays between requests

### Browser Crashes

**Error:** Browser process crashes or fails to start

**Solutions:**

1. **Update Playwright:**
   ```bash
   pip install --upgrade playwright
   playwright install
   ```

2. **Try different browser:**
   ```python
   grabber = YouTubeTranscriptGrabber(browser_type="firefox")
   ```

3. **Check system resources:**
   - Ensure enough RAM and disk space
   - Close other applications

## Performance Issues

### Slow Extraction

**Problem:** Extraction takes too long

**Solutions:**

1. **Optimize settings:**
   ```python
   grabber = YouTubeTranscriptGrabber(
       headless=True,        # Faster than visible browser
       slow_mo=50,          # Reduce delay between actions
       timeout=20000        # Shorter timeout
   )
   ```

2. **Use batch processing efficiently:**
   ```python
   # Add delays between requests
   import time
   for video_id in video_ids:
       transcript = grabber.extract_transcript(video_id)
       time.sleep(2)  # Be respectful to YouTube
   ```

### High Memory Usage

**Problem:** High memory consumption

**Solutions:**

1. **Process videos one at a time:**
   ```python
   # Don't keep all transcripts in memory
   for video_id in video_ids:
       transcript = grabber.extract_transcript(video_id)
       process_and_save(transcript)  # Process immediately
       del transcript  # Free memory
   ```

2. **Use context managers:**
   ```python
   # Browser cleanup is automatic, but you can be explicit
   with YouTubeTranscriptGrabber() as grabber:
       transcript = grabber.extract_transcript(video_id)
   ```

## Network Issues

### Connection Timeouts

**Error:** Network timeouts or connection refused

**Solutions:**

1. **Check network connectivity:**
   ```bash
   curl -I https://youtube.com
   ```

2. **Configure proxy if needed:**
   ```python
   # Playwright supports proxy configuration
   # See Playwright documentation for proxy setup
   ```

3. **Retry logic:**
   ```python
   import time
   
   def extract_with_retry(grabber, video_id, max_retries=3):
       for attempt in range(max_retries):
           try:
               return grabber.extract_transcript(video_id)
           except Exception as e:
               if attempt == max_retries - 1:
                   raise
               print(f"Attempt {attempt + 1} failed: {e}")
               time.sleep(5)  # Wait before retry
   ```

### Rate Limiting

**Problem:** YouTube blocking or limiting requests

**Solutions:**

1. **Add delays between requests:**
   ```python
   import time
   import random
   
   for video_id in video_ids:
       transcript = grabber.extract_transcript(video_id)
       # Random delay between 2-5 seconds
       time.sleep(random.uniform(2, 5))
   ```

2. **Use different user agents:**
   ```python
   # This would require customizing the browser context
   # Currently not directly supported, but can be added
   ```

## YouTube-Specific Issues

### Layout Changes

**Problem:** YouTube updates their layout

**What to do:**
1. Update to the latest version of the package
2. Report the issue on GitHub with:
   - Video ID that fails
   - Error message
   - Screenshots if possible

### Region Restrictions

**Problem:** Content not available in your region

**Solutions:**
1. Try with videos that are globally available
2. Use a VPN to change your apparent location
3. Test with different types of content (educational, music, etc.)

### Language Issues

**Problem:** Transcripts in unexpected languages

**Note:** The grabber extracts whatever transcript is available. YouTube might provide:
- Auto-generated transcripts in the video's language
- User-submitted transcripts in various languages
- Multiple transcript tracks

Currently, the grabber takes the first available transcript.

## Debugging Tips

### Enable Verbose Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Or use the CLI verbose flag
# youtube-transcript-grabber video_id --verbose
```

### Visual Debugging

```python
# Run with visible browser and slow motion
grabber = YouTubeTranscriptGrabber(
    headless=False,
    slow_mo=2000,  # 2 second delays
    timeout=60000
)
```

### Save Screenshots

```python
# Add this to the grabber code for debugging
page.screenshot(path="debug_screenshot.png")
```

## Getting Help

If you're still experiencing issues:

1. **Check the [Issues](https://github.com/yourusername/youtube-transcript-grabber/issues)** for similar problems
2. **Create a new issue** with:
   - Python version
   - Operating system
   - Error message (full traceback)
   - Video ID that fails
   - Steps to reproduce
3. **Include debug information:**
   ```bash
   python --version
   pip list | grep -E "(playwright|youtube-transcript-grabber)"
   ```

## Common Error Patterns

### Pattern 1: Selector Not Found
```
Error: waiting for selector "button:has-text('Show transcript')" failed
```
**Cause:** YouTube UI changed or transcript button has different text
**Solution:** Update package or report issue

### Pattern 2: Navigation Failed
```
Error: page.goto: net::ERR_NAME_NOT_RESOLVED
```
**Cause:** Network connectivity issue
**Solution:** Check internet connection and DNS

### Pattern 3: Context Closed
```
Error: Target page, context or browser has been closed
```
**Cause:** Browser crashed or was closed unexpectedly
**Solution:** Restart and check system resources