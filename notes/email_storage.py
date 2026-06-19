import json
import os
from datetime import datetime

STORAGE_FILE = "/app/email_storage.json"

def get_emails():
    if not os.path.exists(STORAGE_FILE):
        return []
    try:
        with open(STORAGE_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_email(email_data):
    emails = get_emails()
    email_data["id"] = len(emails) + 1
    email_data["sent_at"] = datetime.now().isoformat()
    emails.append(email_data)
    with open(STORAGE_FILE, 'w') as f:
        json.dump(emails, f, indent=2, default=str)
    return True

def clear_emails():
    if os.path.exists(STORAGE_FILE):
        os.remove(STORAGE_FILE)
    return {"message": "Emails cleared"}