import streamlit as st
# from langchain.llms import Ollama
# from langchain.agents import AgentType, initialize_agent, load_tools, AgentExecutor, create_react_agent
# from langchain.callbacks import StreamlitCallbackHandler
# from langchain.callbacks.manager import CallbackManager
# from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
# from langchain_core.prompts.prompt import PromptTemplate
# from langchain.tools import tool

# from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
# from langchain_core.messages import AIMessage

import random
import time


st.session_state.TestConfigs = st.session_state.TestConfigs



# template = """
# Question: {question}

# Answer: Let's think step by step.
# """

# prompt = ChatPromptTemplate.from_template(template)

# model = OllamaLLM(model="llama3.1")





# chain = prompt | model

def response_generator_fixed():
    response = random.choice([
        "Hello there! How can I assist you today?",
        "Hi, human! Is there anything I can help you with?",
        "Do you need help?",
    ])

    for word in response.split():
        yield word + " "
        time.sleep(0.05)

# def response_generator_ollama(input_text):
#     model = Ollama(
#         model="llama2-uncensored:latest",
#         callback_manager=CallbackManager([StreamingStdOutCallbackHandler()])
#     )

#     return model.stream(input_text)

def response_generator_ollama(input_text):
    llm = ChatOllama(model="llama3.2")
    
    return llm.astream(input_text)
      
      

st.title("Simple Chat")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):

    with st.chat_message("user"):
        st.markdown(prompt)    
    st.session_state.messages.append({ "role": "user", "content": prompt })

 
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator_ollama(prompt))
    st.session_state.messages.append({ "role": "assistant", "content": response })




# if 'TestConfigs' in st.session_state:

#     st.header(f"Knowledge Entity Extraction", divider="blue")
#     st.table(st.session_state.TestConfigs["KnowledgeEntityExtraction"])

#     st.header(f"Testing Query Generation", divider="blue")
#     st.table(st.session_state.TestConfigs["TestingQueryGeneration"])

#     st.header(f"Knowledge Graph Construction", divider="blue")
#     st.table(st.session_state.TestConfigs["KnowledgeGraphConstruction"])
   