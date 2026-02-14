# 🎮 AI 3D Game Maker
### Powered by DeepSeek R1 & Playwright Automation

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![DeepSeek](https://img.shields.io/badge/AI-DeepSeek_R1-purple)
![Playwright](https://img.shields.io/badge/Automation-Playwright-green)

## 📖 Overview

The **AI 3D Game Maker** is an advanced autonomous agent that transforms natural language descriptions into 3D simulations and games. It leverages **DeepSeek R1** for complex reasoning and code generation, and uses **Playwright** to automatically execute and visualize the generated code on [Trinket.io](https://trinket.io/features/pygame).

Whether you want to create a solar system simulation, a 3D chess board, or a cyberpunk car drift scene, just describe it, and the AI will build and run it for you.

## ✨ Key Features

-   **🧠 DeepSeek R1 Integration**: Utilizes state-of-the-art reasoning models to generate logic, accurate Python/PyGame code.
-   **🤖 Autonomous Visualization**: Automatically navigates to an online compiler (Trinket.io), injects the code, and runs the simulation without human intervention.
-   **🎨 Cyberpunk UI**: Features a premium "Cyberpunk/Neon" aesthetic with glassmorphism, Lottie animations, and dynamic status updates.
-   **⚡ Real-time Feedback**: Visual status indicators keep you informed of the AI's reasoning, coding, and execution phases.
-   **🛠️ Robust Automation**: Intelligent iframe detection ensures reliable interaction with embedded code editors.

## 🛠️ Tech Stack

-   **Frontend**: Streamlit (with custom CSS & Lottie Animations)
-   **AI Core**: DeepSeek R1 (via Groq API)
-   **Automation**: Playwright (Async API)
-   **Language**: Python 3.11+
-   **Environment Management**: `python-dotenv`

## 🚀 Installation & Setup

Follow these steps to get the project running on your local machine.

### Prerequisites
-   Python 3.11 or higher installed.
-   A [Groq API Key](https://console.groq.com/keys) for accessing DeepSeek models.

### 1. Clone the Repository
```bash
git clone https://github.com/RohitBit-25/Project-Ai-Projects.git
cd Project-Ai-Projects/ai-3dgame
```

### 2. Install Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```

### 3. Install Playwright Browsers
The automation requires browser binaries to work:
```bash
playwright install
```

### 4. Configuration
Create a `.env` file in the root directory (optional, or enter keys in the UI):
```env
GROQ_API_KEY=your_groq_api_key_here
```

## 🎮 Usage Guide

1.  **Run the Application**:
    ```bash
    streamlit run main.py
    ```

2.  **Configure API**:
    -   Open the sidebar ("Control Center").
    -   Enter your **Groq API Key** if not set in `.env`.

3.  **Generate a Game**:
    -   **Select a Preset**: Choose from examples like "Indian Flag Weaving" or "Spiral Galaxy".
    -   **Or Describe Your Own**: Type a detailed description of the simulation you want.
    -   Click **✨ Generate Logic (Code)**.

4.  **Maximize & Visualize**:
    -   Review the generated code and reasoning trace.
    -   Click **🔴 LIVE Visualization**.
    -   Watch as the browser agent automates the execution on Trinket.io!

## 📂 Project Structure

```
ai-3dgame/
├── main.py                 # Application Entry Point & Logic
├── ui_components.py        # UI Rendering, CSS, & Animations
├── automation_service.py   # Playwright Automation Logic
├── llm_service.py          # AI Model Interaction (DeepSeek/Groq)
├── config.py               # Configuration & Constants
├── requirements.txt        # Python Dependencies
└── README.md               # Project Documentation
```

## 🤝 Contributing

Contributions are welcome! If you have ideas for new features, game templates, or UI improvements:
1.  Fork the repository.
2.  Create a feature branch (`git checkout -b feature/NewFeature`).
3.  Commit your changes.
4.  Push to the branch and open a Pull Request.

## 📄 License

This project is licensed under the MIT License.

---
**Made with ❤️ by RohitBit-25**
