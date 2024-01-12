import discord
import random
from discord.ext import commands
import os
import time
import psutil
import datetime
import string
import dotenv
from openai import OpenAI

class Siege(commands.Cog):

    def __init__(self, client):
        self.client = client

        print("Siege commands loaded")

    @commands.command()
    async def roles(self, ctx, team=' '):
        order = []
        if(team[0] == 'a'):
            roles = ['entry', 'drone', 'medic', 'planter', 'tail']
        elif(team[0] == 'd'):
            roles = ['roamer', 'cam', 'medic', 'defuser', 'anchor']
        else:
            roles = ['1', '2', '3', '4', '5']
        while(roles):
            pick = random.choice(roles)
            order.append(pick)
            roles.remove(pick)
        await ctx.send(order)

    @commands.command()
    async def strat(self, ctx, team=None, current_map=None, *notes):
        """
        Use openai to generate strats
        """
        if team is None:
            await ctx.send("Please specify a side [attack, defense]")
            return
        if current_map is None:
            await ctx.send("Please specify a map")
            return
        if team[0] == 'a':
            team = 'attack'
        if team[0] == 'd':
            team = 'defense'
        if team not in ['attack', 'defense']:
            await ctx.send("Please specify a side [attack, defense]")
            return
        print(f"Team: {team}, Map: {current_map}")
        self.messages = [
            {
                "role": "system",
                "content": "You are Siege Strategist, designed to offer fun and humorous strategies for Rainbow Six Siege, inspired by stratroulette.net. Before suggesting a strategy, it will always ask the user which side they are playing on (attackers or defenders) and the specific map they are playing on. This ensures that the strategies are tailored to the actual game scenario. The strategies will be random, unconventional, and focused on creating enjoyable gameplay rather than purely competitive play - but they should not be so ridiculous that winning is impossible, we want to mix it up not just lose immidiatly. The GPT will avoid suggesting strategies that exploit game bugs or glitches, promoting fair play. It will maintain a light-hearted and playful tone, making the gaming experience more entertaining and less serious. If you do not know the map the user tells you then keep that a secret and give a generic strat that could apply to any map.",
            }
        ]
        dotenv.load_dotenv(dotenv_path='../.env')
        openai_api_key = os.getenv('OPEN_KEY')
        self.model = OpenAI(api_key=openai_api_key)
        messages = self.messages
        if notes:
            notes = ' '.join(notes)
        else:
            notes = "none"
        messages.append({
            "role": "user",
            "content": f"We are playing {team} on {current_map}  {notes} - We want the strategy to be fun and unconventional, but not so ridiculous that we will lose immidiatly - we want to maintain a somewhatcompetitive edge. "
        })
        if team[0] == 'a':
            team = "attacker"
        else:
            team = "defender"
        await ctx.send(f"Generating {team} strategy for {current_map} {notes}...")
        response = self.model.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=messages,
        )
        content = response.choices[0].message.content
        while len(content) > 0:
            if len(content) <= 2000:
                await ctx.send(content)
                break
            else:
                await ctx.send(content[:2000])
                content = content[2000:]
        
        


async def setup(client):
    await client.add_cog(Siege(client))



if __name__ == '__main__':
    os.system('python3 main.py')
