import os
from firebase_admin import credentials, initialize_app
from dotenv import load_dotenv

load_dotenv()

cred_path = "./setup/config/cred_firebase.json"

cred = credentials.Certificate(cred_path)
firebase_app = initialize_app(cred)