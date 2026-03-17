from agent import Agent
from google import genai
from tools import get_planet_mass, calculate

system_prompt = open("system_prompt_2.txt", "r").read().strip()

client = genai.Client(
    vertexai=True,
    project="agentdevelopment-490218",
    location="us-central1",
)

agent = Agent(
    client=client,
    system=system_prompt,
    model="gemini-2.5-flash",
    given_tools=[get_planet_mass.definition, calculate.definition]
)

while(True):
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    print("\n" + "*"*50 + "\n")
    agent(user_input)
    print("\n" + "*"*50 + "\n")