import requests
import json
import sqlite3

#sqlite-თან დაკავშირება
conn = sqlite3.connect('basketball_players.db')
c = conn.cursor()

#url
url = "https://api.balldontlie.io/v1/players"
headers = {
    "Authorization": "f7752245-0741-411d-9607-9fc64a0d4886"
}

#კლასის შექმნა
class BasketballPlayer:
    def __init__(self, id, first_name, last_name, position, team):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.position = position
        self.team = team

    #ფუნქცია ინფორმაციის database-ში დასამატებლად
    def add_to_db(self):
        c.execute('''INSERT INTO basketball_players (id, first_name, last_name, position, team) VALUES (?,?,?,?,?)''',
                  (self.id, self.first_name, self.last_name, self.position, json.dumps(self.team, indent=4)))
        conn.commit()

#ფუნქცია API-დან მოთამაშეების ინფორმაციების წამოსაღებლად
def fetch_basketball_players():
    players = []
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        r_data = r.json()
        for data in r_data["data"]:
            player = BasketballPlayer(data['id'], data["first_name"], data["last_name"], data["position"], data["team"])
            players.append(player)
        for player in players:
            player.add_to_db()
    else:
        print(f"Connection failed, Status Code: {r.status_code}")

#ფუნქცია მონაცემების წასაკითხად და ამოსაპრინტად
def read_basketball_players():
    players = c.execute('''SELECT id, first_name, last_name, position, team FROM basketball_players''').fetchall()
    for player in players:
        print(f"ID: {player[0]}\nFullName: {player[1]} {player[2]}\n Position: {player[3]}\n Team: {player[4]}")


#ცხრილის შექმნა მონაცემებისთვის
c.execute('''CREATE TABLE IF NOT EXISTS basketball_players
            (id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            position TEXT,
            team TEXT)''')

#მონაცემთა წამოღება და database-ში გადატანა
fetch_basketball_players()

#მონაცემთა წაკითხვა და ამოპრინტვა
read_basketball_players()

conn.commit()
conn.close()