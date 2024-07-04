import requests
from datetime import datetime

def get_exhibition_data():
    url = "https://cloud.culture.tw/frontsite/trans/SearchShowAction.do?method=doFindTypeJOpenApi&category=6"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def filter_exhibitions(exhibitions, city):
    today = datetime.now().strftime("%Y/%m/%d")
    filtered = [
        ex for ex in exhibitions
        if city in ex.get('location', '')
        and ex.get('endDate', '') >= today
    ]
    return sorted(filtered, key=lambda x: x.get('startDate', ''))[:5]

def format_exhibition_info(exhibitions):
    formatted_info = "展覽資訊：\n\n"
    for exhibition in exhibitions:
        formatted_info += f"展覽名稱：{exhibition['title']}\n"
        formatted_info += f"地點：{exhibition['location']}\n"
        formatted_info += f"開始日期：{exhibition['startDate']}\n"
        formatted_info += f"結束日期：{exhibition['endDate']}\n"
        formatted_info += f"網址：{exhibition.get('website', '無')}\n\n"
    return formatted_info