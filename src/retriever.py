import requests
from src.config import LLM_API_URL, LLM_MODEL, SYSTEM_PROMPT

def run_llm(messages):
    payload = {
        "model": LLM_MODEL,
        "messages": messages,
        "temperature": 0.5,
        "stream": False
    }

    try:
        res = requests.post(LLM_API_URL, json=payload)
        content = res.json()['choices'][0]['message']['content']
        return content
    except Exception as e:
        return f"⚠️ LLM error: {e}"
