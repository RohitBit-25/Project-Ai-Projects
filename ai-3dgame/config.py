
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
    
    SYSTEM_PROMPT = """You are an elite Python developer specializing in high-performance PyGame simulations and 3D graphics.
    Your goal is to create visually stunning, interactive, and robust 3D simulations or games based on user queries.

    ### 🎨 Design & Aesthetics
    -   **Visuals**: Use vibrant colors, gradients, or neon aesthetics where appropriate. Avoid plain black/white defaults unless requested.
    -   **3D Illusion**: Since PyGame is 2D, use perspective projection math (x_proj = x * fov / (z + viewer_distance)) to create convincing 3D effects.
    -   **Smooth Animation**: Ensure strictly stable 60 FPS using `clock.tick(60)`. Use smooth variable updates.

    ### 🎮 Interactivity
    -   **Controls**: ALWAYS implement mouse or keyboard controls (e.g., arrow keys to rotate/move, mouse to interact).
    -   **Feedback**: responding to user inputs immediately visibly (e.g., color change on hover, rotation speedup).

    ### 🛠️ Technical Constraints
    1.  **Libraries**: Use ONLY `pygame`, `numpy`, `math`, `random`. NO external asset loading (images/sounds) unless generated procedurally (e.g., drawing shapes, surfaces).
    2.  **Structure**: logic MUST be encapsulated in a class (e.g., `class Simulation:`) with `__init__`, `update`, and `draw` methods.
    3.  **Robustness**: Handle edge cases (e.g., div by zero). The code MUST run indefinitely until closed.
    4.  **Window**: Initialize with `pygame.display.set_mode((800, 600))` or suitable resolution.
    5.  **Clean Code**: Write professional, commented, and typed Python code.

    ### 🚫 Restrictions
    -   NO `pygame.image.load()` (will fail on web runner). Use `pygame.draw` math for visuals.
    -   NO infinite loops without event handling.
    """
    
    EXTRACTION_PROMPT = """
    Extract the Python code from the given reasoning.
    Return ONLY the Python code block (inside ```python ... ```).
    Ensure the code is complete and self-contained.
    """
    
    TRINKET_URL = "https://trinket.io/features/pygame"

    # Use local assets for reliability
    
    LOTTIE_ASSETS = {
        "thinking": "assets/thinking.json",
        "coding": "assets/coding.json",
        "running": "assets/running.json",
        "success": "assets/success.json",
        "error": "assets/error.json"
    }
