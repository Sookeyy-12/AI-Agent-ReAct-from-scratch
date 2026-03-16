class Agent:
    def __init__(self, client, system):
        self.client = client
        self.system = system
        self.messages = [] # list of messages 
        
        if self.system is not None:
            self.messages.append({"role": "system", "content": self.system})

    def __call__(self, message=""):
        if message:
            self.messages.append({"role": "user", "content": message})
        
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result

    def execute(self):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=self.messages,
        )
        return response.text