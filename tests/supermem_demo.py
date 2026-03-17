from agent import Agent
from google import genai
from dotenv import load_dotenv

load_dotenv()

from supermemory import Supermemory
user_id = "suket"

client = genai.Client(
    vertexai=True,
    project="agentdevelopment-490218",
    location="us-central1",
)

mem_client = Supermemory()

agent = Agent(
    client = client,
    system = "You are a helpful personal AI Assitant, catering to everything the user requires.",
)

while(True):
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    profile = mem_client.profile(container_tag=user_id, q=(agent.messages[-1].parts[0].text if agent.messages else "GENERAL OVERVIEW"))
    static = "\n".join(profile.profile.static)
    dynamic = "\n".join(profile.profile.dynamic)
    memories = "\n".join(r.get("memory", "") for r in profile.search_results.results) 
    print(f"STATIC MEMORY: {static}")
    print(f"DYNAMIC MEMORY: {dynamic}")
    print(f"MEMORIES: {memories}")
    context = f"""
    Static profile:
    {static}
    Dynamic profile:
    {dynamic}
    Relevant memories:
    {memories}
    """
    agent(f"USER CONTEXT: {context}, USER QUERY: {user_input}")
    mem_client.add(
        content="\n".join(f"{m.role}: {m.parts[0].text if m.parts[0].text else ''}" for m in agent.messages[-2:]),
        container_tag=user_id,
    )


