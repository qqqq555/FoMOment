import requests
from datetime import datetime, timedelta
from linebot.models import CarouselTemplate, CarouselColumn, MessageAction, URIAction, TemplateSendMessage

def get_exhibition_data():
    url = "https://cloud.culture.tw/frontsite/trans/SearchShowAction.do?method=doFindTypeJ&category=6"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def filter_exhibitions(exhibitions, city):
    today = datetime.now().date()
    filtered = []
    for ex in exhibitions:
        locations = [info['location'] for info in ex.get('showInfo', [])]
        start_date = datetime.strptime(ex.get('startDate', '1900/01/01'), "%Y/%m/%d").date()
        end_date = datetime.strptime(ex.get('endDate', '9999/12/31'), "%Y/%m/%d").date()
        if any(city in loc for loc in locations) and end_date >= today:
            if start_date > today:
                ex['days_to_start'] = (start_date - today).days
                ex['days_left'] = None
            else:
                ex['days_left'] = (end_date - today).days
                ex['days_to_start'] = None
            filtered.append(ex)
    
    return sorted(filtered, key=lambda x: (x['days_left'] is None, x['days_left'], x['days_to_start']))[:5]

def create_carousel_template(exhibitions):
    columns = []
    for exhibition in exhibitions:
        location = exhibition['showInfo'][0]['location'] if exhibition['showInfo'] else '未知地點'
        title = exhibition['title'] if exhibition['title'] else '未知展覽名稱'
        thumbnail_image_url = exhibition.get('image', 'https://storage.googleapis.com/你的圖片連結.png')
        columns.append(
            CarouselColumn(
                text=location,
                title=title,
                thumbnail_image_url=thumbnail_image_url,
                actions=[
                    MessageAction(label='按鈕 1', text=f"展覽名稱：{title}\n地點：{location}"),
                    URIAction(label='更多資訊', uri=exhibition['webSales'] if 'webSales' in exhibition else 'https://www.google.com')
                ]
            )
        )
    carousel_template = CarouselTemplate(columns=columns)
    return TemplateSendMessage(alt_text='輪播樣板', template=carousel_template)

def main(city):
    exhibitions = get_exhibition_data()
    if exhibitions:
        filtered_exhibitions = filter_exhibitions(exhibitions, city)
        if filtered_exhibitions:
            return create_carousel_template(filtered_exhibitions)
        else:
            return "目前沒有符合條件的展覽。"
    else:
        return "無法獲取展覽數據。~~"

// In your main function or webhook handler, you would call:
city = '台北市'  # Replace with the city you want to filter by
carousel_message = main(city)
