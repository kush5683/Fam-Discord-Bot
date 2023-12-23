import discord
import random
from discord.ext import commands
import os
import time
import psutil
import datetime
import string


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


async def setup(client):
    await client.add_cog(Siege(client))



if __name__ == '__main__':
    os.system('python3 main.py')
