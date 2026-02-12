
import streamlit as st
from config import Config

class UIComponents:
    @staticmethod
    def setup_page():
        """
        Configures the Streamlit page and applies custom CSS.
        """
        st.set_page_config(
            page_title=Config.PAGE_TITLE, 
            page_icon=Config.PAGE_ICON, 
            layout=Config.LAYOUT
        )
        
        # Custom CSS for a premium look
        st.markdown("""
        <style>
        .stApp {
            background-color: #0e1117;
            color: #ffffff;
        }
        .stButton>button {
            width: 100%;
            border-radius: 8px;
            background-color: #ff4b4b;
            color: white;
            font-weight: 600;
            border: none;
            padding: 0.5rem 1rem;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #ff3333;
            box-shadow: 0 4px 12px rgba(255, 75, 75, 0.3);
            transform: translateY(-2px);
        }
        h1 {
            background: linear-gradient(45deg, #ff4b4b, #ff904b);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
        }
        .stTextInput>div>div>input {
            border-radius: 8px;
            border: 1px solid #2d2d2d;
            background-color: #1e1e1e;
            color: white;
        }
        .stTextArea>div>div>textarea {
            border-radius: 8px;
            border: 1px solid #2d2d2d;
            background-color: #1e1e1e;
            color: white;
        }
        </style>
        """, unsafe_allow_html=True)

    @staticmethod
    def sidebar():
        """
        Renders the sidebar for API key configuration.
        """
        with st.sidebar:
            st.title("Settings")
            
            # check if keys are present in config
            groq_status = "✅ Configured" if Config.API_KEYS["groq"] else "❌ Missing"
            
            st.markdown(f"**Groq API:** {groq_status}")
            
            if "Missing" in groq_status:
                st.warning("Please set your GROQ_API_KEY")
            
            st.markdown("---")
            st.info("""
            **How to use:**
            1. Select a real-world simulation or describe your own.
            2. Generate Code to see the Python script.
            3. Generate Visualization to run it on Trinket.
            """)
            
            return Config.API_KEYS["groq"]

    @staticmethod
    def render_header():
        """
        Renders the main header.
        """
        st.title(Config.PAGE_TITLE)
        st.markdown("### Create interactive 3D simulations with AI")

    @staticmethod
    def render_query_input():
        """
        Renders the query input area with presets.
        """
        presets = {
            "Custom": "",
            "Solar System": "Create a 3D solar system simulation with the Sun in the center and 8 planets orbiting at different speeds and distances. Use realistic colors for planets. Add a starfield background.",
            "Bouncing Particles": "Create a particle system where 100 colorful particles emit from the center, bounce off the window edges, and are affected by gravity. Add a trail effect to each particle.",
            "3D Cube Rotation": "Create a 3D rotating cube using PyGame. The cube should rotate on all three axes (X, Y, Z) controlled by mouse movement. Draw edges in white and faces with semi-transparent colors.",
            "Rain Simulation": "Create a realistic rain simulation. Raindrops should fall from the top, splash when they hit the bottom, and be affected by a wind force controlled by the left/right arrow keys.",
            "Conway's Game of Life": "Implement Conway's Game of Life grid. Allow the user to pause/resume with spacebar and clear the grid with 'C'. Allow drawing cells with the mouse.",
        }
        
        selected_preset = st.selectbox("Choose a Real-World Example:", list(presets.keys()))
        
        default_value = presets[selected_preset] if selected_preset != "Custom" else ""
        
        return st.text_area(
            "Describe your simulation:",
            height=150,
            value=default_value,
            placeholder=f"e.g.: {Config.EXAMPLE_QUERY}"
        )

    @staticmethod
    def render_action_buttons():
        """
        Renders the action buttons.
        """
        col1, col2 = st.columns(2)
        generate_code = col1.button("✨ Generate Code")
        generate_vis = col2.button("🚀 Generate Visualization")
        return generate_code, generate_vis
