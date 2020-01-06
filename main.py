# ZealotBot for MTG Guild
import discord
import logging
import os
from discord.ext import commands
from dotenv import load_dotenv
import json


def get_prefix(client, message):
    return "!"


def botowner(ctx):
    return ctx.author.id == 147090693725093888


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
client = commands.Bot(command_prefix=get_prefix)

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

date = "11. Januar"
time = "20:00"


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
@commands.check(botowner)
async def load(ctx, extension):
    """Loads a module"""
    await ctx.message.add_reaction('\U00002705')
    client.load_extension(f'cogs.{extension.lower()}')
    await ctx.send(f"{extension} geladen")


# unloads a module
@client.command()
@commands.check(botowner)
async def unload(ctx, extension):
    """Unloads a module"""
    await ctx.message.add_reaction('\U00002705')
    client.unload_extension(f'cogs.{extension.lower()}')
    await ctx.send(f"{extension} entladen")


# shutdowns the command
@client.command()
@commands.check(botowner)
async def shutdown(ctx):
    """Shutdowns the Bot"""
    await ctx.message.add_reaction('\U00002705')
    await ctx.send("Heruntergefahren")
    await client.logout()


# returns the user ping
@client.command()
async def announce(ctx):
    """Kündigt einen Dragon-Fight an"""
    message = await ctx.send(
        f"@everyone: Der nächste Dragon-Raid findet am {date} um {time} statt! Durch drücken auf \U00002705 oder \U0000274C unter der Nachricht, meldest du dich an oder ab.\nWenn ihr Augen habt reagiert bitte mit der entsprechenden Zahl oder mit dem Stern, wenn ihr mehr als 8 setzten wollt"
    )

    emojis = [
        # ACCEPT
        '\U00002705',
        # DECLINE
        '\U0000274C',
        # NUMS
        '\U00000031\U0000FE0F\U000020E3',
        '\U00000032\U0000FE0F\U000020E3',
        '\U00000033\U0000FE0F\U000020E3',
        '\U00000034\U0000FE0F\U000020E3',
        '\U00000035\U0000FE0F\U000020E3',
        '\U00000036\U0000FE0F\U000020E3',
        '\U00000037\U0000FE0F\U000020E3',
        '\U00000038\U0000FE0F\U000020E3',
        # STAR
        '\U0000002A\U0000FE0F\U000020E3'
    ]

    for emoji in emojis:
        await message.add_reaction(emoji)

    with open(f"./data/registered.json", "w") as file:
        data = {}
        json.dump(data, file, indent=4)

    with open(f"./data/declined.json", "w") as file:
        data = {}
        json.dump(data, file, indent=4)


# manages reactions for
# dragon-raids (ch_id = 653269648862609409)
@client.event
async def on_raw_reaction_add(payload):
    if payload.channel_id != 653269648862609409:
        return
    if payload.user_id == client.user.id:
        return

    channel = await client.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    if message.author != client.user:
        return

    user = await client.fetch_user(payload.user_id)
    if payload.emoji.name == '\U00002705':
        with open(f"./data/registered.json", "r") as file:
            users = json.load(file)

        users[str(user.id)] = str(user.display_name)

        with open(f"./data/registered.json", "w") as file:
            json.dump(users, file, indent=4)

        await user.send(content=f"Du hast dich erfolgreich für den Dragon-Raid am {date} um {time} angemeldet!")
    elif payload.emoji.name == '\U0000274C':
        with open(f"./data/declined.json", "r") as file:
            users = json.load(file)

        users[str(user.id)] = str(user.display_name)

        with open(f"./data/declined.json", "w") as file:
            json.dump(users, file, indent=4)

        await user.send(content=f"Du hast dich erfolgreich für den Dragon-Raid am {date} um {time} abgemeldet!")
    elif payload.emoji.name == '\U00000031\U0000FE0F\U000020E3':
        await add_eyes(1, user)
    elif payload.emoji.name == '\U00000032\U0000FE0F\U000020E3':
        await add_eyes(2, user)
    elif payload.emoji.name == '\U00000033\U0000FE0F\U000020E3':
        await add_eyes(3, user)
    elif payload.emoji.name == '\U00000034\U0000FE0F\U000020E3':
        await add_eyes(4, user)
    elif payload.emoji.name == '\U00000035\U0000FE0F\U000020E3':
        await add_eyes(5, user)
    elif payload.emoji.name == '\U00000036\U0000FE0F\U000020E3':
        await add_eyes(6, user)
    elif payload.emoji.name == '\U00000037\U0000FE0F\U000020E3':
        await add_eyes(7, user)
    elif payload.emoji.name == '\U00000038\U0000FE0F\U000020E3':
        await add_eyes(8, user)
    elif payload.emoji.name == '\U0000002A\U0000FE0F\U000020E3':
        await add_eyes("+", user)


async def add_eyes(num, user):
    with open(f"./data/registered.json", "r") as file:
        users = json.load(file)

    if str(user.id) not in users:
        await user.send(content=f"Du musst dich dafür zuerst registrieren! Reagiere dazu auf \U00002705")
        return False
    else:
        users[str(user.id)] = str([users[str(user.id)], num])

        with open(f"./data/registered.json", "w") as file:
            json.dump(users, file, indent=4)

        await user.send(content=f"Du hast erfolgreich {num} Auge eingetragen.")
    return True


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
