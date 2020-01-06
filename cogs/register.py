from discord.ext import commands


class Register(commands.Cog):

    def __init__(self, client):
        self.client = client

    def botowner(ctx):
        return ctx.author.id == 147090693725093888

    @commands.command()
    @commands.check(botowner)
    async def list(self, ctx, ext):
        if ext == "register":
            await ctx.message.add_reaction('\U00002705')
            await ctx.send(f"Folgende User haben sich angemeldet:")
            file = open("dragonparty.txt", "r")
            lines = file.readlines()
            for line in lines:
                await ctx.send(line)
            file.close()
        elif ext == "eyes":
            await ctx.message.add_reaction('\U00002705')
            await ctx.send(f"Folgende User haben Eyes:")
            file = open("eyes.txt", "r")
            lines = file.readlines()
            for line in lines:
                await ctx.send(line)
            file.close()
        else:
            await ctx.send("Ungültiger Subcommand - Nutze <register> oder <eyes>")


def setup(client):
    client.add_cog(Register(client))
