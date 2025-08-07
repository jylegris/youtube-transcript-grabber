from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.youtube.com/watch?v=Iv-u8hwjHw4")
    # Click the description expander
    page.click("#description-inline-expander")
    # wait  for 10 seconds
    print("Waiting for 10 seconds to ensure page loads completely...")
    page.wait_for_timeout(10000)
    page.get_by_role("button", name="Show transcript").click()
    
    # Wait for transcript to load
    print("Waiting for transcript to load...")
    page.wait_for_timeout(3000)
    
    # Extract transcript segments
    print("Extracting transcript segments...")
    segments = page.query_selector_all("ytd-transcript-segment-renderer")
    print(f"Found {len(segments)} transcript segments")
    
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
                transcript_data.append(f"{timestamp} {text}")
                
        except Exception as e:
            print(f"Error extracting segment {i}: {e}")
            continue
    
    # Print the extracted transcript
    print("\n" + "="*50)
    print("EXTRACTED TRANSCRIPT:")
    print("="*50)
    for line in transcript_data:
        print(line)
    print("="*50)
    print(f"Total segments extracted: {len(transcript_data)}")

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
