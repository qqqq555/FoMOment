import random
from linebot.models import FlexSendMessage, BubbleContainer, BoxComponent, TextComponent, ImageComponent

FORTUNES = ["大吉", "吉", "中吉", "小吉", "末吉", "凶"]

FORTUNES_IMAGES = {
    "大吉": [
        "https://storage.cloud.google.com/sitconimg/img/%E5%A4%A7%E5%90%89.png"
    ],
    "吉": [
        "https://storage.cloud.google.com/sitconimg/img/%E5%90%89.png"
    ],
    "中吉": [
        "https://storage.cloud.google.com/sitconimg/img/%E4%B8%AD%E5%90%89.png"
    ],
    "小吉": [
        "https://storage.cloud.google.com/sitconimg/img/%E5%B0%8F%E5%90%89.png"
    ],
    "末吉": [
        "https://storage.cloud.google.com/sitconimg/img/%E6%9C%AB%E5%90%89.png"
    ],
    "凶": [
        "https://storage.cloud.google.com/sitconimg/img/%E5%87%B6.png"
    ]
}

FORTUNE_MESSAGES = {
    "大吉": [
        "今天會是美好的一天！充滿希望和機遇。",
        "你的努力將得到回報，繼續保持積極的態度。",
        "好運將伴隨著你，勇敢地追逐你的夢想吧！"
    ],
    "吉": [
        "今天運氣不錯，保持樂觀的心態。",
        "可能會有意外的驚喜，保持警覺。",
        "適合嘗試新事物，或許會有意想不到的收穫。"
    ],
    "中吉": [
        "平穩的一天，適合專注於日常任務。",
        "保持平和的心態，不要輕易被外界干擾。",
        "可能會遇到一些小挑戰，但都能順利解決。"
    ],
    "小吉": [
        "今天運勢平平，多多關注身邊的人和事。",
        "可能會有些小麻煩，但別擔心，都能克服。",
        "適合反思和計劃，為未來做好準備。"
    ],
    "末吉": [
        "今天可能會遇到一些困難，保持冷靜和耐心。",
        "不要輕易做重要決定，多聽聽他人的意見。",
        "適合整理和反省，為明天做好準備。"
    ],
    "凶": [
        "今天運勢不佳，但別灰心，明天會更好。",
        "小心謹慎為上，避免衝動的行為。",
        "多關心身邊的人，他們的支持會給你力量。"
    ]
}

def get_daily_fortune():
    fortune = random.choice(FORTUNES)
    message = random.choice(FORTUNE_MESSAGES[fortune])
    return fortune, message

def create_fortune_flex_message(fortune, message):
    bubble = BubbleContainer(
        body=BoxComponent(
            layout="vertical",
            contents=[
                ImageComponent(
                    url=FORTUNES_IMAGES[fortune],
                    size="full",
                    aspect_mode="cover",
                    aspect_ratio="1:1"
                ),
                TextComponent(
                    text=fortune,
                    weight="bold",
                    size="xl",
                    margin="md"
                ),
                TextComponent(
                    text=message,
                    size="sm",
                    wrap=True,
                    margin="md"
                )
            ]
        )
    )
    return FlexSendMessage(alt_text="今日運勢", contents=bubble)