import leaderboard
import time


while True:

    leaderboard.update()

    with open('./db/timestamp.txt', 'w') as file:
        file.write(leaderboard.last_updated_time)

    time.sleep(60*10)
