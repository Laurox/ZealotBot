from discord.ext import commands
import discord
import json

# basis structure
data = {}
data['reactionroles'] = []


class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active = {}

    @commands.group(invoke_without_command=True)
    @commands.has_permissions(manage_roles=True)
    async def rr(self, ctx):
        """Manages reactionroles"""
        pass

    @rr.command()
    @commands.has_permissions(manage_roles=True)
    async def add(self, ctx, role: discord.Role):
        """Creates a new reactionrole"""

        if ctx.author.top_role <= role:
            await ctx.send("Target role is higher than current highest role.", delete_after=60)
            return

        self.active[ctx.author.id] = role.id
        await ctx.send("React to a message with an emoji to finish the setup.", delete_after=60)

    @rr.command()
    @commands.has_permissions(manage_roles=True)
    async def delete(self, ctx):
        """Deletes a reactionrole"""

        self.active[ctx.author.id] = None
        await ctx.send("React to a message with an emoji to delete a reactionrole.", delete_after=60)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        guild = self.bot.get_guild(payload.guild_id)
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        member = guild.get_member(payload.user_id)

        if member == guild.me:
            return

        if member.id in self.active:
            if self.active[member.id] is None:
                # delete reaction role
                with open('data/reactionroles.json', 'r') as file:
                    data = json.load(file)

                c = 0
                for _ in data['reactionroles']:
                    message_id = data['reactionroles'][c]['data']['message_id']
                    emoji = data['reactionroles'][c]['data']['emoji']
                    if message_id == payload.message_id and emoji == payload.emoji.name:
                        data['reactionroles'].pop(c)
                        break
                    c += 1

                with open('data/reactionroles.json', 'w') as file:
                    json.dump(data, file, indent=4)
                await message.remove_reaction(payload.emoji, guild.me)
            else:
                # add reaction role
                with open('data/reactionroles.json', 'r') as file:
                    data = json.load(file)

                data['reactionroles'].append({
                    'id': len(data['reactionroles']),
                    'data': {
                        'message_id': payload.message_id,
                        'emoji': payload.emoji.name,
                        'role': self.active.get(member.id)
                    }
                })

                with open('data/reactionroles.json', 'w') as file:
                    json.dump(data, file, indent=4)
                await message.add_reaction(payload.emoji)

            await message.remove_reaction(payload.emoji, member)
            self.active.pop(member.id)
            return

        # give player roles
        with open('data/reactionroles.json', 'r') as file:
            data = json.load(file)

            c = 0
            for _ in data['reactionroles']:
                message_id = data['reactionroles'][c]['data']['message_id']
                emoji = data['reactionroles'][c]['data']['emoji']
                if message_id == payload.message_id and emoji == payload.emoji.name:
                    role_id = data['reactionroles'][c]['data']['role']
                    role = discord.utils.get(guild.roles, id=role_id)
                    await member.add_roles(role)
                    await message.remove_reaction(payload.emoji, member)
                    break
                c += 1


def setup(bot):
    bot.add_cog(ReactionRoles(bot))
