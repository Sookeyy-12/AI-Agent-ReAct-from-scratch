from google import genai
from google.genai import types
from tools import *



class Agent:
    def __init__(self, client, system=None, model="gemini-2.5-flash", given_tools=None):
        self.client = client
        self.system = system
        self.model = model
        self.messages = [] # list of messages 
        self.given_tools = given_tools or []
        self.tools = []
        for tool in self.given_tools:
            self.tools.append(types.Tool(function_declarations=[tool]))
        
        self.config = types.GenerateContentConfig(
            tools=self.tools if self.tools else None,
            system_instruction=self.system
        )

    def __call__(self, message=""):
        if message:
            self.messages.append({"role": "user", "parts": [{"text": message}]})
        
        return self.execute()

    def execute(self):
        response = self.client.models.generate_content(
            model=self.model,
            contents=self.messages,
            config=self.config,
        )
        
        tool_calls = []
        # Log reasoning parts and tool calls
        for part in response.candidates[0].content.parts:
            if part.text:
                print(f"**ASSISTANT**: {part.text.strip()}")
            if part.function_call:
                print(f"**CALLING TOOL**: {part.function_call.name} with {part.function_call.args}")
                tool_calls.append(part.function_call)

        # Keep track of the model's response
        self.messages.append(response.candidates[0].content)
        
        if tool_calls:
            response_parts = [self.execute_tool(tc) for tc in tool_calls]
            self.messages.append(types.Content(role="tool", parts=response_parts))
            return self.execute()
            
        return response.text

    def execute_tool(self, tool_call):
        result = eval(f"{tool_call.name}.tool(**{tool_call.args})")
        print(f"**TOOL RESULT**: {result}")
        return types.Part.from_function_response(
            name=tool_call.name,
            response={"result": result},
        )
