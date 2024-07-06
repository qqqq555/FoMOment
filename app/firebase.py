import firebase_admin
from firebase_admin import db
from app.config import Config
from datetime import datetime

firebase_admin.initialize_app(options={
    'databaseURL': Config.FIREBASE_URL
})

def get_messages(group_id):
    messages_ref = db.reference(f'groups/{group_id}/messages')
    messages = messages_ref.get()
    if not messages:
        return []
    return [f"{msg['user']}: {msg['text']}" for msg in messages.values()]

def clear_messages(group_id):
    messages_ref = db.reference(f'groups/{group_id}/messages')
    messages_ref.delete()

def add_message(group_id, message_text, user_name):
    messages_ref = db.reference(f'groups/{group_id}/messages')
    message_id = messages_ref.push().key
    message_data = {
        "text": message_text,
        "user": user_name
    }
    messages_ref.child(message_id).set(message_data)

def get_summary_count(group_id):
    group_ref = db.reference(f'groups/{group_id}')
    summary_count = group_ref.child('summary_count').get()
    if summary_count is None:
        return 50
    return summary_count

def set_summary_count(group_id, count):
    group_ref = db.reference(f'groups/{group_id}')
    group_ref.update({'summary_count': count})

def delete_group_data(group_id):
    group_ref = db.reference(f'groups/{group_id}')
    group_ref.delete()

def check_fortune_usage(user_id):
    today = datetime.now().strftime("%Y-%m-%d")
    user_ref = db.reference(f'users/{user_id}/fortune_usage')
    last_usage = user_ref.get()
    if last_usage == today:
        return False
    user_ref.set(today)
    return True