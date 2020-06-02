import requests
import util.uuid_util
import leaderboard
import util.converter
import time
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('API_TOKEN')
rq = requests.get("https://api.hypixel.net/guild?key=" + token + "&id=5d2e186677ce8415c3fd0074")

c = 0
for member in rq.json()['guild']['members']:
    try:
        name = util.uuid_util.get_name_from_uuid(member['uuid'])
        profile = leaderboard.get_current_profile(member['uuid'])

        souls = profile['fairy_souls_collected']

        farming_xp = profile['experience_skill_farming']
        combat_xp = profile['experience_skill_combat']
        foraging_xp = profile['experience_skill_foraging']
        mining_xp = profile['experience_skill_mining']
        fishing_xp = profile['experience_skill_fishing']
        taming_xp = profile['experience_skill_taming']
        alchemy_xp = profile['experience_skill_alchemy']
        enchanting_xp = profile['experience_skill_enchanting']

        total_xp = farming_xp + combat_xp + foraging_xp + mining_xp + fishing_xp + taming_xp + alchemy_xp + enchanting_xp
        average_xp = total_xp / 8

        farming_lvl = util.converter.skill_exp_to_level(farming_xp)
        combat_lvl = util.converter.skill_exp_to_level(combat_xp)
        foraging_lvl = util.converter.skill_exp_to_level(foraging_xp)
        mining_lvl = util.converter.skill_exp_to_level(mining_xp)
        fishing_lvl = util.converter.skill_exp_to_level(fishing_xp)
        taming_lvl = util.converter.skill_exp_to_level(taming_xp)
        alchemy_lvl = util.converter.skill_exp_to_level(alchemy_xp)
        enchanting_lvl = util.converter.skill_exp_to_level(enchanting_xp)

        total_level = farming_lvl + combat_lvl + foraging_lvl + mining_lvl + fishing_xp + taming_lvl + alchemy_xp + enchanting_lvl
        average_lvl = total_level / 8

        revenant_xp = profile['slayer_bosses']['zombie']['xp']
        tarantula_xp = profile['slayer_bosses']['spider']['xp']
        sven_xp = profile['slayer_bosses']['wolf']['xp']

        total_slayer_xp = revenant_xp + tarantula_xp + sven_xp
        average_slayer_xp = total_slayer_xp / 3

        revenant_lvl = util.converter.slayer_exp_to_level(revenant_xp)
        tarantula_lvl = util.converter.slayer_exp_to_level(tarantula_xp)
        sven_lvl = util.converter.slayer_exp_to_level(sven_xp)

        total_slayer_level = revenant_xp + tarantula_lvl + sven_lvl
        average_skayer_lvl = total_level / 3

        # if not (souls >= 190):
        #    print(name + " kennt TimeDeo nicht")
        # elif not (average_lvl >= 20.0):
        #     print(name + " ist sehr schlecht")
        # elif not (total_slayer_level >= 13):
        #     print(name + " selbst P2Go ist besser")
        # elif not (sven_lvl >= 6):
        #     print(name + " wird vom Sven T1 gekillt")
        if not total_xp >= 20000000:
            print(name + " hat kack Skills")
    except:
        print(name + " ist nh bissle dumm")

    time.sleep(1)
