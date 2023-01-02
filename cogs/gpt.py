import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import openai

class GPT(commands.Cog):
    def __init__(self,client):
        self.client = client
        print("GPT commands loaded")
        load_dotenv()
        self.key = os.getenv('OPENAI_API_KEY')

    @commands.command()
    async def fucker(self,ctx,*prompt):
        stiched_prompt = ""
        for p in prompt:
            stiched_prompt += f"{p} "
        openai.api_key = self.key
        #"Fucker is a chatbot that reluctantly answers questions with sarcastic responses and swears abundently and calls everyone a cuntstick:\n\nYou:{prompt}",
        response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Fucker is a highly intelligent chat but but with a very vulgar attitude.\n\nYou:{stiched_prompt}",
        temperature=0.5,
        max_tokens=60,
        top_p=0.3,
        frequency_penalty=0.5,
        presence_penalty=0.0
        )
        await ctx.send(f"```{response['choices'][0]['text']}```")
    
    @commands.command()
    async def helper(self,ctx,*prompt):
        stiched_prompt = ""
        for p in prompt:
            stiched_prompt += f"{p} "
        response = openai.Completion.create(
        model="text-davinci-003",
        prompt= f"Human:{stiched_prompt}",
        temperature=0.9,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
        )

        await ctx.send(f"```{response['choices'][0]['text']}```")

    @commands.command()
    async def coder(self, ctx, *prompt):
        stiched_prompt = ""
        for p in prompt:
            stiched_prompt += f"{p} "
        response = openai.Completion.create(
        model="code-davinci-002",
        prompt=stiched_prompt,
        temperature=0,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )

        answer = response['choices'][0]['text'].replace("```","")
        await ctx.send(f"```{answer}```")

def setup(client):
    client.add_cog(GPT(client))
