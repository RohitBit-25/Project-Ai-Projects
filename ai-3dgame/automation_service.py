
import asyncio
from browser_use import Browser, Agent
from langchain_openai import ChatOpenAI
from config import Config

class AutomationService:
    @staticmethod
    async def run_pygame_on_trinket(code: str, api_key: str):
        """
        Automates the process of running PyGame code on Trinket.io using Groq.
        """
        if not api_key:
            raise ValueError("API Key is missing for automation.")
            
        # Initialize browser
        browser = Browser()
        
        # Correct usage: browser itself acts as a manager, then create context
        async with await browser.new_context() as context:
            # Use Groq via LangChain's ChatOpenAI wrapper (Groq is OpenAI compatible)
            model = ChatOpenAI(
                base_url="https://api.groq.com/openai/v1",
                model="llama-3.3-70b-versatile", # Fast and capable model for tool use
                api_key=api_key
            )
            
            # Define agents for specific tasks
            navigator = Agent(
                task=f'Go to {Config.TRINKET_URL}, thats your only job.',
                llm=model,
                browser_context=context,
            )
            
            # We combine the "coder" and "executor" tasks to be more robust
            
            coder_with_payload = Agent(
                task=f'Coder. Clear the editor and paste ONLY this code:\n\n{code}\n\nThen stop.',
                llm=model,
                browser_context=context
            )
            
            executor = Agent(
                task='Executor. Your job is to click the "Run" or "Play" button to execute the code. Make sure the code is run.',
                llm=model,
                browser_context=context
            )

            viewer = Agent(
                task='Viewer. Your job is to just view the pygame window for 10 seconds to ensure it runs.',
                llm=model,
                browser_context=context,
            )

            # Execution flow
            await navigator.run()
            await coder_with_payload.run()
            await executor.run()
            await viewer.run()
