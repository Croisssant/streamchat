import streamlit as st

st.session_state.TestConfigs = st.session_state.TestConfigs

st.set_page_config(layout="wide")

st.title(":blue[Testing] Configurations")

st.html("""
    <style>
        [data-testid="stExpander"] details {
            border-style: none;
        }
        div[data-testid="stExpander"] details summary p{
            font-size: 1.2rem;
        }
    </style>
""")

def form_callback():
    # st.session_state.TestConfigs = st.session_state.KnowledgeEntityExtractionTemperature
    st.session_state.TestConfigs = {
        "KnowledgeEntityExtraction": {
            "Temperature": st.session_state.KnowledgeEntityExtractionTemperature,
            "Threshold": st.session_state.KnowledgeEntityExtractionThreshold,
            "DomainLabels": ["c4", "arXiv", "stackExchange"],
            "Domain": st.session_state.KnowledgeEntityExtractionDomain,
            "DomainIndex": st.session_state.TestConfigs["KnowledgeEntityExtraction"]["DomainLabels"].index(st.session_state.KnowledgeEntityExtractionDomain)
        },
        "TestingQueryGeneration": {
            "Temperature": st.session_state.TestingQueryGenerationTemperature,
            "NumberOfQuery": st.session_state.TestingQueryGenerationQuery,
        },
        "KnowledgeGraphConstruction": {
            "Temperature": st.session_state.KnowledgeGraphConstructionTemperature,
        }
    }
    

with st.form(border=True, key="KnowledgeEntityExtractionForm"):
    with st.expander(label="**Knowledge Entity Extraction**", expanded=True):
        col1, col2, col3 = st.columns(3, gap="medium")

        with col1:
            st.slider(
                label="Temperature", 
                min_value=0, 
                max_value=100, 
                value=st.session_state.TestConfigs["KnowledgeEntityExtraction"]["Temperature"], 
                key="KnowledgeEntityExtractionTemperature"
            )

        with col2:
            st.slider(
                label="Threshold", 
                min_value=0, 
                max_value=100, 
                value=st.session_state.TestConfigs["KnowledgeEntityExtraction"]["Threshold"], 
                key="KnowledgeEntityExtractionThreshold"
            )

        with col3:
            st.selectbox(
                label="Domain",
                options=st.session_state.TestConfigs["KnowledgeEntityExtraction"]["DomainLabels"],
                index=st.session_state.TestConfigs["KnowledgeEntityExtraction"]["DomainIndex"],
                placeholder="Select Domain",
                key="KnowledgeEntityExtractionDomain",
            )

    with st.expander(label="**Testing Query Generation**", expanded=True):
        col1, col2, _ = st.columns(3, gap="medium")

        with col1:
            st.slider(
                label="Temperature", 
                min_value=0, 
                max_value=100, 
                value=st.session_state.TestConfigs["TestingQueryGeneration"]["Temperature"], 
                key="TestingQueryGenerationTemperature"
            )

        with col2:
            st.number_input(
                label="Number of Query", 
                min_value=0, 
                max_value=250, 
                key="TestingQueryGenerationQuery", 
                value=st.session_state.TestConfigs["TestingQueryGeneration"]["NumberOfQuery"]
            )

    with st.expander(label="**Knowledge Graph Construction**", expanded=True):
        col1, col2, _ = st.columns(3, gap="medium")

        with col1:
            st.slider(
                label="Temperature", 
                min_value=0, 
                max_value=100, 
                value=st.session_state.TestConfigs["KnowledgeGraphConstruction"]["Temperature"], 
                key="KnowledgeGraphConstructionTemperature"
            )

    _, col2, _ = st.columns(3, gap="medium")
    with col2:
        submitted = st.form_submit_button("Load", type="primary", use_container_width=True, on_click=form_callback)

st.title(":blue[Testing] Metrics")
st.title(st.session_state.KnowledgeEntityExtractionTemperature)