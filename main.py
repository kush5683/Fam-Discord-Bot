import discord
from discord.ext import commands
import os
import threading
from dotenv import load_dotenv
import asyncio
load_dotenv()
version = "Build 4.0"


TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents)
client.remove_command('help')


@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')


# if __name__ == '__main__':
#     threads = []
#     for filename in os.listdir("cogs"):
#         if filename.endswith('.py'):
#             print(f'loading {filename}')
#             t = threading.Thread(
#                 client.load_extension(f'cogs.{filename[:-3]}'))
#             threads.append(t)
#     for thread in threads:
#         thread.start()
#     for thread in threads:
#         thread.join()
#     client.run(TOKEN)
    
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    tasks = []
    for filename in os.listdir("cogs"):
        if filename.endswith('.py'):
            print(f'loading {filename}')
            task = loop.create_task(client.load_extension(f'cogs.{filename[:-3]}'))
            tasks.append(task)
    loop.run_until_complete(asyncio.gather(*tasks))
    client.run(TOKEN)
