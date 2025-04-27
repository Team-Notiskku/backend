import os
import firebase_admin
from firebase_admin import credentials, firestore

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cred = credentials.Certificate(os.path.join(BASE_DIR, "assets", "firebase-key.json"))
firebase_admin.initialize_app(cred)

db = firestore.client()