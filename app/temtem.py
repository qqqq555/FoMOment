from linebot.models import MessageEvent, TextMessage, TextSendMessage, JoinEvent, LeaveEvent,TemplateSendMessage,ButtonsTemplate,MessageAction,PostbackAction,ImageCarouselTemplate,ImageCarouselColumn,ImageSendMessage
def template_message(msg):
    if msg == '!輪播樣板':
            carousel_template = CarouselTemplate(columns=[
                CarouselColumn(
                    text='選項 1',
                    title='標題 1',
                    thumbnail_image_url='../img/大吉.png',
                    actions=[
                        MessageAction(label='按鈕 1', text='按鈕 1')
                    ]
                ),
                CarouselColumn(
                    text='連結',
                    title='連結',
                    thumbnail_image_url='../img/大吉.png',
                    actions=[
                        URIAction(label='前往GOOGLE', uri='https://www.google.com')
                    ]
                )
            ])
            return (alt_text='輪播樣板', template=carousel_template)