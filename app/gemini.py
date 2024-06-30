import requests
import json
from app.config import Config

def summarize_with_gemini(messages):
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={Config.GEMINI_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    data = {
    "contents": [
        {
            "parts": [{"text": '請重點整理以下訊息，使用繁體中文回答：' + messages}]
        }
    ]
}
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return data.candidates[0].content.parts[0].text
    else:
        return f"Error: {response.status_code}"




