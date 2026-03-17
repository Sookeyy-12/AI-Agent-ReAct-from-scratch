from google import genai
import re
from agent.agent import Agent
from tools import calculate, get_planet_mass

system_prompt = open("system_prompt.txt", "r").read().strip()

client = genai.Client(
    vertexai=True,
    project="agentdevelopment-490218",
    location="us-central1",
)


def agent_loop(max_iter, system, query):
    agent = Agent(client, system_prompt)
    tools = ['calculate', 'get_planet_mass']
    next_prompt = query
    i = 0
    while i < max_iter:
        i+=1
        result = agent(next_prompt)
        print(result)

        if "PAUSE" in result and "Action" in result:
            action = re.findall(r"Action: ([a-z_]+): (.+)", result, re.IGNORECASE)
            chosen_tool = action[0][0]
            arg = action[0][1]
            if chosen_tool in tools:
                result_tool = eval(f"{chosen_tool}.tool('{arg}')")
                next_prompt = f"Observation: {result_tool}"
            else:
                next_prompt = "Observation: Tool not Found"
            
            print(next_prompt)
        elif "Answer" in result:
            break
        else:
            continue

agent_loop(10, system_prompt, "What is the mass of Earth  and the mass of mercury and what would be their sum?")
