import requests
import google.generativeai as genai
from app.config import Config

def summarize_with_gemini(messages):
    genai.configure(api_key={Config.GEMINI_API_KEY})
    if response.status_code == 200:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(
            f'請條列式重點整理以下訊息，使用繁體中文回答：{messages}')
        return response.text
    return f"Error: {response.status_code}"