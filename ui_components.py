
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
            st.title("API Configuration")
            
            deepseek_key = st.text_input(
                "DeepSeek API Key",
                type="password",
                value=Config.API_KEYS["deepseek"] or ""
            )
            openai_key = st.text_input(
                "OpenAI API Key",
                type="password",
                value=Config.API_KEYS["openai"] or ""
            )
            
            st.markdown("---")
            st.info("""
            **How to use:**
            1. Enter your API keys.
            2. Describe your simulation.
            3. Generate Code to see the Python script.
            4. Generate Visualization to run it on Trinket.
            """)
            
            return deepseek_key, openai_key

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
        Renders the query input area.
        """
        return st.text_area(
            "Describe your simulation:",
            height=100,
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
