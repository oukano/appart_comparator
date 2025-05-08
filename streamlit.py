import streamlit as st
from agent import agent  # make sure agent is initialized in its module

st.set_page_config(page_title="Moroccan Flat Finder", layout="wide")

st.title("🏠 Moroccan Flat Finder")
st.markdown("Ask in natural language to find apartments in Morocco:")

query = st.text_input("Search query", placeholder="e.g. Flats in Tangier under 1M MAD with 2 bedrooms")

if st.button("Find Flats") and query:
    with st.spinner("Searching..."):
        try:
            result = agent.run(query)
            print(result)
            st.success("Results found:")
            st.text(result)
        except Exception as e:
            st.error(f"Error: {e}")
