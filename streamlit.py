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
            if not result:
                st.info("No listings found.")
            else:
                st.success("Results found:")
                for line in result.split("\n"):
                    if line.strip() == "":
                        continue
                    if "http" in line:
                        st.markdown(f"[🔗 View Listing]({line})")
                    else:
                        st.markdown(f"**{line}**")
        except Exception as e:
            st.error(f"⚠️ Error: {e}")
