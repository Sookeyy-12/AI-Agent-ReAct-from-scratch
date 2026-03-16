class Agent:
    def __init__(self, client, system=None, model="gemini-2.5-flash"):
        self.client = client
        self.system = system
        self.model = model
        self.messages = [] # list of messages 

    def __call__(self, message=""):
        if message:
            self.messages.append({"role": "user", "parts": [{"text": message}]})
        
        result = self.execute()
        self.messages.append({"role": "model", "parts": [{"text": result}]})
        return result

    def execute(self):
        config = {}
        if self.system:
            config["system_instruction"] = self.system

        response = self.client.models.generate_content(
            model=self.model,
            contents=self.messages,
            config=config,
        )
        return response.text