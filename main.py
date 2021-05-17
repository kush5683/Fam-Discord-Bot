import discord
from discord.ext import commands
import os
import threading

version = "Build 4.0"


TOKEN = open('token.txt').readline()

intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents)
client.remove_command('help')


@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')


if __name__ == '__main__':
    threads = []
    for filename in os.listdir("./cogs"):
        if filename.endswith('.py'):
            print(f'loading {filename}')
            t = threading.Thread(
                client.load_extension(f'cogs.{filename[:-3]}'))
            threads.append(t)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    client.run(TOKEN)
