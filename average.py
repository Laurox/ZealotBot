import util.converter
import sqlite3
import locale


def get_averages():
    conn = sqlite3.Connection('./db/mtg.db')
    c = conn.cursor()
    result = c.execute("""SELECT total_skill_xp, farming_xp, foraging_xp, combat_xp, mining_xp, taming_xp, enchanting_xp, fishing_xp, alchemy_xp, total_slayer_xp, revenant_xp, tarantula_xp, sven_xp FROM user_info""").fetchall()
    conn.commit()
    conn.close()

    return '\nGildendurschnitt:\n\tSkill: ' + get_skill_average(result) + '\n\tSlayer: ' + get_slayer_average(result)


def get_skill_average(result):
    length = len(result)
    total = 0
    skill_average = 0
    for res in result:
        total += res[0]
        c = 1
        while c <= 8:
            skill_average += round(util.converter.skill_exp_to_level(res[c]), 1)
            c += 1
    xp = round(total/ length)
    return str(__group_num(xp)) + ' >> [' + str(round(skill_average/(8*length), 1)) + ']'


def get_slayer_average(result):
    length = len(result)
    total = 0
    slayer_average = 0
    for res in result:
        total += res[9]
        c = 10
        while c <= 12:
            slayer_average += round(util.converter.slayer_exp_to_level(res[c]), 1)
            c += 1
    # average total slayer xp NOT for a single boss
    xp = round(total / length)
    return str(__group_num(xp)) + ' >> [' + str(round(slayer_average/(3*length), 1)) + ']'


def __group_num(i: int):
    locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')
    return locale.format_string("%d", round(i), grouping=True)
