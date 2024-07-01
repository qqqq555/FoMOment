import google.generativeai as genai
from app.config import Config

def summarize_with_gemini(messages):
    try:
        genai.configure(api_key=Config.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(
            f'請為以下聊天內容做重點整理。(輸出規則：1. 使用條列式呈現2. 根據上下文判斷重要信息3. 保留核心內容，省略冗餘細節4. 回覆字數限制：原文字數的 1%5. 使用繁體中文回答6. 確保每個要點簡潔明瞭) 聊天內容：{messages}')
        return response.text
    except Exception as e:
        return f"Error: {str(e)}\n\n輸入敏感字詞有可能會出錯，請見諒QQ"