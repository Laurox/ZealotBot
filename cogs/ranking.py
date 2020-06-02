import discord
from discord.ext import commands, tasks
import leaderboard
from os import path
import sqlite3
import average

channel_id = 714549273429016650


class Ranking(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.update_values.start()

    @commands.command()
    @commands.has_role('Admin')
    async def skills(self, ctx, i=10):
        """Lists n player sorted by total skill xp"""

        await ctx.send("```\n" + leaderboard.out_slayer_top(i) + "```")

    @commands.command()
    @commands.has_role('Admin')
    async def slayers(self, ctx, i=10):
        """Lists n player sorted by total slayer xp"""
        await ctx.send("```\n" + leaderboard.out_slayer_top(i) + "```")

    @commands.command()
    @commands.has_role('Admin')
    async def top(self, ctx, i=10, skill=None):
        """Shows Total Leaderboards"""
        if skill is not None:
            skill = str(skill).lower()
        basepath = path.dirname(__file__)
        filepath = path.realpath(path.join(basepath, "..", "db", "timestamp.txt"))
        with open(filepath, 'r') as file:
            timestamp = file.readline()
        if skill is None:
            embed = self.generate_embed(i=i, timestamp=timestamp)
            await ctx.send(embed=embed)
        elif skill is 'foraging' or 'farming' or 'taming' or 'enchanting' or 'mining' or 'alchemy' or 'fishing' or 'combat':
            filepath = path.realpath(path.join(basepath, "..", "db", "mtg.db"))
            conn = sqlite3.connect(filepath)
            c = conn.cursor()
            if skill == 'farming':
                result = c.execute("""SELECT uuid, farming_xp FROM user_info ORDER BY farming_xp DESC""").fetchmany(i)
            elif skill == 'foraging':
                result = c.execute("""SELECT uuid, foraging_xp FROM user_info ORDER BY foraging_xp DESC""").fetchmany(i)
            elif skill == 'combat':
                result = c.execute("""SELECT uuid, combat_xp FROM user_info ORDER BY combat_xp DESC""", ).fetchmany(i)
            elif skill == 'mining':
                result = c.execute("""SELECT uuid, mining_xp FROM user_info ORDER BY mining_xp DESC""").fetchmany(i)
            elif skill == 'taming':
                result = c.execute("""SELECT uuid, taming_xp FROM user_info ORDER BY taming_xp DESC""").fetchmany(i)
            elif skill == 'enchanting':
                result = c.execute("""SELECT uuid, enchanting_xp FROM user_info ORDER BY enchanting_xp DESC""").fetchmany(i)
            elif skill == 'alchemy':
                result = c.execute("""SELECT uuid, alchemy_xp FROM user_info ORDER BY alchemy_xp DESC""").fetchmany(i)
            elif skill == 'fishing':
                result = c.execute("""SELECT uuid, fishing_xp FROM user_info ORDER BY fishing_xp DESC""").fetchmany(i)
            else:
                print("Fehler!")
            conn.commit()
            conn.close()
            embed = self.generate_skill_embed(skill.capitalize(), result, i, timestamp=timestamp)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Invalid Command Arguments")

    @tasks.loop(minutes=60.0)
    async def update_values(self):
        channel = self.bot.get_channel(channel_id)
        basepath = path.dirname(__file__)
        filepath = path.realpath(path.join(basepath, "..", "db", "timestamp.txt"))
        with open(filepath, 'r') as file:
            timestamp = file.readline()
        e = self.generate_embed(timestamp=timestamp)
        await channel.send(embed=e)

    def cog_unload(self):
        self.update_values.cancel()

    @update_values.before_loop
    async def before_printer(self):
        await self.bot.wait_until_ready()

    @staticmethod
    def generate_embed(i=10, timestamp="NONE"):
        embed = discord.Embed(title="Leaderboards",
                              description=f"```Zeigt die Top #{i} Spieler in unserer Gilde in Total Skill- und Slayer-XP\n\n" + average.get_averages() + "```",
                              color=0x0080ff)
        embed.add_field(name="Skills Leaderboard", value="```yaml\n" + leaderboard.out_skill_top(i) + "```", inline=True)
        embed.add_field(name="Slayer Leaderboard", value="```yaml\n" + leaderboard.out_slayer_top(i) + "```", inline=True)
        embed.set_footer(text="Zuletzt aktualisiert: " + str(timestamp))
        return embed

    @staticmethod
    def generate_skill_embed(skill, result, i, timestamp="NONE"):
        embed = discord.Embed(title="Leaderboards",
                              description=f"```Zeigt die Top #{i} Spieler in unserer Gilde in {skill}```",
                              color=0x0080ff)
        embed.add_field(name=f"{skill} Leaderboard", value="```yaml\n" + leaderboard.out_specific_skill(result) + "```", inline=True)
        embed.set_footer(text="Zuletzt aktualisiert: " + str(timestamp))
        return embed


def setup(bot):
    bot.add_cog(Ranking(bot))
