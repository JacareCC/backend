import os
from firebase_admin import credentials, initialize_app
from dotenv import load_dotenv

load_dotenv()

if os.environ.get("ENV"):
    cred_path = "./setup/config/cred_firebase.json"
else:
    cred_path = {"type": os.environ.get("SERVICE_ACCOUNT"),
    "project_id": os.environ.get("PROJECT_ID"),
    "private_key_id": os.environ.get("PRIVATE_KEY_ID"),
    "private_key": os.environ.get("PRIVATE_KEY").replace('\\n', '\n'),
    "client_email": os.environ.get("CLIENT_EMAIL"),
    "client_id": os.environ.get("CLIENT_ID"),
    "auth_uri": os.environ.get("AUTH_URI"),
    "token_uri": os.environ.get("TOKEN_URI"),
    "auth_provider_x509_cert_url": os.environ.get("AUTH_PROVIDER_URL"),
    "client_x509_cert_url": os.environ.get("CLIENT_URL"),
    "universe_domain": os.environ.get("UNIVERSE_DOMAIN")
}

cred = credentials.Certificate(cred_path)
firebase_app = initialize_app(cred)