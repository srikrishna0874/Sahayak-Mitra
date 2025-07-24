import firebase_admin
from firebase_admin import credentials,storage, firestore
import datetime
from io import BytesIO

cred = credentials.Certificate("Firebase/sahayak-mitra-firebase-adminsdk-fbsvc-caa1fa3039.json")
firebase_admin.initialize_app(cred,{"storageBucket": "sahayak-mitra"})



bucket=storage.bucket()

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
    
    
