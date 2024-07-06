from gnews import GNews
from app.config import Config

google_news = GNews(language=Config.NEWS_LANGUAGE, country='Taiwan', max_results=10)

def get_news_carousel():
    try:
        news_items = google_news.get_top_news()
        return [
            {
                'title': item['title'][:40], 
                'url': item['url'],
                'image': item.get('image', 'https://storage.googleapis.com/sitconimg/img/news.png')
            }
            for item in news_items[:10]
        ]
    except Exception as e:
        return f"獲取新聞時發生錯誤: {str(e)}"