from google import genai

client = genai.Client(
    vertexai=True,
    project="agentdevelopment-490218",
    location="us-central1",
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain what a react ai agent is in a few words."
)
print(response.text)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="What was my last question to you?"
)
print(response.text)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=["How are you?", "What was my last question to you?"]
)
print(response.text)