import os
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from dotenv import load_dotenv

load_dotenv()

cred_path = os.getenv("FIREBASE_CRED_PATH")
credentials = service_account.Credentials.from_service_account_file(
    cred_path,
    scopes=["https://www.googleapis.com/auth/datastore"]
)

PROJECT_ID = credentials.project_id
FIRESTORE_URL = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents"


def _get_access_token():
    if not credentials.valid:
        credentials.refresh(Request())
    return credentials.token


def save_analysis(resume_name, result):
    token = _get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    body = {
        "fields": {
            "resume_name": {"stringValue": resume_name},
            "result": {"stringValue": result}
        }
    }
    response = requests.post(
        f"{FIRESTORE_URL}/ats_analyses",
        headers=headers,
        json=body,
        timeout=15
    )
    response.raise_for_status()
    return response.json()