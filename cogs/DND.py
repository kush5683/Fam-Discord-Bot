import discord
import random
from discord.ext import commands
import os
import time
import psutil
import datetime
import string


class DND(commands.Cog):
    def __init__(self, client):
        self.client = client
        print("DND commands loaded")

    def checkRole(self, ctx, desiredRole):
        ans = False
        for role in ctx.author.roles:
            if str(role) == desiredRole:
                ans = True
        return ans

    def localRoll(self, ctx, numDie, die):
        dice = [4, 6, 8, 10, 12, 20, 100]
        checkAdmin = self.checkRole(ctx, "Admin")
        if numDie > 40 and checkAdmin == False:
            return "too many dice"
        values = []
        sum = 0
        rolls = 0
        theDie = int(die[1:])
        # d4 d6 d8 d10 d12 d20 d100
        if theDie in dice:
            while rolls < numDie:
                roll = random.randint(1, theDie)
                sum += roll
                values.append(roll)
                rolls += 1
        else:
            return "Something went wrong"
        if(sum == 20 and theDie == 20 and numDie == 1):
            return ('Nat 20', values)
        if(sum == 1):
            return ('Crit Fail', values)
        return (sum, values)

    @commands.command()
    async def roll(self, ctx, die='d20', numDie=1):
        tup = self.localRoll(ctx, int(numDie), die)

        if ctx.channel.topic == 'general chat':

            await ctx.send(f'This action is not allowed in {ctx.channel}')
        elif tup == "too many dice" or tup == "Something went wrong":
            await ctx.send(tup)
        else:
            await ctx.send(f' {ctx.author.display_name} rolled {tup[0]} from {numDie} {die} \n{tup[1]}')

    @commands.command()
    async def zoom(self,ctx):
        link = 'https://wpi.zoom.us/j/8394497794'
        await ctx.send(f'{link}')


def setup(client):
    client.add_cog(DND(client))


if __name__ == '__main__':
    os.system('python3 main.py')
