import json
from similarity_checker import calSimilarity

def exact_match(query):
    search_val = " ".join(calSimilarity(query))
    q = {
            "size": 500,
            "explain": True,
            "query": {
                "match": {
                    "வீரர்_பெயர்": search_val
                }
            },
        }
    q = json.dumps(q)
    return q

def field_value_condition_q(query, field, value, synonym):
    print(value,field)
    if synonym == 'high':
        q = {   
            "size": 200,
            "explain": True,
            "query": {
                "bool":{
                    "must": {
                        "range" : {
                field : {
                    "gte" : value,
                    "lte" : 20000,
                    "boost": 5.0
                    }
                }
                    }
                }
            
            }
        }
    else:
        q = {   "size": 50,
            "explain": True,
            "query": {
            "range" : {
                field : {
                    "gte" : 0,
                    "lte" : value,
                    "boost": 5.0
                    }
                }
            }
        }
    q = json.dumps(q)
    
    return q