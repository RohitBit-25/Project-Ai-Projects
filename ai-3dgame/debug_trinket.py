
import asyncio
from playwright.async_api import async_playwright

async def main():
    print("Starting inspection...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print("Navigating to Trinket...")
        await page.goto("https://trinket.io/features/pygame")
        
        # Wait for some load
        try:
            await page.wait_for_load_state("networkidle", timeout=10000)
        except:
            print("Network idle timeout, proceeding...")

        print(f"Page Title: {await page.title()}")
        
        # Check main page HTML for clues
        content = await page.content()
        if "ace_editor" in content:
            print("Found 'ace_editor' string in main page content")
        else:
            print("'ace_editor' NOT found in main page content")

        # Inspect frames
        print(f"Total Frames: {len(page.frames)}")
        for i, frame in enumerate(page.frames):
            print(f"Frame {i}: Name='{frame.name}', URL='{frame.url}'")
            try:
                # Try to find editor in this frame
                editor = await frame.query_selector(".ace_editor")
                if editor:
                    print(f"  >>> FOUND .ace_editor in Frame {i}!")
                    
                textarea = await frame.query_selector("textarea.ace_text-input")
                if textarea:
                    print(f"  >>> FOUND textarea.ace_text-input in Frame {i}!")
                    
            except Exception as e:
                print(f"  Error inspecting frame {i}: {e}")

        await browser.close()
    print("Inspection done.")

if __name__ == "__main__":
    asyncio.run(main())
