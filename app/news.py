from newsapi import NewsApiClient
from app.config import Config

newsapi = NewsApiClient(api_key=Config.NEWS_API_KEY)

def get_top_headlines(country='tw', category=None, max_articles=10):
    try:
        top_headlines = newsapi.get_top_headlines(country=country, category=category, language='zh')
        articles = top_headlines['articles'][:max_articles]
        
        formatted_news = "今日頭條新聞:\n\n"
        for i, article in enumerate(articles, 1):
            formatted_news += f"{i}. {article['title']}\n"
            formatted_news += f"   {article['description']}\n"
            formatted_news += f"   閱讀更多: {article['url']}\n\n"
        
        return formatted_news
    except Exception as e:
        return f"獲取新聞時發生錯誤: {str(e)}"