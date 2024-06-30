import firebase_admin
from firebase_admin import credentials, firestore
from gemini_utils import generate_summary
from config import FIREBASE_CREDENTIALS_PATH

cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
firebase_admin.initialize_app(cred)
db = firestore.client()

def store_message(group_id, user_id, message):
    doc_ref = db.collection('groups').document(group_id).collection('messages').document()
    doc_ref.set({
        'user_id': user_id,
        'message': message,
        'timestamp': firestore.SERVER_TIMESTAMP,
        'read': False
    })

def summarize_unread_messages(group_id):
    unread_messages = db.collection('groups').document(group_id).collection('messages').where('read', '==', False).order_by('timestamp').get()
    
    messages_text = "\n".join([msg.to_dict()['message'] for msg in unread_messages])
    
    summary = generate_summary(messages_text)
    
    for msg in unread_messages:
        msg.reference.update({'read': True})
    
    return summary