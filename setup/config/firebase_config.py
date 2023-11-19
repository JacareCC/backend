import os
from firebase_admin import credentials, initialize_app
from dotenv import load_dotenv

load_dotenv()

cred_path = "./setup/config/cred_firebase.json"

cred = credentials.Certificate({"type": os.environ["SERVICE_ACCOUNT"],
    "project_id": os.environ["PROJECT_ID"],
    "private_key_id": os.environ["PRIVATE_KEY_ID"],
    "private_key": os.environ["PRIVATE_KEY"],
    "client_email": os.environ["CLIENT_EMAIL"],
    "client_id": os.environ["CLIENT_ID"],
    "auth_uri": os.environ["AUTH_URI"],
    "token_uri": os.environ["TOKEN_URI"],
    "auth_provider_x509_cert_url": os.environ["AUTH_PROVIDER_URL"],
    "client_x509_cert_url": os.environ["CLIENT_URL"],
    "universe_domain": os.environ["UNIVERSE_DOMAIN"]
})
firebase_app = initialize_app(cred)