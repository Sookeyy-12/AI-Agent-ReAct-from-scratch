from google import genai
from google.genai import types
from tools import get_planet_mass

get_planet_mass_function = {
    "name": "get_planet_mass",
    "description": "Gets mass of a planet",
    "parameters": {
        "type": "object",
        "properties": {
            "planet": {
                "type": "string",
                "description": "Planet name (e.g., 'Earth')",
            },
        },
        "required": ["planet"],
    },
}

client = genai.Client(
    vertexai=True,
    project="agentdevelopment-490218",
    location="us-central1",
)

tools = types.Tool(function_declarations=[get_planet_mass_function])
config = types.GenerateContentConfig(tools=[tools])

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="What is the mass of Earth?",
    config=config,
)

if response.candidates[0].content.parts[0].function_call:
    # Extract tool call details, it may not be in the first part.
    function_call = response.candidates[0].content.parts[0].function_call
    print(f"Function to call: {function_call.name}")
    print(f"Arguments: {function_call.args}")
    if function_call.name == "get_planet_mass":
        result = get_planet_mass.tool(**function_call.args)
        print(f"Function execution result: {result}")
else:
    print("No function call found in the response.")
    print(response.text)

print(response.text)
