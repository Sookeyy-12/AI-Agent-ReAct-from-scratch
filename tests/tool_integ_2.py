from google import genai
from google.genai import types
# from tools.get_planet_mass import get_planet_mass
from tools import get_planet_mass

contents = []

client = genai.Client(
    vertexai=True,
    project="agentdevelopment-490218",
    location="us-central1",
)

tools = types.Tool(function_declarations=[get_planet_mass.definition])
config = types.GenerateContentConfig(tools=[tools])

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="What is the mass of Earth?",
    config=config,
)

# Extract tool call details, it may not be in the first part.
tool_call = response.candidates[0].content.parts[0].function_call
if tool_call.name == "get_planet_mass":
    result = get_planet_mass.tool(**tool_call.args)
    print(f"Function execution result: {result}")

# Create a function response part
function_response_part = types.Part.from_function_response(
    name=tool_call.name,
    response={"result": result},
)

contents.append(response.candidates[0].content) # Append the content from the model's response.
print("*"*50)
print(response.candidates[0].content)
print("*"*50)


contents.append(types.Content(role="user", parts=[function_response_part])) # Append the function response

final_response = client.models.generate_content(
    model="gemini-2.5-flash",
    config=config,
    contents=contents,
)

print(final_response.text)
