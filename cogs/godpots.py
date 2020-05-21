import requests

import discord
from discord.ext import commands

POTIONS = {
    'STRENGTH': ['<:blazerod:711328213158068345>', 'ENCHANTED_BLAZE_ROD', 'KNOCKOFF_COLA'],
    'SPEED': ['<:sugarcane:711328213351268452>', 'ENCHANTED_SUGAR_CANE', 'DECENT_COFFEE'],
    'CRITICAL': ['<:flint:711328213325971456>', 'FLINT', 'SLAYER_ENERGY_DRINK'],
    'ARCHERY': ['<:feather:711328213221113938>', 'FEATHER', 'TUTTI_FRUTTI'],
    'ADRENALINE': ['<:ecookie:711328213195948152>', 'ENCHANTED_COOKIE', 'DECENT_COFFEE'],
    'RABBIT': ['<:rabbitfoot:711328213372239942>', 'ENCHANTED_RABBIT_FOOT', 'DECENT_COFFEE'],
    'AGILITY': ['<:ecake:711328213179170836>', 'ENCHANTED_CAKE', 'DECENT_COFFEE'],
    'EXPERIENCE': ['<:lapis:711328213351006268>', 'LAPIS_LAZULI', 'VIKING_TEAR']
}

NOBASES = {
    'PET_LUCK': ['<:rabbithide:711328213049278535>', 'ENCHANTED_RABBIT_HIDE'],
    'SPIRIT': ['<:waterbottle:711328213267120199>', 'GREEN_CANDY'],
    'MAGIC_FIND': ['<:waterbottle:711328213267120199>', 'GREEN_CANDY'],
    'COMBAT_XP_BOOST': ['<:combat:711328212906409995>', 'COMBAT_XP_BOOST_III']
}

MODIFIER = {
    'REDSTONE': ['<:redstone:711328213351137451>', 'ENCHANTED_REDSTONE_BLOCK'],
    'GLOWSTONE': ['<:glowstone:711328213019656264>', 'ENCHANTED_GLOWSTONE'],
    'LAMP': ['<:lamp:711328213464514590>', 'ENCHANTED_REDSTONE_LAMP'],
    'GUNPOWDER': ['<:gunpowder:711328213271314502>', 'ENCHANTED_GUNPOWDER']
}

AMOUNT = {
    'ENCHANTED_BLAZE_ROD': 1,
    'ENCHANTED_GLOWSTONE': 10,
    'ENCHANTED_REDSTONE_BLOCK': 11,
    'ENCHANTED_REDSTONE_LAMP': 1,
    'ENCHANTED_CAKE': 1,
    'ENCHANTED_COOKIE': 1,
    'FEATHER': 1,
    'FLINT': 1,
    'ENCHANTED_RABBIT_HIDE': 1,
    'ENCHANTED_RABBIT_FOOT': 1,
    'ENCHANTED_GUNPOWDER': 1,
    'ENCHANTED_SUGAR_CANE': 1,
    'GREEN_CANDY': 33,

    'SLAYER_ENERGY_DRINK': 3,
    'TUTTI_FRUTTI': 3,
    'DECENT_COFFEE': 3,
    'VIKING_TEAR': 3,
    'KNOCKOFF_COLA': 3,
    'LAPIS_LAZULI': 1,
    'COMBAT_XP_BOOST_III': 3
}

BAZAAR_LIST = [
    'ENCHANTED_BLAZE_ROD',
    'ENCHANTED_GLOWSTONE',
    'ENCHANTED_REDSTONE_BLOCK',
    'ENCHANTED_REDSTONE_LAMP',
    'ENCHANTED_CAKE',
    'ENCHANTED_COOKIE',
    'FEATHER',
    'FLINT',
    'ENCHANTED_RABBIT_HIDE',
    'ENCHANTED_RABBIT_FOOT',
    'ENCHANTED_GUNPOWDER',
    'ENCHANTED_SUGAR_CANE',
    'GREEN_CANDY'
]

SPLASH_LIST = {
    'SLAYER_ENERGY_DRINK': 10000,  # 3x
    'TUTTI_FRUTTI': 1000,  # 3x
    'DECENT_COFFEE': 5000,  # 12x
    'VIKING_TEAR': 15000,  # 3x
    'KNOCKOFF_COLA': 1500,  # 3x
    'LAPIS_LAZULI': 10,  # 1x
    'COMBAT_XP_BOOST_III': 50000,  # 3x
    'NONE': 0
}

SEAL_OF_THE_FAMILY = {
    'TALISMAN': 0.01,
    'RING': 0.02,
    'ARTIFACT': 0.03
}


def get_price(item_key):
    req = requests.get('https://api.slothpixel.me/api/skyblock/bazaar/' + item_key)
    return int(req.json()['quick_status']['buyPrice'])


def look_up(item_key):
    if BAZAAR_LIST.__contains__(item_key):
        return get_price(item_key)
    elif SPLASH_LIST.__contains__(item_key):
        return SPLASH_LIST[item_key]
    else:
        return -1


class GodPots(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def godpots(self, ctx):
        out_string = "Materials and Prices for 3 Splashes\n\n"
        total_price = 0

        out_string += "__Potions:__ \n\n"
        for potion in POTIONS:
            key = POTIONS[potion][1]
            modifier = POTIONS[potion][2]
            price = look_up(key) * AMOUNT[key] + look_up(modifier) * AMOUNT[modifier]
            total_price += price
            out_string += POTIONS[potion][0] + " " + potion.lower() + " + " + modifier.lower() + ": " + str(price) + "\n"

        for potion in NOBASES:
            key = NOBASES[potion][1]
            price = look_up(key) * AMOUNT[key]
            total_price += price
            out_string += NOBASES[potion][0] + " " + potion.lower() + ": " + str(price) + "\n"

        out_string += "\n__Modifier:__\n\n"
        for modifier in MODIFIER:
            key = MODIFIER[modifier][1]
            price = look_up(key) * AMOUNT[key]
            total_price += price
            out_string += MODIFIER[modifier][0] + " " + modifier.lower() + ": " + str(price) + "\n"

        out_string += f'\nTotal Price: **{total_price}**'

        await ctx.send(out_string)


def setup(bot):
    bot.add_cog(GodPots(bot))
