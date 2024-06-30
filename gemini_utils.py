import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def generate_summary(text):
    response = model.generate_content(f"請對以下對話進行重點摘要:\n{text}")
    return response.text