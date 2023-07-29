
import os
import streamlit as st
import pandas as pd
from io import StringIO
from PyPDF2 import PdfReader
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import openai

openai.api_key = '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'
#set up using Langchain
chat = ChatOpenAI(temperature=0.0)

uploaded_file = st.file_uploader("Choose a PDF file")

if uploaded_file is not None:
    #read file
    reader = PdfReader(uploaded_file)
    
    # printing number of pages in pdf file
    print(len(reader.pages))
    
    for i in range(len(reader.pages)):
        page = reader.pages[i]
        text = page.extract_text()
        "Text inputed "+str(i+1)+ ":"
        text
        template_string = """Summarize the text \
        that is delimited by triple backticks \
        text: ```{text}```
        """
        prompt_template = ChatPromptTemplate.from_template(template_string)
        messages = prompt_template.format_messages(text=text)
        response = chat(messages)
        "\nSummary: \n"
        response.content



    