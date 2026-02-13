
import asyncio
import os
from browser_use import Agent, Browser
from browser_use.llm import ChatGroq
# Patch ToolCallingModels to force tool usage instead of json_schema
from browser_use.llm.groq.chat import ToolCallingModels
ToolCallingModels.append('llama-3.3-70b-versatile')

from dotenv import load_dotenv

load_dotenv()

async def main():
    print("Starting functional test...")
    try:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            print("ERROR: GROQ_API_KEY not found")
            return

        print(f"Using API Key: {api_key[:5]}...")
        
        # Initialize LLM
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=api_key
        )
        
        # Initialize Browser
        # Add headless=True to mimic production (or False to see it)
        # Using default (usually False/visible for browser-use?)
        browser = Browser() 
        print("Browser initialized.")

        # Create Agent
        agent = Agent(
            task="Go to https://example.com and get the page title.",
            llm=llm,
            browser=browser
        )
        print("Agent initialized.")
        
        # Run Agent
        print("Running agent...")
        history = await agent.run()
        print("Agent run complete.")
        print(f"Result: {history}")

    except Exception as e:
        print(f"FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        if 'browser' in locals():
            print("Cleaning up browser...")
            try:
                await browser.stop()
                print("Browser stopped.")
            except Exception as e:
                print(f"Error stopping browser: {e}")

if __name__ == "__main__":
    asyncio.run(main())
