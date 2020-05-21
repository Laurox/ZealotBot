import sqlite3
from os import path

if not path.exists('./db/mtg.db'):
    conn = sqlite3.connect('./db/mtg.db')
    c = conn.cursor()
    c.execute("CREATE TABLE user_info(discordtag TEXT, uuid TEXT)")
    conn.commit()
