import streamlit as st
import pandas as pd
from io import StringIO
from PyPDF2 import PdfReader
from langchain.chat_models import ChatOpenAI
from google.oauth2 import service_account
from google.cloud import firestore
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
import ai_response as ai


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

    


# Authenticate to Firestore with the JSON account key.
import json
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="ai-chatbox-database")


#Database info
#st.write("The id is: ", doc.id)
#st.write("The contents are: ", doc.to_dict())

#UI header
st.title('Welcome to the AI resume helper web! ')
st.subheader('Please upload new resume _PDF_ to the database')
st.subheader('Or specify the name and ask any question about an existing resume')


# set up using Langchain

uploaded_file = st.file_uploader("Choose a PDF file")
content=''



#upload file to the database
if uploaded_file is not None:
    #read file
    reader = PdfReader(uploaded_file)

    #convert to text
    content = ''
    for i in range(len(reader.pages)):
        page = reader.pages[i]
        text = page.extract_text()
        content = content+text
    
    #get person name and doc name
    name= ai.from_text_answer_question(content, 'What is the name of the person? Please just answer 2 words. Make sure the first name is the first name and second word is the last name. ')
    docName = name+' Resume'
    addFile(db, docName, name, text)

#get answer
user_input = st.chat_input('How can I help you?')
if(user_input and user_input!='None'):
    with st.chat_message("user"):
        print(user_input)
        st.markdown(user_input)
getResumeName= ai.from_text_answer_question(user_input, 'What is the name of the person we are getting resume about? Please just answer 2 words.')+" Resume"
getResumeContent = getFile(db, getResumeName)
print(getResumeName)
res = ai.from_text_answer_question(getResumeContent, user_input)

if(res and res!='requirements: None'):
    with st.chat_message("assistant"):
        print(res)
        st.markdown(res)



    
