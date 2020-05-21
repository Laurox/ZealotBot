import requests

data = requests.get("https://api.hypixel.net/player?key=1d017c26-5792-4765-818f-f0de300df3b4&name=LauroxTV").json()

print(data)
