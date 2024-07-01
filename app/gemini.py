import google.generativeai as genai
from app.config import Config

def summarize_with_gemini(messages):
    try:
        genai.configure(api_key=Config.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(
            f'請為以下聊天訊息做條列式的重點整理，看前後語意判斷，講重點就好，不要太多冗言贅字，回覆字數盡量不超過我給你的文字數量除以100，使用繁體中文回答：{messages}')
        return response.text
    except Exception as e:
        return f"Error: {str(e)}\n\n輸入敏感字詞有可能會出錯，請見諒QQ"