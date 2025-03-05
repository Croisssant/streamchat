import streamlit as st

from typing import Annotated
from typing_extensions import TypedDict

from langchain_ollama import ChatOllama
from langchain_community.tools.tavily_search import TavilySearchResults

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from basictoolnode import BasicToolNode


st.session_state.TestConfigs = st.session_state.TestConfigs


class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]

graph_builder= StateGraph(State)
tool = TavilySearchResults(max_results=2)
tools = [tool]
llm = ChatOllama(model="llama3.2").bind_tools(tools)

def chatbot(state: State):
    return { "messages": [llm.invoke(state["messages"])] }


def stream_graph_updates(user_input: str):
    for msg, metadata in graph.stream({"messages": [{"role": "user", "content": user_input}]}, stream_mode="messages"):
        if msg.content:
            yield msg.content


def route_tools(state: State):
    """
    Use in the conditional_edge to route to the ToolNode if the last message
    has tool calls. Otherwise, route to the end.
    """
    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools"
    return END

# The first argument is the unique node name
# The second argument is the function or object that will be called whenever
# the node is used.
graph_builder.add_node("chatbot", chatbot)

# tool_node = BasicToolNode(tools=[tool])
tool_node = ToolNode(tools=[tool])

graph_builder.add_node("tools", tool_node)
# The `tools_condition` function returns "tools" if the chatbot asks to use a tool, and "END" if
# it is fine directly responding. This conditional routing defines the main agent loop.
# graph_builder.add_conditional_edges(
#     "chatbot",
#     route_tools,
#     # The following dictionary lets you tell the graph to interpret the condition's outputs as a specific node
#     # It defaults to the identity function, but if you
#     # want to use a node named something else apart from "tools",
#     # You can update the value of the dictionary to something else
#     # e.g., "tools": "my_tools"
#     {"tools": "tools", END: END},
# )

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)

# Any time a tool is called, we return to the chatbot to decide the next step
graph_builder.add_edge("tools", "chatbot")
graph_builder.set_entry_point("chatbot")
graph = graph_builder.compile()

st.image(graph.get_graph().draw_mermaid_png())


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
   