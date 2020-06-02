import constants

def skill_exp_to_level(exp: int):
    c = 0
    while not c > 49 and constants.skill_xp_requirements[c] <= exp:
        c += 1
    if c >= 50:
        return c
    left = exp - constants.skill_xp_requirements[c - 1]
    needed = constants.skill_xp_requirements[c] - constants.skill_xp_requirements[c - 1]
    return c + left/needed


def slayer_exp_to_level(exp: int):
    c = 0
    while not c > 8 and constants.slayer_level_requirements[c] <= exp:
        c += 1
    if c >= 9:
        return c
    left = exp - constants.slayer_level_requirements[c - 1]
    needed = constants.slayer_level_requirements[c] - constants.slayer_level_requirements[c - 1]
    return c + left/needed
