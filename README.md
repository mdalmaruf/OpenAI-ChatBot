# Building a Streamlit Application with OpenAI Integration

This article will guide you through creating a Streamlit application in three parts. First, we'll build a basic Streamlit chat application with a static AI response. Then, we'll enhance the application to provide dynamic responses using OpenAI's GPT-3.5 model. 

## Prerequisites

Ensure you have the following installed:
- Python 3.9+
- Streamlit
- OpenAI Python client
- LangChain
- dotenv

You can install these dependencies using `pip`:

```sh
pip install streamlit openai langchain-openai python-dotenv

###Part 1: Creating a Basic Streamlit Application
We'll start by creating a basic Streamlit application that accepts user input and responds with a static message.

####Step 1: Set Up the Environment
Create a file named app.py and add the following code:
```python
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(page_title="Streaming Bot", page_icon="🤖")
st.title("Streaming Bot")

# Display chat history
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
        ai_response = "I don't know"
        st.markdown(ai_response)
        st.session_state.chat_history.append(AIMessage(ai_response))
'''
