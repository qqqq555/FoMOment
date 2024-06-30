import firebase_admin
from firebase_admin import credentials, db
from app.config import Config
from datetime import datetime

firebase_admin.initialize_app(options={
    'databaseURL': Config.FIREBASE_URL
})

d in messages.values()]

def clear_messages(group_id):
    messages_ref = db.reference(f'groups/{group_id}/messages')
    messages_ref.delete()

def add_message(group_id, message_text):
    messages_ref = db.reference(f'groups/{group_id}/messages')
    message_id = messages_ref.push().key
    message_data = {
        "text": message_text
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
