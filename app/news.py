from gnews import GNews
from app.config import Config

google_news = GNews(language=Config.NEWS_LANGUAGE, country='Taiwan', max_results=5)

def get_top_headlines():
    try:
        news_items = google_news.get_top_news()
        formatted_news = "今日頭條新聞：\n\n"
        for i, item in enumerate(news_items, 1):
            formatted_news += f"{i}. {item['title']}\n"
            formatted_news += f"   {item['description']}\n"
            formatted_news += f"   閱讀更多: {item['url']}\n\n"
        return formatted_news
    except Exception as e:
        return f"獲取新聞時發生錯誤: {str(e)}"
