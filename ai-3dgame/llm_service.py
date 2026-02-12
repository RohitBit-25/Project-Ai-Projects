
from openai import OpenAI
from agno.agent import Agent as AgnoAgent
from agno.run.agent import RunOutput
from agno.models.openai import OpenAIChat as AgnoOpenAIChat
import streamlit as st
from config import Config

class LLMService:
    @staticmethod
    def get_deepseek_reasoning(query: str, api_key: str):
        """
        Fetches reasoning from DeepSeek model.
        """
        if not api_key:
             raise ValueError("DeepSeek API Key is missing.")
             
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )
        
        response = client.chat.completions.create(
            model="deepseek-reasoner",
            messages=[
                {"role": "system", "content": Config.SYSTEM_PROMPT},
                {"role": "user", "content": query}
            ],
            max_tokens=1 # We only need reasoning content, which is separate from content
        )
        
        return response.choices[0].message.reasoning_content

    @staticmethod
    def extract_code_with_agno(reasoning_content: str, api_key: str):
        """
        Uses Agno Agent (OpenAI) to extract Python code from reasoning.
        """
        if not api_key:
             raise ValueError("OpenAI API Key is missing.")

        agent = AgnoAgent(
            model=AgnoOpenAIChat(
                id="gpt-4o",
                api_key=api_key
            ),
            debug_mode=True,
            markdown=True
        )
        
        extraction_prompt = Config.EXTRACTION_PROMPT.format(reasoning_content=reasoning_content)
        
        response: RunOutput = agent.run(extraction_prompt)
        return response.content
