
import asyncio
from playwright.async_api import async_playwright
from config import Config

class AutomationService:
    @staticmethod
    async def run_pygame_on_trinket(code: str, api_key: str):
        """
        Automates the process of running PyGame code on Trinket.io using direct Playwright.
        This provides a much more stable and faster execution than using an LLM agent.
        """
        async with async_playwright() as p:
            # Launch browser (headless=False so user can see it)
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()
            
            try:
                # 1. Navigate to Trinket
                await page.goto(Config.TRINKET_URL)
                await page.wait_for_load_state("networkidle")
                
                # 2. Wait for editor to be ready
                # Trinket uses Ace editor, so we target the text area or the container
                # We might need to wait for a specific element that significantly indicates the editor is loaded
                await page.wait_for_selector(".ace_content")
                
                # 3. Focus the editor
                await page.click(".ace_content")
                
                # 4. Select All and Delete
                # Mac uses Meta+A, others use Control+A
                modifier = "Meta" if await page.evaluate("navigator.platform.includes('Mac')") else "Control"
                await page.keyboard.press(f"{modifier}+A")
                await page.keyboard.press("Backspace")
                
                # 5. Paste the code
                # Direct typing can be slow for large code, so we use clipboard or evaluate
                # But typing is safer for diverse environments. Let's try direct fill first if possible, 
                # or just type it fast.
                
                # Using invalidation of clipboard permissions by default in many browsers, 
                # we will simulate typing but very fast
                await page.keyboard.insert_text(code)
                
                # 6. Click Run
                # The run button usually has a specific class or title. 
                # In Trinket Pygame, it's often a play icon.
                # We look for a button that contains "Run" or has a play icon class.
                await page.click("button.run-button")  # Common selector, needs verification if fails
                # Fallback if specific class isn't found, try finding by text or icon
                
                # 7. Wait and Watch
                # Keep the browser open for 15 seconds to let the user see the result
                await asyncio.sleep(15)
                
            except Exception as e:
                print(f"Automation Error: {e}")
                raise e
            finally:
                await browser.close()
