# Building a Streamlit Application with OpenAI Integration

This article will guide you through creating a Streamlit application in three parts. First, we'll build a basic Streamlit chat application with a static AI response. Then, we'll enhance the application to provide dynamic responses using OpenAI's GPT-3.5 model. 

## Prerequisites

Ensure you have the following installed:
- Python 3.9+
- Streamlit
- OpenAI Python client
- LangChain
- dotenv

## Set Up the Virtual Environment

1. **Create a Virtual Environment**:
   Open VS Code and open a terminal. Run the following command to create a new virtual environment:

    ```sh
    conda create -p venv python=3.9
    ```

2. **Activate the Virtual Environment**:
    ```sh
    conda activate venv
    ```

After that, you can install these dependencies using `pip`:

```sh
# pip install streamlit openai langchain-openai python-dotenv
```
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
```

####Step 2: Run the Application
Run the application using the following command:
```sh
streamlit run app.py
```
This will start a local Streamlit server and open your default web browser to display the chat application. You can enter messages, and the AI will always respond with "I don't know".

###Part 2: Integrating OpenAI for Dynamic Responses
Next, we'll enhance the application to provide dynamic responses using OpenAI's GPT-3.5 model.

####Step 1: Obtain an OpenAI API Key
Sign up at OpenAI and generate an API key. Save this key, as you'll need it to authenticate your requests.

####Step 2: Set Up Environment Variables
Create a .env file in your project directory and add your OpenAI API key:
```sh
OPENAI_API_KEY=your-openai-api-key
```
Step 3: Load Environment Variables
Update your app.py to load the environment variables and use the OpenAI API key:
```python
import os
import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# Load environment variables from the .env file
load_dotenv()

# Initialize the ChatOpenAI instance with the API key
llm = ChatOpenAI(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
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
        ai_response = get_response(user_query, st.session_state.chat_history)
        st.markdown(ai_response)
        st.session_state.chat_history.append(AIMessage(ai_response))
```
####Step 4: Run the Enhanced Application
Run the application again using the following command:
```sh
streamlit run app.py
```
