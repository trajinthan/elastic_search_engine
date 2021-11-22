from elasticsearch import Elasticsearch, helpers
from elasticsearch_dsl import Index
import json, re
import codecs
import unicodedata

client = Elasticsearch(HOST="http://localhost", PORT=9200)
INDEX = 'name'

def createIndex():
    index = Index(INDEX, using=client)
    res = index.create()
    print(res)

def read_all_songs():
    with open('data.json', 'r', encoding='utf-8-sig') as f:
        all_songs = json.loads(f.read())
        res_list = [i for n, i in enumerate(all_songs) if i not in all_songs[n + 1:]]
        print(res_list)
        return res_list

def genData(song_array):
    for song in song_array:
        name = song.get("Name", None)
        dob = song.get("DOB",None)
        birth_place = song.get("BirthPlace", None)
        age = song.get("Age", None)
        batting_style = song.get("Batting Style", None)
        bowling_style = song.get("Bowling Style", None)
        role = song.get("Playing Role", None)
        education = song.get("Education", None)
        matches = song.get("Matches",None)
        innings = song.get('Innings', None)
        wickets = song.get("Wickets", None)
        bbm = song.get("BBM", None)
        runs = song.get("Runs", None)
        highscore = song.get("Highscore", None)
        fifties = song.get("50s", None)
        hundreds = song.get("100s", None)

        yield {
            "_index": "slcricketplayersdata",
            "_source": {
                "வீரர் பெயர்": name,
                "பிறந்த திகதி": dob,
                "பிறந்த இடம்": birth_place,
                "வயது": age,
                "பேட்டிங் பாணி": batting_style,
                "பந்துவீச்சு பாணி": bowling_style,
                "பங்கு": role,
                "பாடசாலை": education,
                "போட்டிகள்": matches,
                "இன்னிங்ஸ்": innings,
                "விக்கெட்டுகள்": wickets,
                "சிறந்த பெறுதிகள்": bbm,
                "ஒட்டங்கள்": runs,
                "அதிக ஒட்டங்கள்": highscore,
                "அரை சதங்கள்": fifties,
                "சதங்கள்": hundreds
            },
        }

createIndex()
all_songs = read_all_songs()
helpers.bulk(client,genData(all_songs))