import requests
from app.config import Config

def summarize_with_gemini(messages):
    url = "https://api.gemini.com/v1/summarize"
    headers = {"Authorization": f"Bearer {Config.GEMINI_API_KEY}"}
    data = {"messages": messages}
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get("summary", "無法總結訊息")
    else:
        return f"Error: {response.status_code}"
