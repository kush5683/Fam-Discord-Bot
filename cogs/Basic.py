import discord
import random
from discord.ext import commands
import os
import time
import psutil
import datetime
import string


class Basic(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.version = '4.0'
        self.processID = psutil.Process(os.getpid())
        print("Basic commands loaded")

    def helpEmbed(self):
        embed = discord.Embed(
            color=discord.Colour.orange(),
            title='Help'
        )
        embed.add_field(name='!help', value='This message', inline=False)
        embed.add_field(name='!ping', value='Returns Pong!', inline=False)
        # embed.add_field(name='!roll', value='Takes in [d4, d6, d8, d10, d12, d20, d100] followed by a number <10 [1 if not specified] and returns the value rolled', inline=False)
        # embed.add_field(name='!roles', value='Returns Your roles', inline=False)
        # embed.add_field(name='!poop', value='Returns poopy', inline=False)
        # embed.add_field(name='!unshitmypants',value='Does the thing', inline=False)
        embed.add_field(
            name='!flip', value='Flips a coin (Heads or Tails)', inline=False)
        embed.add_field(
            name='!clear', value='Takes an integer value as input or 100 if none is supplied, will clear n messages', inline=False)
        # embed.add_field(name='!statusreport',value='reports status', inline=False)

        return embed

    def getBotStat(self):
        sendTo = ''
        text_channel_list = []
        for guild in self.client.guilds:
            for channel in guild.text_channels:
                text_channel_list.append(channel)
        for channel in text_channel_list:
            if(channel.name == 'bot-status'):
                sendTo = channel
        return sendTo

    def checkRole(self, ctx, desiredRole):
        ans = False
        for role in ctx.author.roles:
            if str(role) == desiredRole:
                ans = True
        return ans

    @commands.Cog.listener()
    async def on_ready(self):
        self.up = time.strftime("%Y-%m-%d %H:%M:%S",
                                time.localtime(self.processID.create_time()))
        os.system('clear')
        print(self.version)
        channel = self.getBotStat()
        await channel.purge(limit=100)
        await channel.send(f'I have arrived with version {self.version} loaded')
        await channel.send(embed=self.helpEmbed())
        await channel.send(f'Boot time:{self.up}')

    @commands.Cog.listener()
    async def on_message(self, message):
        print(
            f"{message.channel}: {message.author}: {message.author.name}: {message.content}")
        text = []
        for str in message.content.upper().split():
            text.append(str.translate(
                str.maketrans('', '', string.punctuation)))
        for x in text:

            if (x == 'BOT' or x == message.guild.me.display_name.upper()) and (message.author.display_name != message.guild.me.display_name):
                await message.channel.send(f'I am the {message.guild.me.display_name}!')

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong!')

    @commands.command()
    async def help(self, ctx):
        await ctx.channel.send(embed=self.helpEmbed())

    @commands.command()
    async def flip(self, ctx):
        coin = ['Heads', 'Tails']
        result = random.choice(coin)
        await ctx.send(result)

    @commands.command()
    async def shutdown(self, ctx):
        if ctx.message.author.id == 336296609694351361:  # replace OWNERID with your user id
            print("shutdown")
            try:
                await self.client.logout()
            except:
                print("EnvironmentError")
                self.client.clear()
        else:
            await ctx.send("You do not own this bot!")

    @commands.command()
    async def clear(self, ctx, amount=100):
        admin = self.checkRole(ctx, 'Admin')
        if admin:
            await ctx.channel.purge(limit=amount)
            await ctx.send(f'Cleared by {ctx.author.display_name}')
        else:
            await ctx.send(f'Only Admin can perform this task')

    @commands.command()
    async def repeat(self, ctx, message, amount=1):
        if(self.checkRole(ctx, 'Admin')):
            count = 0
            send = ''
            while count < amount:
                send += (message + ' ')
                count += 1
            await ctx.send(send)
        else:
            await ctx.send('This fun command is only for Admins sorry :(')

    @commands.command()
    async def statusreport(self, ctx):
        subject = random.choice(ctx.guild.members)
        report = discord.Embed(
            color=discord.Colour.dark_red(),
            title='STATUS REPORT'
        )
        report.add_field(
            name='Status:', value=f'{subject.status}', inline=False)
        report.add_field(name=f'{subject.display_name}:',
                         value='Still poopy', inline=False)

        report.add_field(
            name='Next: ', value='Will update when status changes', inline=False)
        await ctx.send(embed=report)

    @commands.command()
    async def poop(self, ctx):
        # print(f'{ctx.author.name.upper()}')
        if('KUSH' not in ctx.author.name.upper()):
            await ctx.send(f'{ctx.author.display_name} is poopy')
        else:
            await ctx.send('Keith is a poopy head')

    @commands.command()
    async def unshitmypants(self, ctx):
        await ctx.send(file=discord.File('assets/poopPants.jpg'))


def setup(client):
    client.add_cog(Basic(client))


if __name__ == '__main__':
    os.system('python3 main.py')
