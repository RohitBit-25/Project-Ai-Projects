
import asyncio
from browser_use import Browser, Agent
# Use ChatGroq from browser_use to ensure compatibility
from browser_use.llm import ChatGroq
from config import Config

class AutomationService:
    @staticmethod
    async def run_pygame_on_trinket(code: str, api_key: str):
        """
        Automates the process of running PyGame code on Trinket.io using Groq.
        """
        if not api_key:
            raise ValueError("API Key is missing for automation.")
            
        # Initialize browser (BrowserSession)
        browser = Browser()
        
        try:
            # Use ChatGroq wrapper which is compatible with browser-use Agent
            model = ChatGroq(
                model="llama-3.3-70b-versatile",
                api_key=api_key
            )
            
            # Define agents for specific tasks
            # Note: We pass 'browser' directly as it is a BrowserSession
            
            navigator = Agent(
                task=f'Go to {Config.TRINKET_URL}, thats your only job.',
                llm=model,
                browser=browser,
            )
            
            coder_with_payload = Agent(
                task=f'Coder. Clear the editor and paste ONLY this code:\n\n{code}\n\nThen stop.',
                llm=model,
                browser=browser
            )
            
            executor = Agent(
                task='Executor. Your job is to click the "Run" or "Play" button to execute the code. Make sure the code is run.',
                llm=model,
                browser=browser
            )

            viewer = Agent(
                task='Viewer. Your job is to just view the pygame window for 10 seconds to ensure it runs.',
                llm=model,
                browser=browser,
            )

            # Execution flow
            await navigator.run()
            await coder_with_payload.run()
            await executor.run()
            await viewer.run()
            
        finally:
            # clean up browser
            # clean up browser
            await browser.stop()
