import requests
import json
from app.config import Config

def summarize_with_gemini(messages):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={Config.GEMINI_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    data = {
    "contents": [
        {
            "parts": [{"請重點整理以下訊息，使用繁體中文回答："  + messages}]
        }
    ]
}
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get("summary", "無法總結訊息")
    else:
        return f"Error: {response.status_code}"




