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
    filtered = []
    for ex in exhibitions:
        locations = [info['location'] for info in ex.get('showInfo', [])]
        if any(city in loc for loc in locations) and ex.get('endDate', '') >= today:
            filtered.append(ex)
    return sorted(filtered, key=lambda x: x.get('startDate', ''))[:5]

def format_exhibition_info(exhibitions):
    formatted_info = "展覽資訊：\n\n"
    for exhibition in exhibitions:
        formatted_info += f"展覽名稱：{exhibition['title']}\n"
        if exhibition['showInfo']:
            formatted_info += f"地點：{exhibition['showInfo'][0]['location']}\n"
            formatted_info += f"開始時間：{exhibition['showInfo'][0]['time']}\n"
            formatted_info += f"結束時間：{exhibition['showInfo'][0]['endTime']}\n"
        formatted_info += f"開始日期：{exhibition['startDate']}\n"
        formatted_info += f"結束日期：{exhibition['endDate']}\n"
        formatted_info += f"主辦單位：{', '.join(exhibition['masterUnit'])}\n"
        formatted_info += f"簡介：{exhibition['descriptionFilterHtml'][:100]}...\n\n"
    return formatted_info