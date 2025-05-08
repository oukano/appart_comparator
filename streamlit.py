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
                flats = result.split("\n")
                for i in range(0, len(flats), 2):
                    info_line = flats[i].strip() if i < len(flats) else ""
                    link_line = flats[i + 1].strip() if i + 1 < len(flats) else ""
                    if info_line and link_line.startswith("http"):
                        st.markdown(f"**{info_line}**\n\n[🔗 View Listing]({link_line})")
                    elif info_line:
                        st.markdown(f"**{info_line}**")
        except Exception as e:
            st.error(f"⚠️ Error: {e}")

