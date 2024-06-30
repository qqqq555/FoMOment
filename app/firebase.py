import firebase_admin
from firebase_admin import credentials, db
from app.config import Config
from datetime import datetime

firebase_admin.initialize_app(options={
    'databaseURL': Config.FIREBASE_URL
})

def get_new_messages(group_id):
    group_ref = db.reference(f'groups/{group_id}')
    last_entry_time = group_ref.child('last_entry_time').get()
    messages_ref = group_ref.child('messages')
    
    if not last_entry_time:
        return ["沒有新的訊息"]

    new_messages = messages_ref.order_by_child('timestamp').start_at(last_entry_time).get()
    if not new_messages:
        return ["沒有新的訊息"]

    # 更新最後進入聊天室時間
    group_ref.update({'last_entry_time': datetime.now().timestamp()})
    
    return [msg['text'] for msg in new_messages.values()]
