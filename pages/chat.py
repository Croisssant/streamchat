import streamlit as st

from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_ollama import ChatOllama
st.session_state.TestConfigs = st.session_state.TestConfigs


class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]

graph_builder= StateGraph(State)

llm = ChatOllama(model="llama3.2")

def chatbot(state: State):
    return { "messages": [llm.invoke(state["messages"])] }

# The first argument is the unique node name
# The second argument is the function or object that will be called whenever
# the node is used.
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()

def stream_graph_updates(user_input: str):
    for msg, metadata in graph.stream({"messages": [{"role": "user", "content": user_input}]}, stream_mode="messages"):
        if msg.content:
            yield msg.content
           

    
st.title("StreamChat")

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
        response = st.write_stream(stream_graph_updates(prompt))
    st.session_state.messages.append({ "role": "assistant", "content": response })




# if 'TestConfigs' in st.session_state:

#     st.header(f"Knowledge Entity Extraction", divider="blue")
#     st.table(st.session_state.TestConfigs["KnowledgeEntityExtraction"])

#     st.header(f"Testing Query Generation", divider="blue")
#     st.table(st.session_state.TestConfigs["TestingQueryGeneration"])

#     st.header(f"Knowledge Graph Construction", divider="blue")
#     st.table(st.session_state.TestConfigs["KnowledgeGraphConstruction"])
   