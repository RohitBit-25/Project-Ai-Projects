
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    PAGE_TITLE = "AI 3D Visualizer with DeepSeek R1"
    PAGE_ICON = "🎮"
    LAYOUT = "wide"
    
    API_KEYS = {
        "deepseek": os.getenv("DEEPSEEK_API_KEY", ""),
        "openai": os.getenv("OPENAI_API_KEY", "")
    }
    
    EXAMPLE_QUERY = "Create a particle system simulation where 100 particles emit from the mouse position and respond to keyboard-controlled wind forces"
    
    SYSTEM_PROMPT = """You are a Pygame and Python Expert that specializes in making games and visualisation through pygame and python programming. 
    During your reasoning and thinking, include clear, concise, and well-formatted Python code in your reasoning. 
    Always include explanations for the code you provide."""
    
    EXTRACTION_PROMPT = """Extract ONLY the Python code from the following content which is reasoning of a particular query to make a pygame script. 
    Return nothing but the raw code without any explanations, or markdown backticks:
    {reasoning_content}"""

    TRINKET_URL = "https://trinket.io/features/pygame"
