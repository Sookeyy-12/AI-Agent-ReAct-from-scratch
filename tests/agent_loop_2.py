from google import genai
import re
from agent.agent import Agent
from tools import calculate, get_planet_mass

system_prompt = open("system_prompt_2.txt", "r").read().strip()

client = genai.Client(
    vertexai=True,
    project="agentdevelopment-490218",
    location="us-central1",
)

def agent_loop(system, query):
    tools = [calculate.definition, get_planet_mass.definition]
    agent = Agent(client, system, given_tools=tools)
    result = agent(query)
    print(f"\nFinal Result:\n{result}")


agent_loop(system_prompt, "What is the mass of Earth and the mass of mercury and what would be their sum?")
