# ZealotBot for MTG Guild
import discord
import logging
import os
from discord.ext import commands
from dotenv import load_dotenv


def get_prefix(client, message):
    return "z "


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
client = commands.Bot(command_prefix=get_prefix)

load_dotenv()
token = os.getenv('DISCORD_TOKEN')


# loads the bot
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.dnd, activity=discord.Game('Hypixel Skyblock'))


# returns the user ping
@client.command()
async def ping(ctx):
    """PONG!"""
    await ctx.message.add_reaction('\U00002705')
    await ctx.send(f"Pong! {round(client.latency * 1000)} ms")


# loads a module
@client.command()
@commands.is_owner()
async def load(ctx, extension):
    """Loads a module"""
    await ctx.message.add_reaction('\U00002705')
    client.load_extension(f'cogs.{extension.lower()}')
    await ctx.send(f"{extension} geladen")


# unloads a module
@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    """Unloads a module"""
    await ctx.message.add_reaction('\U00002705')
    client.unload_extension(f'cogs.{extension.lower()}')
    await ctx.send(f"{extension} entladen")


# shutdowns the command
@client.command()
@commands.is_owner()
async def shutdown(ctx):
    """Shutdowns the Bot"""
    await ctx.message.add_reaction('\U00002705')
    await ctx.send("Heruntergefahren")
    await client.logout()


# loads all modules at start
for filename in os.listdir('./cogs'):
    if filename.endswith(".py"):
        if not filename.startswith('test'):
            if filename.endswith('.py'):
                client.load_extension(f'cogs.{filename[:-3]}')
                print(filename[:-3] + ' aktiviert')
            elif filename.endswith('__pycache__'):
                print('Py-Cache gefunden')
            else:
                print(F'{filename}' + ' ist fehlerhaft')
    else:
        pass


print(f"loading bot using token: {token}")
client.run(token)
