import requests
from datetime import datetime
from linebot import LineBotApi
from linebot.models import FlexSendMessage, BubbleContainer, BoxComponent, TextComponent, ButtonComponent, URIAction

line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')

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

def create_flex_message(exhibitions):
    bubbles = []
    for exhibition in exhibitions:
        title = exhibition['title']
        description = exhibition['descriptionFilterHtml'][:100] + '...'
        location = exhibition['showInfo'][0]['location'] if exhibition['showInfo'] else '未知'
        start_date = exhibition['startDate']
        end_date = exhibition['endDate']

        bubble = BubbleContainer(
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(text=title, weight='bold', size='lg'),
                    BoxComponent(
                        layout='baseline',
                        contents=[
                            TextComponent(text='地點:', size='sm', color='#AAAAAA'),
                            TextComponent(text=location, size='sm', color='#666666')
                        ],
                    ),
                    BoxComponent(
                        layout='baseline',
                        contents=[
                            TextComponent(text='開始日期:', size='sm', color='#AAAAAA'),
                            TextComponent(text=start_date, size='sm', color='#666666')
                        ],
                    ),
                    BoxComponent(
                        layout='baseline',
                        contents=[
                            TextComponent(text='結束日期:', size='sm', color='#AAAAAA'),
                            TextComponent(text=end_date, size='sm', color='#666666')
                        ],
                    ),
                    ButtonComponent(
                        action=URIAction(label='查看更多', uri='http://example.com'),
                        style='link'
                    )
                ],
            )
        )
        bubbles.append(bubble)

    flex_message = FlexSendMessage(
        alt_text='展覽資訊',
        contents=BoxComponent(
            type='carousel',
            contents=bubbles
        )
    )

    return flex_message

def send_flex_message(user_id, exhibitions):
    flex_message = create_flex_message(exhibitions)
    line_bot_api.push_message(user_id, flex_message)

def main():
    city = "台北市"  
    exhibitions = get_exhibition_data()
    if exhibitions:
        filtered_exhibitions = filter_exhibitions(exhibitions, city)
        user_id = 'USER_ID'  
        send_flex_message(user_id, filtered_exhibitions)
    else:
        print("获取展览数据失败")

if __name__ == '__main__':
    main()
