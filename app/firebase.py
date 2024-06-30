import firebase_admin
from firebase_admin import credentials, db
from app.config import Config

firebase_admin.initialize_app(options={
    'databaseURL': Config.FIREBASE_URL
})

def get_unread_messages(group_id):
    ref = db.reference(f'groups/{group_id}/unread_messages')
    unread_messages = ref.get()
    if not unread_messages:
        return ["沒有未讀訊息"]
    return [msg['text'] for msg in unread_messages.values()]
