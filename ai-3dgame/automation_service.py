
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
                
                # 2. Locate the iframe containing the editor
                # Trinket embeds the editor in an iframe
                # We wait for the iframe to be attached
                iframe_element = await page.wait_for_selector("iframe[src*='trinket.io/embed']", state="attached")
                iframe = await iframe_element.content_frame()
                
                if not iframe:
                    raise Exception("Could not find the Trinket editor iframe")

                # 3. Wait for editor inside iframe
                await iframe.wait_for_selector(".ace_content")
                
                # 4. Focus the editor (click inside textarea or editor div)
                await iframe.click(".ace_content")
                
                # 5. Select All and Delete
                modifier = "Meta" if await page.evaluate("navigator.platform.includes('Mac')") else "Control"
                await page.keyboard.press(f"{modifier}+A")
                await page.keyboard.press("Backspace")
                
                # 6. Paste the code
                # We use the clipboard method which is faster and cleaner for large code blocks
                # or just type it if clipboard is restricted. 
                # typing is safer.
                await page.keyboard.insert_text(code)
                
                # 7. Click Run
                # The run button is also inside the iframe usually for the embed view
                # It has a class 'run-button' or ID 'run-button'
                try:
                    await iframe.click(".run-button", timeout=3000)
                except:
                    # Fallback: try finding a button with play icon class
                    await iframe.click("img[src*='play']") # speculative fallback, main one should work

                # 8. Wait and Watch
                # Keep the browser open for 15 seconds to let the user see the result
                await asyncio.sleep(15)
                
            except Exception as e:
                print(f"Automation Error: {e}")
                raise e
            finally:
                await browser.close()
