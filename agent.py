from langchain.agents.initialize import initialize_agent
from langchain.agents import Tool
from langchain_community.llms import Ollama
from langchain.agents.agent_types import AgentType
from apart_scrapper import get_avito_flats
from dotenv import load_dotenv
import re
import os

# Load environment variables from .env file
load_dotenv()

# Define a LangChain-compatible wrapper for the tool
def find_flats_wrapper(city: str = "Casablanca", max_price: int = None, min_surface: int = None):
    results = get_avito_flats(city=city, max_price=max_price, min_surface=min_surface)
    return "\n".join([f"{r['title']} | {r['price']} | {r['surface']}m² | {r['price_per_m2']} DH/m²\n{r['link']}" for r in results[:5]])

# Register it as a LangChain tool
tools = [
    Tool(
        name="FindFlats",
        func=find_flats_wrapper,
        description="Useful for finding apartment listings in Morocco. Input should include city name, max_price, min_surface."
    )
]

# Use Mistral model via Ollama (local)
llm = Ollama(model="mistral")

# Initialize agent with ReAct style
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

# Example query
if __name__ == "__main__":
    user_input = "Find me the cheapest flats in Marrakech above 80m² under 1.2 million MAD"
    try:
        response = agent.run(user_input)
        print("\nAI Agent Response:\n")
        print(response)
    except Exception as e:
        print("\n⚠️ Error during Ollama agent execution:")
        print(str(e))
