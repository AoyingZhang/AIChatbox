import streamlit as st
import pandas as pd
from io import StringIO
from PyPDF2 import PdfReader
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import openai
from google.oauth2 import service_account

from dotenv import load_dotenv
import os
load_dotenv()  # take environment variables from .env.


from google.cloud import firestore

# Authenticate to Firestore with the JSON account key.
import json
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="ai-chatbox-database")

# Create a reference to the Google post.
doc_ref = db.collection("posts").document("Google")

# Then get the data at that reference.
doc = doc_ref.get()

#Database info
#st.write("The id is: ", doc.id)
#st.write("The contents are: ", doc.to_dict())

st.title('Welcome to the AI Chatbox web! ')
st.subheader('Please upload the _PDF_ file you want to get help about')
st.subheader('Then a chatbox will appear and what you need help about :sunglasses:')

openai_api_key = os.getenv("OPENAI_API_KEY")
print(openai_api_key) 
openai.api_key = openai_api_key

# set up using Langchain
chat = ChatOpenAI(openai_api_key=openai_api_key, temperature=0.0)


uploaded_file = st.file_uploader("Choose a PDF file")

if uploaded_file is not None:
    #read file
    reader = PdfReader(uploaded_file)
    
    # printing number of pages in pdf file
    print(len(reader.pages))
    
    content = ''
    for i in range(len(reader.pages)):
        page = reader.pages[i]
        text = page.extract_text()
        content = content+text
    #content

    user_input = st.text_input('How can I help you?', 'Please summarize the text content')

    template_string = """Please handle the text \
    that is delimited by triple backticks based on\
    the following requirements that is delimited by triple pipes\
    text: ```{text}```\
    requirements:|||{requirements}|||\
    """
    prompt_template = ChatPromptTemplate.from_template(template_string)
    messages = prompt_template.format_messages(text=content, requirements=user_input)
    response = chat(messages)
    "\nHere's the response: \n"
    response.content



    
