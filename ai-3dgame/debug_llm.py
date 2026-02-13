
import browser_use.llm
print(dir(browser_use.llm))
try:
    from browser_use.llm import LangChainChatModel
    print("Found LangChainChatModel")
except ImportError:
    print("LangChainChatModel not found")
