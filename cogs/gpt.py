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
    async def marv(self,ctx,prompt):
        openai.api_key = self.key

        response = openai.Completion.create(
        model="text-davinci-002",
        prompt=f"Marv is a chatbot that reluctantly answers questions with sarcastic responses and swears abundently:\n\nYou:{prompt}",
        temperature=0.5,
        max_tokens=60,
        top_p=0.3,
        frequency_penalty=0.5,
        presence_penalty=0.0
        )
        await ctx.send(response['choices'][0]['text'])
    
    @commands.command()
    async def helper(self,ctx,prompt):
        response = openai.Completion.create(
        model="text-davinci-002",
        prompt= f"Human:{prompt}",
        temperature=0.9,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
        )

        await ctx.send(response['choices'][0]['text'])

def setup(client):
    client.add_cog(GPT(client))
