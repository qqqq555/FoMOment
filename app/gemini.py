import requests
from app.config import Config

def summarize_messages(messages):
    url = "https://api.gemini.com/v1/summarize"
    headers = {"Authorization": f"Bearer {Config.GEMINI_API_KEY}"}
    data = {"messages": messages}
    
    response = requests.post(url, headers=headers, json=data)
    return response.json().get("summary", "無法總結訊息")
