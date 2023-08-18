from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os
import openai
openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_api_key

chat = ChatOpenAI(openai_api_key=openai_api_key, temperature=0.0)

#===========================from text answer question=========================
#generate prompt template ->set up for AI
from_text_answer_question_prompt = """Please handle the text \
that is delimited by triple backticks based on\
the following requirements that is delimited by triple pipes\
text: ```{text}```\
requirements:|||{requirements}|||\
"""
from_text_answer_question_prompt_template = ChatPromptTemplate.from_template(from_text_answer_question_prompt)

#get AI response function
def from_text_answer_question(content, user_input):
    
    if(user_input!=''):
        messages = from_text_answer_question_prompt_template.format_messages(text=content, requirements=user_input)
        response = chat(messages)
        return response.content
    return ''
