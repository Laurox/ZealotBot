import sqlite3
import requests
from os import path
from util.uuid_util import get_uuid_from_name
from util.uuid_util import get_name_from_uuid
import locale
import util.converter
from datetime import datetime

last_updated_time = None

if not path.exists('./db/mtg.db'):
    print('creating mtg database...')
    conn = sqlite3.connect('./db/mtg.db')
    c = conn.cursor()
    c.execute("""
            CREATE TABLE user_info (
                discord_id INTEGER, 
                uuid TEXT,
                total_skill_xp REAL,
                total_slayer_xp REAL,

                farming_xp REAL,
                foraging_xp REAL,
                combat_xp REAL,
                mining_xp REAL,
                taming_xp REAL,
                enchanting_xp REAL,
                alchemy_xp REAL,
                fishing_xp REAL,

                revenant_xp INTEGER,
                tarantula_xp INTEGER,
                sven_xp INTEGER)
            """)
    conn.commit()
    conn.close()
    print('Done creating! You can now use mtg.db')


def get_current_profile(uuid: str):
    rq = requests.get(
        'https://api.hypixel.net/skyblock/profiles?key=f987964c-c219-46e4-9625-1593a855e148&uuid=' + uuid).json()
    result = None
    maximum = 0
    for profile in rq['profiles']:
        temp = profile['members'][uuid]
        if 'last_save' not in temp:
            print('FOUND pending invitation... skipping')
            pass
        else:
            millis = temp['last_save']
            if millis > maximum:
                maximum = millis
                result = temp
    return result


def insert_player(discord_id, uuid, profile):
    conn = sqlite3.connect('./db/mtg.db')
    c = conn.cursor()
    if 'experience_skill_farming' not in profile:
        # todo failback behaviour for disabled skills
        print(get_name_from_uuid(uuid) + ' has disabled his Skill Api')
        return
    if 'experience_skill_taming' not in profile:
        print(get_name_from_uuid(uuid) + ' has not logged in after petsV2')
        return
    c.execute("""
                INSERT INTO user_info VALUES (
                    :discord_id, :uuid, :total_skill_xp, :total_slayer_xp,
                    :farming_xp, :foraging_xp, :combat_xp, :mining_xp, :taming_xp, :enchanting_xp, :alchemy_xp, :fishing_xp,
                    :revenant_xp, :tarantula_xp, :sven_xp)
                """,
              {
                  'discord_id': discord_id,
                  'uuid': uuid,
                  'total_skill_xp': profile['experience_skill_farming'] + profile['experience_skill_foraging'] +
                                    profile['experience_skill_combat'] + profile['experience_skill_mining'] + profile[
                                        'experience_skill_taming'] + profile['experience_skill_enchanting'] + profile[
                                        'experience_skill_alchemy'] + profile['experience_skill_fishing'],
                  'total_slayer_xp': profile['slayer_bosses']['zombie']['xp'] + profile['slayer_bosses']['spider'][
                      'xp'] + profile['slayer_bosses']['wolf']['xp'],

                  'farming_xp': profile['experience_skill_farming'],
                  'foraging_xp': profile['experience_skill_foraging'],
                  'combat_xp': profile['experience_skill_combat'],
                  'mining_xp': profile['experience_skill_mining'],
                  'taming_xp': profile['experience_skill_taming'],
                  'enchanting_xp': profile['experience_skill_enchanting'],
                  'alchemy_xp': profile['experience_skill_alchemy'],
                  'fishing_xp': profile['experience_skill_fishing'],

                  'revenant_xp': profile['slayer_bosses']['zombie']['xp'],
                  'tarantula_xp': profile['slayer_bosses']['spider']['xp'],
                  'sven_xp': profile['slayer_bosses']['wolf']['xp']
              }
              )
    conn.commit()
    conn.close()


def get_skill_top(n: int):
    conn = sqlite3.connect('./db/mtg.db')
    c = conn.cursor()
    c.execute("""
                 SELECT uuid, total_skill_xp,
                 farming_xp, foraging_xp, combat_xp, mining_xp, taming_xp, enchanting_xp, alchemy_xp, fishing_xp
                 FROM user_info ORDER BY total_skill_xp DESC
                """)
    result = c.fetchmany(n)
    conn.commit()
    conn.close()
    return result


