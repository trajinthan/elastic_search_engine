import json
import query_types
import re

from elasticsearch import Elasticsearch
from synonyms_list import runs, wickets, highest, lowest, matches, centuries
from similarity_checker import calSimilarity_words

INDEX = 'slodiplayersdata'
client = Elasticsearch(HOST="http://localhost",PORT=9200)

flags = [0, 0, 0, 0, 0, 0, 0, 0, 0]
flagedValue = {}
# flag_pointer -1 => numeric
# flag_pointer -2 => name
# flag_pointer -3 => birth_place
# flag_pointer -4 => age
# flag_pointer -5 => matches
# flag_pointer -6 => wickets
# flag_pointer -7 => runs
# flag_pointer -8 => highscore
# flag_pointer -9 => 100s

def searchByName(tokens):
    name_exists = False
    with open('corpus/data.json', 'r', encoding='utf-8') as f:
        player_dict = json.load(f)
    names=[]
    for distro in player_dict:
        names.append(distro['Name'])

    for t in range(len(tokens)):
        token = tokens[t]

        for name in names:
            name_list = name.split()
            for i in range(len(name_list)):
                if calSimilarity_words(token, name_list[i], 0.8) and abs(len(token)-len(name_list[i])) <= 1:
                    tokens.append(name_list[i])
                    name_exists = True
    return name_exists

def search(query):
    tokens = query.split()
    search_by_name = searchByName(tokens)
    containsDigit = bool(re.search(r'\d', query))
    tokens = list(set(tokens))
    field = ""
    if containsDigit: 
        for token in tokens:
            if token.isdigit():
                value = int(token)
            if token in highest:
                synonym = 'high'
            if token in lowest:
                synonym = 'low'
            if token in wickets:
                field = 'wickets'
                flags[5] = 1
            if token in runs:
                field = 'runs'
                flags[6] = 1
            if token in matches:
                field = 'matches'
                flags[4] = 1
            if token in centuries:
                field = 'centuries'
                flags[8] = 1

    if search_by_name:
        query = " ".join(tokens)
        query_body = query_types.exact_match(query)
        res = client.search(index=INDEX, body=query_body)
        return res
    elif field == 'runs' and synonym != None:
        query_body = query_types.field_value_condition_q(query, 'ஒட்டங்கள்', value, synonym)
        res = client.search(index=INDEX, body=query_body)
        return res
    elif field == 'wickets' and synonym != None:
        query_body = query_types.field_value_condition_q(query, 'விக்கெட்டுகள்', value, synonym)
        res = client.search(index=INDEX, body=query_body)
        return res
    elif field == 'matches' and synonym != None:
        query_body = query_types.field_value_condition_q(query, 'போட்டிகள்', value, synonym)
        res = client.search(index=INDEX, body=query_body)
        return res
    elif field == 'centuries' and synonym != None:
        query_body = query_types.field_value_condition_q(query, 'சதங்கள்', value, synonym)
        res = client.search(index=INDEX, body=query_body)
        return res
