import streamlit as st
import pandas as pd
from io import StringIO
from PyPDF2 import PdfReader
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import openai
from google.oauth2 import service_account
from google.cloud import firestore
from dotenv import load_dotenv
import os
load_dotenv()  # take environment variables from .env.


#generate prompt template ->set up for AI
template_string = """Please handle the text \
that is delimited by triple backticks based on\
the following requirements that is delimited by triple pipes\
text: ```{text}```\
requirements:|||{requirements}|||\
"""
prompt_template = ChatPromptTemplate.from_template(template_string)

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

    else: 
        print("No such document!")

#get AI response function
def getAIResponse(prompt_template, content, user_input):
    if(user_input!=''):
        messages = prompt_template.format_messages(text=content, requirements=user_input)
        response = chat(messages)
        return response.content
    return ''

# Authenticate to Firestore with the JSON account key.
import json
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="ai-chatbox-database")


#Database info
#st.write("The id is: ", doc.id)
#st.write("The contents are: ", doc.to_dict())

#UI header
st.title('Welcome to the AI Chatbox web! ')
st.subheader('Please upload the _PDF_ file you want to get help about')
st.subheader('Then a chatbox will appear and what you need help about :sunglasses:')

openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_api_key

# set up using Langchain
chat = ChatOpenAI(openai_api_key=openai_api_key, temperature=0.0)
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
    name= getAIResponse(prompt_template, content, 'What is the name of the person? Please just answer 2 words.')
    docName = name+' Resume'
    addFile(db, docName, name, text)

#get answer
user_input = st.text_input('How can I help you?', '')
getResumeName= getAIResponse(prompt_template, user_input, 'What is the name of the person we are getting resume about? Please just answer 2 words.')+" Resume"
getResumeContent = getFile(db, getResumeName)
print(getResumeName)
st.write(getAIResponse(prompt_template, getResumeContent, user_input))



    
