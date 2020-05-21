import discord
import operator
import asyncio
from discord.ext import commands

default_id = 697073966635810886
MAX = 5


class Splash(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.time_left = 30
        self.active_ctx = None
        self.active_message = None
        self.active = False

        self.foraging = 0
        self.farming = 0
        self.combat = 0
        self.fishing = 0
        self.early_winner = None

    channel_id = None
    role_id = None

    @commands.command()
    @commands.has_role('Splasher')
    async def rq(self, ctx):
        """Stellt eine Anfrage für einen Splash"""
        # Checks if another request is active right now
        if self.active:
            await ctx.send("Another Vote is currently active, wait for it to end before starting another!",
                           delete_after=60)
            return

        self.active_ctx = ctx
        embed = self.create_embed(ctx, self.time_left)

        # Changes Active to True and process request
        self.active = True

        # todo add channel support
        # using channel ID and default Channel
        channel = self.bot.get_channel(default_id)
        self.active_message = await channel.send("<@&697074938820952104> | Ein neuer Skill-XP Splash wurde angekündigt!", embed=embed)
        await self.active_message.add_reaction('🌲')
        await self.active_message.add_reaction('🌾')
        await self.active_message.add_reaction('🗡️')
        await self.active_message.add_reaction('🎣')
        await self.update(5)

    async def update(self, waiting_time: int):
        # initial waiting period
        await asyncio.sleep(waiting_time)

        # loop for 5 min
        while True:
            if self.time_left <= 0:
                if self.early_winner is None:
                    m = self.find_max()
                    m = m[0] if m[1] > 0 else 'Invalid'
                    embed = self.create_embed(self.active_ctx, "Over", won=m)
                    await self.active_message.edit(embed=embed)
                else:
                    embed = self.create_embed(self.active_ctx, "Over", won=self.early_winner)
                    await self.active_message.edit(embed=embed)
                self.reset()
                break
            else:
                self.time_left -= 5
                embed = self.create_embed(self.active_ctx, str(self.time_left) + ' Sekunden')
                await self.active_message.edit(embed=embed)
                await asyncio.sleep(waiting_time)

    def reset(self):
        self.active_ctx = None
        self.active_message = None
        self.early_winner = None
        self.time_left = 30
        self.active = False
        self.foraging = 0
        self.farming = 0
        self.combat = 0
        self.fishing = 0

    @staticmethod
    def create_embed(ctx, time_left, **kwargs):
        splashrq = discord.Embed(title=f"Splash Request von {ctx.author.name}",
                                 description="Vote für einen der folgenden XP Potions innerhalb der nächsten 5 Minuten. ```Foraging - 🌲``` ```Farming  - 🌾``` ```Combat   - 🗡️``` ```Fishing  - 🎣```",
                                 color=0xff8040)
        splashrq.set_footer(text=f'Angefragt von {ctx.author}', icon_url=ctx.author.avatar_url)
        splashrq.add_field(name="Verbleibende Zeit ⏰", value=str(time_left), inline=False)
        won = kwargs.get('won', None)
        if won is None:
            splashrq.add_field(name="Welcher Pot?", value="Ausstehend", inline=False)
        else:
            splashrq.add_field(name="Welcher Pot?", value=str(won), inline=False)
        return splashrq

    def evaluate(self):
        if self.foraging >= MAX:
            return "Foraging"
        elif self.farming >= MAX:
            return "Farming"
        elif self.combat >= MAX:
            return "Combat"
        elif self.fishing >= MAX:
            return "Fishing"
        else:
            return -1

    def find_max(self):
        votes = {'Foraging': self.foraging, 'Farming': self.farming, 'Combat': self.combat, 'Fishing': self.fishing}
        return max(votes.items(), key=operator.itemgetter(1))

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)

        if member == guild.me:
            return

        if self.active_message is None:
            return

        # todo adding user id check
        if payload.message_id == self.active_message.id and payload.emoji.name == '🌲':
            self.foraging += 1
        elif payload.message_id == self.active_message.id and payload.emoji.name == '🌾':
            self.farming += 1
        elif payload.message_id == self.active_message.id and payload.emoji.name == '🗡️':
            self.combat += 1
        elif payload.message_id == self.active_message.id and payload.emoji.name == '🎣':
            self.fishing += 1
        else:
            return

        e = self.evaluate()
        if e != -1:
            self.early_winner = e
            self.time_left = 0

    @commands.command()
    @commands.has_role('Admin')
    async def set_splash_channel(self, ctx):
        """Setzt den Channel für RQ"""
        # todo add channel support
        return

    @commands.command()
    @commands.has_role('Admin')
    async def set_splash_ping(self, ctx, role: discord.Role):
        """Setzt die Role für RQ"""
        # todo add channel support
        return


def setup(bot):
    bot.add_cog(Splash(bot))
