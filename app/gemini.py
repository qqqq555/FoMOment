import google.generativeai as genai
from app.config import Config
from app.firebase import delete_message

def check_message(group_id, message_id, message_text):
    try:
        genai.configure(api_key=Config.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(f"{message_text}")
    except Exception as e:
        delete_message(group_id, message_id)

def summarize_with_gemini(messages):
    try:
        genai.configure(api_key=Config.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(
            f'請為以下聊天訊息做條列式的簡易重點整理，看前後語意判斷，講重點就好，不要太多冗言贅字，重點列數盡量不要超過我給你的訊息量除以5，若訊息數小於5，給一條重點就好了，每一條不要超過15個字，使用繁體中文回答：{messages}')
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"