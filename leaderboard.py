import sqlite3
from os import path

if not path.exists('./db/mtg.db'):
    print('creating mtg database...')
    conn = sqlite3.connect('./db/mtg.db')
    c = conn.cursor()
    c.execute("""
            CREATE TABLE user_info (
                discord_id INTEGER, 
                uuid TEXT,
                farming_xp REAL,
                foraging_xp REAL,
                combat_xp REAL,
                mining_xp REAL,
                taming_xp REAL,
                enchanting_xp REAL,
                alchemy_xp REAL,
                
                revenant_xp INTEGER,
                tarantula_xp INTEGER,
                sven_xp INTEGER)
            """)
    conn.commit()
    print('Done creating! You can now use mtg.db')


def init():
    return


def update():
    return


def output():
    return
