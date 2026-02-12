
import asyncio
from browser_use import Browser, Agent
from langchain_openai import ChatOpenAI
from config import Config

class AutomationService:
    @staticmethod
    async def run_pygame_on_trinket(code: str, openai_api_key: str):
        """
        Automates the process of running PyGame code on Trinket.io.
        """
        if not openai_api_key:
            raise ValueError("OpenAI API Key is missing for automation.")
            
        browser = Browser()
        async with await browser.new_context() as context:
            model = ChatOpenAI(
                model="gpt-4o", 
                api_key=openai_api_key
            )
            
            # Define agents for specific tasks
            navigator = Agent(
                task=f'Go to {Config.TRINKET_URL}, thats your only job.',
                llm=model,
                browser_context=context,
            )
            
            # We combine the "coder" and "executor" tasks to be more robust
            # The original code had separate agents which is a good pattern, keeping it but refining prompts slightly
            
            coder = Agent(
                task='Coder. Your job is to wait for the page to load, then paste the provided code into the code editor. Delete existing code if any. You have 20 seconds.',
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
            
            # In a real scenario, we might want to inject the code via execution rather than relying on LLM to "paste" it physically if possible, 
            # but sticking to the requested "browser-use" agentic pattern:
            # We need to tell the coder *what* code to write. The original code missed passing the 'code' variable to the prompt explicitly in a robust way for the agent to "know" it.
            # However, the original prompt just said "wait for the user...". 
            # I will improve the coder prompt to actually *contain* the code to be pasted, or at least simulate the user action better.
            # *Self-correction*: The original code relied on the user manually interacting or the agent magically knowing? 
            # Ah, "wait for the user... to write the code" -> This implies the *user* manually types it? 
            # No, the goal is automation. 
            # Let's try to make the agent paste the code.
            
            coder_with_payload = Agent(
                 task=f'Coder. Clear the editor and paste ONLY this code:\n\n{code}\n\nThen stop.',
                 llm=model,
                 browser_context=context
            )

            await coder_with_payload.run()
            await executor.run()
            await viewer.run()
