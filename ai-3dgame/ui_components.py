
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
        
        # Custom CSS for a premium, glassmorphism look
        st.markdown("""
        <style>
        /* Main Background */
        .stApp {
            background: radial-gradient(circle at 10% 20%, rgb(0, 0, 0) 0%, rgb(30, 30, 30) 90.2%);
            color: #ffffff;
            font-family: 'Inter', sans-serif;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: rgba(20, 20, 20, 0.95);
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }

        /* Glassmorphism Containers */
        .stTextArea, .stTextInput, .stSelectbox {
             background: rgba(255, 255, 255, 0.05);
             backdrop-filter: blur(10px);
             border-radius: 12px;
             border: 1px solid rgba(255, 255, 255, 0.1);
             padding: 10px;
        }

        /* Typography */
        h1 {
            background: linear-gradient(90deg, #FF9933, #FFFFFF, #138808); /* Tiranga Gradient */
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            font-size: 3rem !important;
            text-shadow: 0 0 20px rgba(255, 153, 51, 0.3);
        }
        h3 {
            color: #ccc;
            font-weight: 300;
        }

        /* Buttons */
        .stButton>button {
            width: 100%;
            border-radius: 12px;
            background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
            color: white;
            font-weight: 600;
            border: none;
            padding: 0.75rem 1.5rem;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .stButton>button:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 20px rgba(37, 117, 252, 0.4);
        }

        /* Input Fields */
        .stTextInput>div>div>input, .stTextArea>div>div>textarea {
            color: white;
            background-color: transparent;
        }
        
        /* Custom Classes */
        .glass-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            margin-bottom: 20px;
        }
        </style>
        """, unsafe_allow_html=True)

    @staticmethod
    def sidebar():
        """
        Renders the sidebar for API key configuration.
        """
        with st.sidebar:
            st.image("https://media.giphy.com/media/l41lFj8afad4T1pDy/giphy.gif", use_container_width=True) # Tech vibe GIF
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
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
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
