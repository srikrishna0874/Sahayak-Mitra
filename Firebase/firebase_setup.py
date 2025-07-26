import firebase_admin
from firebase_admin import credentials,storage, firestore
import datetime
from io import BytesIO

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(BASE_DIR, 'sahayak-mitra-firebase-adminsdk-fbsvc-649d91ea91.json')

cred = credentials.Certificate(json_path)
firebase_admin.initialize_app(cred,{"storageBucket": "sahayak-mitra"})



bucket=storage.bucket()
firestore_db=firestore.client()

def upload_file_to_firebase(sender, content_type,file,file_extension,userWaId=None):
    file_name= f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.{file_extension}"
    print(cred.project_id)
    destination_blob_name = "Chat_files/"
    if sender == "user":
        destination_blob_name += "user/"+userWaId+"/"
    elif sender == "bot":
        destination_blob_name += "bot/"+userWaId+"/"
    destination_blob_name += file_name
    print(f"Uploading file to {destination_blob_name} in Firebase Storage")
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_file(BytesIO(file),content_type=content_type)
    blob.make_public()
    print(f"File {destination_blob_name} uploaded to {destination_blob_name}.")
    return f"https://storage.googleapis.com/sahayak-mitra/{destination_blob_name}"
    
    
def insert_new_document_to_firestore(waId, messageType,messageBody,sender):
    messages_collection = firestore_db.collection("chats").document(waId).collection("messages")
    print("Inserting new message to Firestore")
    new_message = {
        "messageType": messageType,
        "messageBody": messageBody,
        "timestamp": firestore.SERVER_TIMESTAMP,
        "sender": sender
    }

    # Add the new message to the collection
    messages_collection.add(new_message)
    print("Message added successfully!")
    
    

    
    
def get_recent_ten_messages(waId):
    messages_collection = firestore_db.collection("chats").document(waId).collection("messages")
    print("Fetching recent ten messages from Firestore")
    recent_messages = messages_collection.order_by("timestamp", direction=firestore.Query.DESCENDING).limit(10).stream()
    
    messages_list = []
    for message in recent_messages:
        data=message.to_dict()
        print(f"Message ID: {message.id}, Data: {data}")
        filtered = {
            'messageType': message.get('messageType'),
            'messageBody': message.get('messageBody'),
            'sender': message.get('sender'),
            'timeStamp': str(message.get('timestamp'))
        }
        messages_list.append(filtered)
    
    return messages_list
    
    
# print(get_recent_ten_messages("1234567890"))  # Replace with actual WhatsApp ID to test
    
 