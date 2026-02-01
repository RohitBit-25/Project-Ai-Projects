# Text-to-SQL Agent

This application allows you to query a SQL database using natural language. It uses an LLM (Groq Llama 3) to convert English questions into SQL queries, executes them against a SQLite database, and returns the results.

## Features

-   **Natural Language Querying**: Ask questions in plain English (e.g., "How many students are in the Data Science course?").
-   **SQL Database**: Uses a local SQLite database (`student.db`).
-   **Streamlit UI**: Simple and interactive web interface.

## Prerequisites

-   Python 3.8+
-   A Groq API Key (Get one from [Groq Console](https://console.groq.com/))

## Installation

1.  **Clone the repository** (if you haven't already).
2.  **Navigate to the project directory**:
    ```bash
    cd Text-Sql-Agent
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1.  **Set up Environment Variables**:
- 
    -   Open `.env` and add your Groq API Key:
        ```env
        GROQ_API_KEY=gsk_...
        ```

1.  **Initialize the Database**:
    -   Run the `database.py` script to create the table and insert sample data:
        ```bash
        python database.py
        ```
    -   This will create a `student.db` file in the directory.

## Usage

1.  **Run the Application**:
    ```bash
    streamlit run main.py
    ```
2.  **Interact**:
    -   Open the URL provided in the terminal (usually `http://localhost:8501`).
    -   Type your question in the input box and press "Enter".

## Example Questions

-   "How many entries of records are present?"
-   "Tell me all the students studying in Data Science COURSE?"
-   "What are the marks of Student1?"
