from elasticsearch import Elasticsearch, helpers
from elasticsearch_dsl import Index
import json, re

client = Elasticsearch(HOST="http://localhost", PORT=9200)
INDEX = 'sl_odi_player'

def createIndex():
    index = Index(INDEX, using=client)
    res = index.create()
    print(res)

def read_all_players():
    with open('corpus/data.json', 'r', encoding='utf-8-sig') as f:
        all_players = json.loads(f.read())
        res_list = [i for n, i in enumerate(all_players) if i not in all_players[n + 1:]]
        print(res_list)
        return res_list

def genData(all_players):
    for player in all_players:
        name = player.get("Name", None)
        birth_year = player.get("BirthYear",None)
        birth_place = player.get("BirthPlace", None)
        age = player.get("Age", None)
        batting_style = player.get("Batting Style", None)
        bowling_style = player.get("Bowling Style", None)
        role = player.get("Playing Role", None)
        education = player.get("Education", None)
        matches = player.get("Matches",None)
        innings = player.get('Innings', None)
        wickets = player.get("Wickets", None)
        bbm = player.get("BBM", None)
        runs = player.get("Runs", None)
        highscore = player.get("Highscore", None)
        fifties = player.get("50s", None)
        hundreds = player.get("100s", None)

        yield {
            "_index": "slodiplayersdata",
            "_source": {
                "வீரர்_பெயர்": name,
                "பிறந்த_வருடம்": int(birth_year),
                "பிறந்த_இடம்": birth_place,
                "வயது": age,
                "பேட்டிங்_பாணி": batting_style,
                "பந்துவீச்சு_பாணி": bowling_style,
                "பங்கு": role,
                "பாடசாலை": education,
                "போட்டிகள்": int(matches),
                "இன்னிங்ஸ்": int(innings),
                "விக்கெட்டுகள்": int(wickets),
                "சிறந்த_பெறுதிகள்": bbm,
                "ஒட்டங்கள்": int(runs),
                "அதிக_ஒட்டங்கள்": highscore,
                "அரை_சதங்கள்": fifties,
                "சதங்கள்": int(hundreds)
            },
        }

createIndex()
all_players = read_all_players()
print(all_players)
helpers.bulk(client,genData(all_players))
