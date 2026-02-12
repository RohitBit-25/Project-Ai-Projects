
import streamlit as st
import asyncio
from config import Config
from ui_components import UIComponents
from llm_service import LLMService
from automation_service import AutomationService

# 1. Setup Page
UIComponents.setup_page()

# 2. Sidebar & API Keys
deepseek_api_key, openai_api_key = UIComponents.sidebar()

# 3. Main Interface
UIComponents.render_header()
query = UIComponents.render_query_input()
generate_code_btn, generate_vis_btn = UIComponents.render_action_buttons()

# 4. Session State Initialization
if "generated_code" not in st.session_state:
    st.session_state.generated_code = ""

# 5. Logic Handling
if generate_code_btn:
    if not query:
        st.warning("Please enter a description for your simulation.")
    elif not deepseek_api_key or not openai_api_key:
        st.error("Please provide both DeepSeek and OpenAI API keys in the sidebar.")
    else:
        try:
            with st.spinner("🤖 DeepSeek is thinking..."):
                reasoning = LLMService.get_deepseek_reasoning(query, deepseek_api_key)
                with st.expander("View DeepSeek's Reasoning"):
                    st.write(reasoning)
            
            with st.spinner("💻 Generating PyGame code..."):
                code = LLMService.extract_code_with_agno(reasoning, openai_api_key)
                st.session_state.generated_code = code
                
            st.success("Code generated successfully!")
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Always display code if available
if st.session_state.generated_code:
    with st.expander("View Generated Code", expanded=True):
        st.code(st.session_state.generated_code, language="python")

if generate_vis_btn:
    if not st.session_state.generated_code:
        st.warning("Please generate code first.")
    elif not openai_api_key:
        st.error("OpenAI API key is required for visualization automation.")
    else:
        with st.spinner("🚀 Launching automation on Trinket.io..."):
            try:
                # Run the automation asynchronously
                asyncio.run(AutomationService.run_pygame_on_trinket(st.session_state.generated_code, openai_api_key))
                st.success("Automation completed!")
            except Exception as e:
                st.error(f"Automation failed: {str(e)}")
