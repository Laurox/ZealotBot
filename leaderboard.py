import sqlite3

conn = sqlite3.connect('./db/user_data.db')

c = conn.cursor()

c.execute("CREATE TABLE user_info(discordtag TEXT, uuid TEXT)")

conn.commit()
