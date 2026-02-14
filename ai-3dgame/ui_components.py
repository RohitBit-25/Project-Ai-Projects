import streamlit as st
import requests
from streamlit_lottie import st_lottie
from config import Config

class UIComponents:
    @staticmethod
    def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    @staticmethod
    def render_status_animation(key: str, height: int = 200):
        url = Config.LOTTIE_URLS.get(key)
        if url:
            lottie_json = UIComponents.load_lottieurl(url)
            if lottie_json:
                st_lottie(lottie_json, height=height, key=f"lottie_{key}")
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
        
        # Custom CSS for Cyberpunk / Neon Theme
        st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&family=Rajdhani:wght@300;500;700&display=swap');

        /* Main Background - Cyberpunk Void */
        .stApp {
            background-color: #050505;
            background-image: 
                linear-gradient(rgba(0, 255, 255, 0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 255, 255, 0.03) 1px, transparent 1px);
            background-size: 30px 30px;
            color: #d1d5db;
            font-family: 'Rajdhani', sans-serif;
        }

        /* Sidebar - Tech Panel */
        section[data-testid="stSidebar"] {
            background-color: #0a0a0a;
            border-right: 1px solid #333;
        }

        /* Input Fields - Neon Glass */
        .stTextArea, .stTextInput, .stSelectbox {
             background: rgba(10, 10, 10, 0.8);
             border-radius: 4px;
             border: 1px solid #333;
             color: #00ffcc;
             font-family: 'Orbitron', sans-serif;
        }
        .stTextArea:focus-within, .stTextInput:focus-within {
            border-color: #00ffcc;
            box-shadow: 0 0 10px rgba(0, 255, 204, 0.2);
        }

        /* Typography */
        h1, h2, h3 {
            font-family: 'Orbitron', sans-serif !important;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        h1 {
            background: linear-gradient(90deg, #00f2ff, #00ff9d);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 20px rgba(0, 242, 255, 0.5);
            font-weight: 900;
        }

        /* Buttons - Holographic */
        .stButton>button {
            width: 100%;
            border-radius: 0px;
            background: transparent;
            color: #00ffcc;
            border: 1px solid #00ffcc;
            font-family: 'Orbitron', sans-serif;
            font-weight: 600;
            padding: 0.75rem 1.5rem;
            transition: all 0.3s ease;
            text-transform: uppercase;
            position: relative;
            overflow: hidden;
        }
        .stButton>button:hover {
            background: rgba(0, 255, 204, 0.1);
            box-shadow: 0 0 15px rgba(0, 255, 204, 0.4);
            transform: translateY(-2px);
            text-shadow: 0 0 8px #00ffcc;
        }

        /* Custom Classes */
        .neon-card {
            background: rgba(15, 15, 20, 0.6);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(0, 255, 204, 0.1);
            border-left: 2px solid #00ffcc;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
        }
        
        .status-box {
            border: 1px solid #ff00ff;
            background: rgba(255, 0, 255, 0.05);
            padding: 10px;
            border-radius: 4px;
        }
        </style>
        """, unsafe_allow_html=True)

    @staticmethod
    def sidebar():
        """
        Renders the sidebar for API key configuration.
        """
        with st.sidebar:
            st.image("https://media.giphy.com/media/l41lFj8afad4T1pDy/giphy.gif", width=300) # Tech vibe GIF
            st.title("⚙️ Control Center")
            
            st.markdown("### 🔑 API Config")
            # check if keys are present in config
            groq_key = Config.API_KEYS["groq"]
            
            if not groq_key:
                st.warning("⚠️ Groq API Key Missing!")
                groq_key = st.text_input("Enter Groq API Key", type="password")
            else:
                st.success("✅ Groq Connected")
            
            st.markdown("---")
            st.markdown("""
            ### 📜 How it works
            1. **Select** a preset or **Describe** your idea.
            2. **Generate Code** (powered by DeepSeek R1).
            3. **Visualize** (automated on Trinket.io).
            """)
            
            st.markdown("---")
            st.caption("Made with ❤️ in India by **RohitBit-25**")
            
            return groq_key

    @staticmethod
    def render_header():
        """
        Renders the main header.
        """
        st.markdown('<div class="neon-card">', unsafe_allow_html=True)
        st.title(Config.PAGE_TITLE)
        st.markdown("### 🚀 Build 3D Games & Simulations with **DeepSeek R1**")
        st.markdown('</div>', unsafe_allow_html=True)

    @staticmethod
    def render_query_input():
        """
        Renders the query input area with presets.
        """
        presets = {
            "Custom": "",
            "🇮🇳 Indian Flag Weaving": "Create a 3D simulation of a waving Indian Flag using particle systems or mesh grid.",
            "🌌 Spiral Galaxy": "Create a 3D galaxy simulation with thousands of stars rotating in a spiral arm pattern, with a supermassive black hole in the center.",
            "🏎️ Cyberpunk Car Drift": "Create a low-poly cyberpunk car drifting on a neon grid road. Add retro-wave aesthetic colors.",
            "⚽ Bouncing Football": "Create a realistic physics simulation of a football bouncing on a grass field with gravity and elasticity coefficient.",
            "♟️ 3D Chess Board": "Draw a 3D Chess board with black and white squares. Allow rotation of the board using arrow keys.",
        }
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("#### 🎯 Quick Start")
            selected_preset = st.selectbox("Select a Template:", list(presets.keys()))
        
        with col2:
            st.markdown("#### ✍️ Your Vision")
            default_value = presets[selected_preset] if selected_preset != "Custom" else ""
            query = st.text_area(
                "Describe your dream simulation:",
                height=150,
                value=default_value,
                placeholder=f"e.g.: {Config.EXAMPLE_QUERY}"
            )
        
        return query

    @staticmethod
    def render_action_buttons():
        """
        Renders the action buttons.
        """
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            generate_code = st.button("✨ Generate Logic (Code)")
        with col2:
            generate_vis = st.button("🔴 LIVE Visualization")
        with col3:
             if st.button("🔄 Reset"):
                 st.rerun()
                 
        return generate_code, generate_vis
