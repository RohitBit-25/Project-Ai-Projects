
import asyncio
import os
from browser_use import Agent, Browser
from browser_use.llm import ChatGroq
from dotenv import load_dotenv

load_dotenv()

async def main():
    try:
        # Use ChatGroq from browser_use
        # It likely needs API key from env or arg
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            print("GROQ_API_KEY not found")
            return

        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=api_key
        )
        
        browser = Browser()
        print("Browser initialized")
        
        # Instantiate Agent directly
        agent = Agent(
            task="test", 
            llm=llm, 
            browser=browser 
        )
        print("Agent initialized successfully with browser_use.llm.ChatGroq")
        
    except Exception as e:
        print(f"Failed: {e}")
    finally:
        if 'browser' in locals():
             await browser.close() # trying close instead of close_page

if __name__ == "__main__":
    asyncio.run(main())
