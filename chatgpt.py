import openai

class Chatbot:
    def __init__(self, model="gpt-3.5-turbo"):
        self.model = model
        self.messages = [
        {"role": "system", "content":"You are a helpful assistant. You take on any behavior asked of you"},
        ]
    
    def send(self, message):
        self.messages.append({"role": "user", "content": f"{message}"})
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages
        )
        message_content = response["choices"][0]["message"]['content']
        self.messages.append({"role": "assistant", "content": message_content})
        return message_content
