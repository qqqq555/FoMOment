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
    formatted_info = "展覽資訊：\n\n"
    for exhibition in exhibitions:
        formatted_info += f"展覽名稱：{exhibition['title']}\n"
        if exhibition['showInfo']:
            formatted_info += f"地點：{exhibition['showInfo'][0]['locationName']}\n"
        formatted_info += f"開始日期：{exhibition['startDate']}\n"
        formatted_info += f"結束日期：{exhibition['endDate']}\n"
        formatted_info += f"活動官網：{exhibition['sourceWebPromote']}\n"
        if exhibition['days_left'] is not None:
            formatted_info += f"剩餘天數：{exhibition['days_left']}天\n"
        else:
            formatted_info += f"距離開始：{exhibition['days_to_start']}天\n"
        formatted_info += f"主辦單位：{', '.join(exhibition['masterUnit'])}\n"
        formatted_info += f"簡介：{exhibition['descriptionFilterHtml'][:100]}...\n\n"
    return formatted_info