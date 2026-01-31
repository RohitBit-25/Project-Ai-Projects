# Smart Camera Classifier using OpenCV

A real-time custom object classifier that uses your webcam to learn and recognize objects on the fly. Built with Python, Tkinter, and OpenCV.

## Features
- **Real-Time Detection**: Uses OpenCV's K-Nearest Neighbors (KNN) for fast and efficient recognition.
- **Systematic Workflow**: Clearly separated phases for Gathering Data, Training, and Predicting.
- **Dynamic Classes**: Add as many new object classes as you want during runtime.
- **Visual Feedback**:
    - **Green Viewfinder**: Focuses detection on the object of interest.
    - **Status Indicators**: Shows how many samples you've collected and confirms when the model is trained.
- **Optimized Performance**: Throttled prediction loop to ensure smooth video playback.

## Prerequisites
- Python 3.x
- Webcam

## Installation

1.  **Clone/Download** this repository.
2.  **Navigate** to the project folder:
    ```bash
    cd "Camera-Classifier"
    ```
3.  **Set up the Environment**:
    It is recommended to use a virtual environment to handle dependencies (especially for Tkinter on macOS).
    ```bash
    # Create virtual environment (using Homebrew python if on macOS arm64)
    /opt/homebrew/bin/python3 -m venv venv
    
    # Activate it
    source venv/bin/activate
    
    # Install dependencies
    pip install -r requirements.txt
    ```

## Usage

1.  **Run the App**:
    ```bash
    source venv/bin/activate && python app.py
    ```

2.  **Gather Samples**:
    - Click **"Add Class"** and name your object (e.g., "Apple").
    - Place the object inside the **Green Box**.
    - Click the **"Apple" button** multiple times to collect samples.
    - Aim for **20-30 samples** per object for best results.

3.  **Train**:
    - Click **"Train Model"**.
    - Wait for the "Model Trained Successfully" box.

4.  **Predict**:
    - Click **"Auto Predict (Toggle)"**.
    - Point the camera at your objects to see the detection!

## Troubleshooting
- **"ModuleNotFoundError: No module named '_tkinter'"**: This means your Python setup is missing Tkinter. Use the provided virtual environment command above which uses Homebrew's Python.
- **"Camera not found"**: Ensure your webcam is plugged in and allowed for terminal access.

## License
MIT
