import requests
from datetime import datetime, timedelta

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

def format_exhibition_info(exhibitions):
    columns = []
    for exhibition in exhibitions:
        title = exhibition['title']
        column = CarouselColumn(
            text=f"展覽名稱：{title}",
            title=title,
            thumbnail_image_url='https://storage.googleapis.com/sitconimg/img/iconmonstr-location-2-240.png',
            actions=[
                MessageAction(label='查看詳情', text=f"{title} 詳情"),
                URIAction(label='前往Google', uri='https://www.google.com')
            ]
        )
        columns.append(column)
    
    carousel_template = CarouselTemplate(columns=columns)
    return carousel_template

