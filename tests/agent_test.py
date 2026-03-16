from agent.agent import Agent
from google import genai

system_prompt = open("system_prompt.txt", "r").read().strip()

client = genai.Client(
    vertexai=True,
    project="agentdevelopment-490218",
    location="us-central1",
)

astro = Agent(client, system_prompt)

response = astro("What is the mass of Earth time 10?")
print(response)

response = astro("5.972e+24")
print(response)

response = astro("5.972e+25")
print(response)

print(astro.messages)