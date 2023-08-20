import streamlit as st
import pandas as pd
from io import StringIO
from PyPDF2 import PdfReader
from langchain.chat_models import ChatOpenAI

from dotenv import load_dotenv
import database as db
load_dotenv()  # take environment variables from .env.
import ai_response as ai



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
    name= ai.from_text_answer_question(content, 'What is the name of the person? Please just answer 2 words. Make sure the first word is the first name and second word is the last name. Please answer 2 words. ')
    docName = name+' Resume'
    db.addFile(db.database, docName, name, text)

#get answer
user_input = st.chat_input('How can I help you?')
if user_input is not None:
    with st.chat_message("user"):
        print(user_input)
        st.markdown(user_input)
getResumeName= ai.from_text_answer_question(user_input, 'What is the name of the person? Please just answer 2 words. Make sure the first word is the first name and second word is the last name.')+" Resume"
getResumeContent = db.getFile(db.database, getResumeName)
print(getResumeName)
res = ai.from_text_answer_question(getResumeContent, user_input)

if user_input is not None and res is not None:
    with st.chat_message("assistant"):
        print(res)
        st.markdown(res)



    
