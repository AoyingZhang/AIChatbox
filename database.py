from google.oauth2 import service_account
from google.cloud import firestore
import streamlit as st
# Authenticate to Firestore with the JSON account key.
import json
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
database = firestore.Client(credentials=creds, project="ai-chatbox-database")

#add file to database function
def addFile(db, docName, name, text):
    doc_ref = db.collection('users').document(docName)
    doc_ref.set({
        'name': name,
        'content': text
    })

def getFile(db, docName):
    doc_ref = db.collection("users").document(docName)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()['content']


