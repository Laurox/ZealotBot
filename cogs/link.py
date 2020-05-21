from discord.ext import commands
from uuid_util import get_uuid_from_name
import json
import discord
import requests

# basic structure
data = {}
data['member'] = []


class IngameLink(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role('Admin')
    async def link(self, ctx, name):
        """Verknüpft deinen Minecraft Account mit dem Discord Account"""
        # get current file data
        with open('data/ingame_link.json', 'r') as infile:
            data = json.load(infile)

        uuid = get_uuid_from_name(name)
        if uuid is not None:
            "Move to Own File with Error Handling"
            hypixel_data = requests.get('https://api.hypixel.net/player?key=1d017c26-5792-4765-818f-f0de300df3b4&name=' + name)
            profiles = hypixel_data.json()['player']['stats']['SkyBlock']['profiles']

            # json pattern
            data['member'].append({
                'uuid': uuid,
                'info': {
                    'discord_id': ctx.author.id,
                    'discord_name': ctx.author.name,
                    'ingame_name': name,
                    'main_profile': None,
                    'skyblock_profiles': profiles
                }
            })

            # save to file
            with open('data/ingame_link.json', 'w') as outfile:
                json.dump(data, outfile)
            await ctx.send("Account erfolgreich gelinkt!")
        else:
            await ctx.send("Ungültiger Name!")

    @commands.command()
    @commands.has_role('Admin')
    async def profile(self, ctx):
        """Zeigt alle verfügbaren Profile an"""
        # get current data
        with open('data/ingame_link.json', 'r') as infile:
            data = json.load(infile)
            # iterate the linked members
            for member in data['member']:
                # find the one which belongs to the discord_id
                if ctx.author.id == member['info']['discord_id']:
                    profiles = member['info']['skyblock_profiles']
                    profileembed = discord.Embed(colour=ctx.author.color, timestamp=ctx.message.created_at)
                    profileembed.set_author(name=f"Profile von: {member['info']['ingame_name']}")
                    count = 1
                    for profile in profiles:
                        profileembed.add_field(name=f'Profil #{count}', value=member['info']['skyblock_profiles'][profile]['cute_name'])
                        count += 1
                    await ctx.send(embed=profileembed)
                    return
            await ctx.send("Du musst zuerst deinen Account verlinken!")

    @commands.command()
    @commands.has_role('Admin')
    async def choose(self, ctx, profile_name):
        """Wähle dein Hauptprofil aus"""
        # get current data
        with open('data/ingame_link.json', 'r+') as file:
            data = json.load(file)
            count = 0
            for member in data['member']:
                # find the one which belongs to the discord_id
                if ctx.author.id == member['info']['discord_id']:
                    data['member'][count]['info']['main_profile'] = profile_name  # update value
                    file.seek(0)  # <--- should reset file position to the beginning.
                    json.dump(data, file, indent=4)
                    file.truncate()  # remove remaining part
                    await ctx.send(f"Du hast das Profile {profile_name} als Haupt-Profil gewählt!")
                    return
                else:
                    count += 1
            await ctx.send("Du musst zuerst deinen Account verlinken!")


def setup(bot):
    bot.add_cog(IngameLink(bot))
