import google.generativeai as genai
from app.config import Config

def summarize_with_gemini(messages):
    try:
        genai.configure(api_key=Config.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(
            f'請為以下聊天訊息做條列式的簡易重點整理，看前後語意判斷，講重點就好，不要太多冗言贅字，看起來是相同事件的訊息可以歸類在一列重點就好，使用繁體中文回答：{messages}')
        return response.text
    except Exception as e:
        print(f"Error in Gemini API: {str(e)}")
        return f"Error: {str(e)}"