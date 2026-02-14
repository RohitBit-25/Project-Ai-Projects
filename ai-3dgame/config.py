
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    PAGE_TITLE = "AI 3D Visualizer with DeepSeek R1 (Groq)"
    PAGE_ICON = "🎮"
    LAYOUT = "wide"
    
    API_KEYS = {
        "groq": os.getenv("GROQ_API_KEY"),
    }
    
    MODEL_NAME = "llama-3.3-70b-versatile"
    
    EXAMPLE_QUERY = "Create a 3D simulation of a solar system using PyGame."
    
    SYSTEM_PROMPT = """You are an expert Python developer specializing in PyGame simulations.
    Your task is to generate clean, executable Python code for 3D simulations or games based on user queries.
    
    Rules:
    1. Use ONLY standard libraries and 'pygame', 'numpy', 'math'.
    2. Do NOT use external assets (images/sounds) unless generated procedurally.
    3. The code MUST include a main loop and handle QUIT events.
    4. Provide strictly the Python code, no markdown explanations outside the code block.
    5. Ensure the window size is 800x600.
    """
    
    EXTRACTION_PROMPT = """
    Extract the Python code from the following reasoning or text. 
    Return ONLY the Python code block without any markdown formatting or explanation.
    
    Content:
    {reasoning_content}
    """
    
    TRINKET_URL = "https://trinket.io/features/pygame"

    LOTTIE_URLS = {
        "thinking": "https://assets10.lottiefiles.com/packages/lf20_wbrwdn5r.json", # Neural network / tech thinking
        "coding": "https://assets9.lottiefiles.com/packages/lf20_M9p23l.json",     # Coding on laptop
        "running": "https://assets8.lottiefiles.com/packages/lf20_m64r7m.json",    # Rocket launch / execution
        "success": "https://assets1.lottiefiles.com/packages/lf20_pqnfmngr.json",   # Success check
        "error": "https://assets10.lottiefiles.com/packages/lf20_Q2cO7b.json"      # Error bot
    }