def get_slayer_top(n: int):
    conn = sqlite3.connect('./db/mtg.db')
    c = conn.cursor()
    c.execute("""
                 SELECT uuid, total_slayer_xp, revenant_xp, tarantula_xp, sven_xp 
                 FROM user_info ORDER BY total_slayer_xp DESC
                """)
    result = c.fetchmany(n)
    conn.commit()
    conn.close()
    return result


def insert_member(discord_id, name):
    uuid = get_uuid_from_name(name)
    insert_player(discord_id, uuid, get_current_profile(uuid))


def out_skill_top(n: int):
    result = get_skill_top(n)
    return __out_skill(result)


def out_slayer_top(n: int):
    result = get_slayer_top(n)
    return __out_slayer(result)


def out_specific_skill(result):
    out = ''
    c = 1
    for res in result:
        out += '[' + str(c) + '] ' + get_name_from_uuid(res[0]) + ":\n\t>> " + str(__group_num(res[1])) + ' [' + str(round(util.converter.skill_exp_to_level(res[1]), 1)) + ']\n'
        c += 1
    return out


def __out_skill(result):
    out = ''
    c = 1
    for res in result:
        out += '[' + str(c) + '] ' + get_name_from_uuid(res[0]) + ":\n\t>> " + str(__group_num(res[1])) + ' [' + __average_skill_level(res) + ']\n'
        c += 1
    return out


def __out_slayer(result):
    out = ''
    c = 1
    for res in result:
        out += '[' + str(c) + '] ' + get_name_from_uuid(res[0]) + ":\n\t>> " + str(__group_num(res[1])) + ' [' + __average_slayer_level(res) + ']\n'
        c += 1
    return out


def __average_skill_level(result):
    div = 8
    c = 0
    level = 0
    for res in result:
        if c < 2:
            pass
        else:
            level += util.converter.skill_exp_to_level(res)
        c += 1
    f = level / div
    return str(round(f, 1))


def __average_slayer_level(result):
    c = 0
    out = ''
    for res in result:
        if c < 2:
            pass
        else:
            out += str(round(util.converter.slayer_exp_to_level(res), 1)) + '/'
        c += 1
    return str(out)[:-1]


def __group_num(i: int):
    locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')
    return locale.format_string("%d", round(i), grouping=True)


def update():
    print('Updating...')
    conn = sqlite3.connect('./db/mtg.db')
    c = conn.cursor()
    result = c.execute("SELECT discord_id, uuid FROM user_info").fetchall()
    conn.commit()
    for user in result:
        uuid = user[1]
        print(get_name_from_uuid(uuid))
        profile = get_current_profile(uuid)
        if 'experience_skill_farming' not in profile:
            # todo failback behaviour for disabled skills
            print(get_name_from_uuid(uuid) + ' has disabled his Skill Api')
        else:
            farming_xp = profile['experience_skill_farming']
            combat_xp = profile['experience_skill_combat']
            foraging_xp = profile['experience_skill_foraging']
            mining_xp = profile['experience_skill_mining']
            fishing_xp = profile['experience_skill_fishing']
            taming_xp = profile['experience_skill_taming']
            alchemy_xp = profile['experience_skill_alchemy']
            enchanting_xp = profile['experience_skill_enchanting']

            revenant_xp = profile['slayer_bosses']['zombie']['xp']
            tarantula_xp = profile['slayer_bosses']['spider']['xp']
            sven_xp = profile['slayer_bosses']['wolf']['xp']

            total_skill_xp_new = farming_xp + combat_xp + foraging_xp + mining_xp + fishing_xp + taming_xp + alchemy_xp + enchanting_xp
            total_slayer_xp_new = revenant_xp + tarantula_xp + sven_xp

            data = (total_skill_xp_new, total_slayer_xp_new,
                    farming_xp, foraging_xp, combat_xp, mining_xp, taming_xp, enchanting_xp, alchemy_xp, fishing_xp,
                    revenant_xp, tarantula_xp, sven_xp,
                    uuid)

            c.execute("""
                        UPDATE user_info
                        SET total_skilL_xp = ?, total_slayer_xp = ?,
                            farming_xp = ?, foraging_xp = ?, combat_xp = ?, mining_xp = ?, taming_xp = ?, enchanting_xp = ?, alchemy_xp = ?, fishing_xp = ?,
                            revenant_xp = ?, tarantula_xp = ?, sven_xp = ?
                        WHERE uuid = ?
                    """, data)
            conn.commit()
    conn.close()
    now = datetime.now()
    global last_updated_time
    last_updated_time = now.strftime("%H:%M:%S")
    print('Done Updating at ' + last_updated_time)
