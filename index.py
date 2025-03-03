import streamlit as st


if 'TestConfigs' not in st.session_state:
    st.session_state.TestConfigs = {
        "KnowledgeEntityExtraction": {
            "Temperature": 25,
            "Threshold": 25,
            "Domain": "c4",
            "DomainIndex": 0,
            "DomainLabels": ["c4", "arXiv", "stackExchange"]
        },
        "TestingQueryGeneration": {
            "Temperature": 25,
            "NumberOfQuery": 0,
        },
        "KnowledgeGraphConstruction": {
            "Temperature": 25
        }
    }

# if 'KnowledgeEntityExtractionTemperature' not in st.session_state:
#    st.session_state.KnowledgeEntityExtractionTemperature = 25

pg = st.navigation([
    st.Page("./pages/chat.py", title="Chat", icon=":material/speaker_notes:"), 
    st.Page("./pages/settings.py", title="Settings", icon=":material/settings:")
])

pg.run()