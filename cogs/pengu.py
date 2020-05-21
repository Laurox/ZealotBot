import random

from discord.ext import commands


class PinguinFakt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def randomstring(self, file):
        return random.choice(open(f"data/{file}.txt").read().splitlines())

    @commands.command()
    async def pinguinfakt(self, ctx):
        await ctx.send(self.randomstring("pinguinfakten"))


def setup(bot):
    bot.add_cog(PinguinFakt(bot))
