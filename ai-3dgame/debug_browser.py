
import asyncio
from browser_use import Browser

async def main():
    browser = Browser()
    print(f"Browser Object: {browser}")
    print(f"Dir Browser: {dir(browser)}")
    try:
        async with await browser.new_context() as context:
            print("Context created successfully via await new_context()")
    except Exception as e:
        print(f"Failed await new_context(): {e}")
        
    try:
        async with browser.new_context() as context:
             print("Context created successfully via normal new_context()")
    except Exception as e:
        print(f"Failed normal new_context(): {e}")

if __name__ == "__main__":
    asyncio.run(main())
