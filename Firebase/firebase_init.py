import os
from firebase_admin import credentials

key_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "sahayak-mitra-firebase-adminsdk-fbsvc-649d91ea91.json")
cred = credentials.Credentials(key_path)
