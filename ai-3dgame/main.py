
import streamlit as st
import asyncio
from config import Config
from ui_components import UIComponents
from llm_service import LLMService
from automation_service import AutomationService

# 1. Setup Page (Must be first)
UIComponents.setup_page()

# 2. Sidebar & API Keys
groq_api_key = UIComponents.sidebar()

# 3. Main Interface Structure
UIComponents.render_header()
query = UIComponents.render_query_input()
generate_code_btn, generate_vis_btn = UIComponents.render_action_buttons()

# 4. Session State Initialization
if "generated_code" not in st.session_state:
    st.session_state.generated_code = ""

# 5. Logic Handling
if generate_code_btn:
    if not query:
        st.warning("⚠️ Please describe your simulation first!")
    elif not groq_api_key:
        st.error("🔑 Please provide Groq API key in the sidebar.")
    else:
        try:
            with st.status("🤖 AI Agent Working...", expanded=True) as status:
                st.write("🧠 DeepSeek is thinking...")
                reasoning = LLMService.get_deepseek_reasoning(query, groq_api_key)
                st.write("📝 Designing PyGame logic...")
                
                with st.expander("Show Reasoning Trace"):
                    st.write(reasoning)
            
                st.write("💻 Writing clean Python code...")
                code = LLMService.extract_code_with_agno(reasoning, groq_api_key)
                st.session_state.generated_code = code
                status.update(label="✅ Code Generated Successfully!", state="complete", expanded=False)
            
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")

# Always display code if available with a nice editor
if st.session_state.generated_code:
    st.markdown("### 📜 Generated Python Code")
    st.code(st.session_state.generated_code, language="python", line_numbers=True)

if generate_vis_btn:
    if not st.session_state.generated_code:
        st.warning("⚠️ Please generate code first before visualizing.")
    elif not groq_api_key:
        st.error("🔑 Groq API key is required for automation.")
    else:
        status_container = st.container()
        with status_container:
            with st.status("🚀 Launching Autonomous Visualization...", expanded=True) as status:
                st.write("🌐 Initializing Browser Agent...")
                st.write(f"🔗 Navigating to {Config.TRINKET_URL}...")
                st.write("✍️ Writing code to editor...")
                st.write("▶️ Executing simulation...")
                
                try:
                    # Run the automation asynchronously
                    asyncio.run(AutomationService.run_pygame_on_trinket(st.session_state.generated_code, groq_api_key))
                    status.update(label="✅ Visualization Running on Trinket!", state="complete", expanded=False)
                    st.toast("Automation Completed Successfully!", icon="🎉")
                    st.success("Check the opened browser window to see your simulation!")
                    
                except Exception as e:
                    status.update(label="❌ Automation Failed", state="error")
                    st.error(f"Automation failed: {str(e)}")
