# 🎮 AI 3D PyGame Visualizer with DeepSeek R1

### 🎓 FREE Step-by-Step Tutorial 
**👉 [Click here to follow our complete step-by-step tutorial](https://www.theunwindai.com/p/build-an-ai-3d-pygame-visualizer-with-deepseek-r1) and learn how to build this from scratch with detailed code walkthroughs, explanations, and best practices.**

This Project demonstrates R1's code capabilities with a PyGame code generator and visualizer with browser use. The system uses DeepSeek for reasoning, OpenAI for code extraction, and browser automation agents to visualize the code on Trinket.io.

### Features

- Generates PyGame code from natural language descriptions
- Uses DeepSeek Reasoner for code logic and explanation
- Extracts clean code using OpenAI GPT-4o
## 📂 Project Structure

The project is now modularized for better maintainability:

- **`main.py`**: The entry point of the application.
- **`config.py`**: Configuration settings and API key management.
- **`llm_service.py`**: Handles interactions with DeepSeek and OpenAI.
- **`automation_service.py`**: Manages browser automation for Trinket.io.
- **`ui_components.py`**: Custom UI components and styling.
- **`requirements.txt`**: List of dependencies.
- **`.env`**: Environment variables for API keys.

---

## 🚀 How to Run

1.  **Clone the Repository** (if you haven't already):
    ```bash
    git clone https://github.com/Shubhamsaboo/awesome-llm-apps.git
    cd advanced_ai_agents/autonomous_game_playing_agent_apps/ai_3dpygame_r1
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set Up API Keys**:
    Create a `.env` file in the project directory and add your keys:
    ```env
    DEEPSEEK_API_KEY=your_deepseek_key
    OPENAI_API_KEY=your_openai_key
    ```

4.  **Run the Application**:
    ```bash
    streamlit run main.py
    ```

5. Browser use automatically opens your web browser and navigate to the URL provided in the console output to interact with the PyGame generator.

### How it works?

1. **Query Processing:** User enters a natural language description of the desired PyGame visualization.
2. **Code Generation:** 
   - DeepSeek Reasoner analyzes the query and provides detailed reasoning with code
   - OpenAI agent extracts clean, executable code from the reasoning
3. **Visualization:**
   - Browser agents automate the process of running code on Trinket.io
   - Multiple specialized agents handle different tasks:
     - Navigation to Trinket.io
     - Code input
     - Execution
     - Visualization viewing
4. **User Interface:** Streamlit provides an intuitive interface for entering queries, viewing code, and managing the visualization process.
