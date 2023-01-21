import openai

class Chatbot:
    def __init__(self, model="text-davinci-003"):
        self.currentThread = """The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.
                                Human: Hello, who are you?
                                AI: I am an AI created by OpenAI. How can I help you today?
                                Human: 
                                """
        self.model = model
    
    def send(self, message):
        self.currentThread += f"Human: {message}\n AI:"
        response = openai.Completion.create(
            model=self.model,
            prompt=self.currentThread,
            temperature=0.9,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6,
            stop=[" Human:", " AI:"]
        )
        self.currentThread += f"{response['choices'][0]['text']}"
        return response['choices'][0]['text']
