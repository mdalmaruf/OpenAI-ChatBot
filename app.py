import os
import getpass
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Initialize the ChatOpenAI instance with the API key
llm = ChatOpenAI(
    api_key="sk-",
    model="gpt-3.5-turbo",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
)

# Define the get_response function
def get_response(query, chat_history):
    template = """
    You are a helpful assistant. Answer the following questions considering the chat history:

    Chat history: {chat_history}

    User question: {user_question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({
        "chat_history": chat_history,
        "user_question": query
    })

# Initialize Streamlit chat interface
import streamlit as st

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(page_title="Streaming Bot", page_icon="🤖")
st.title("Streaming Bot")

# conversation
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)
    else:
        with st.chat_message("AI"):
            st.markdown(message.content)

user_query = st.chat_input("Your message")
if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(user_query))
    with st.chat_message("Human"):
        st.markdown(user_query)
    with st.chat_message("AI"):
        ai_response = get_response(user_query, st.session_state.chat_history)
        st.markdown(ai_response)
        st.session_state.chat_history.append(AIMessage(ai_response))
