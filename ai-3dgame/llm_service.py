
from groq import Groq
import streamlit as st
from config import Config

class LLMService:
    @staticmethod
    def get_deepseek_reasoning(query: str, api_key: str):
        """
        Fetches reasoning from DeepSeek R1 Distill model via Groq.
        """
        if not api_key:
             raise ValueError("Groq API Key is missing.")
             
        client = Groq(api_key=api_key)
        
        response = client.chat.completions.create(
            model=Config.MODEL_NAME,
            messages=[
                {"role": "system", "content": Config.SYSTEM_PROMPT},
                {"role": "user", "content": query}
            ],
            temperature=0.6,
            max_tokens=4096,
            top_p=0.95,
            stream=False,
            stop=None,
        )
        
        # DeepSeek R1 on Groq usually helps to just get the content directly as it's a distilled model
        return response.choices[0].message.content

    @staticmethod
    def extract_code_with_agno(reasoning_content: str, api_key: str):
        """
        Extracts code from the response. Since we are using Groq/DeepSeek-R1-Distill, 
        we can often just clean the output, or use a smaller Llama model on Groq to extract if needed.
        For simplicity and cost (Free), we will use the same model/client to ensure code format.
        """
        if "```python" in reasoning_content:
            import re
            match = re.search(r'```python(.*?)```', reasoning_content, re.DOTALL)
            if match:
                return match.group(1).strip()
        
        if "```" in reasoning_content:
             import re
             match = re.search(r'```(.*?)```', reasoning_content, re.DOTALL)
             if match:
                return match.group(1).strip()

        return reasoning_content
