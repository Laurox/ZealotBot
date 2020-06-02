import discord
from discord.ext import commands


class Welcome(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        neuzugang = discord.utils.get(member.guild.roles, id=711323499117150319)
        spacer_1 = discord.utils.get(member.guild.roles, id=688166848721715263)
        spacer_2 = discord.utils.get(member.guild.roles, id=697084419009282140)
        await member.add_roles(neuzugang)
        await member.add_roles(spacer_1)
        await member.add_roles(spacer_2)


def setup(bot):
    bot.add_cog(Welcome(bot))
