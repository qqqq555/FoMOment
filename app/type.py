if msg == '!輪播樣板':
        carousel_template = CarouselTemplate(columns=[
            CarouselColumn(
                text='選項 1',
                title='標題 1',
                thumbnail_image_url='https://storage.googleapis.com/你的圖片連結.png',
                actions=[
                    MessageAction(label='按鈕 1', text='按鈕 1')
                ]
            ),
            CarouselColumn(
                text='連結',
                title='連結',
                thumbnail_image_url='https://storage.googleapis.com/你的圖片連結.png',
                actions=[
                    URIAction(label='前往GOOGLE', uri='https://www.google.com')
                ]
            )
        ])
        return TemplateSendMessage(alt_text='輪播樣板', template=carousel_template)