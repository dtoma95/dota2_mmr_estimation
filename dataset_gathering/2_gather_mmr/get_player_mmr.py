"""
Gets the MMR history of each player, that was recorded by OpenDota.
Uses the OpenDota API.
"""

from __future__ import print_function
import time
import od_python
from od_python.rest import ApiException
from pprint import pprint
import json

# create an instance of the API class
api_instance = od_python.PlayersApi()
 # int | Steam32 account ID

fr = open("igraci2.txt")
lista_ideva = fr.readlines()
print(len(lista_ideva))

lista=[]

red = 323 

while red < len(lista_ideva):
    try: 
        # GET /players/{account_id}/ratings
        #
        api_response=[]
        for i in range(red, len(lista_ideva)):
            id = lista_ideva[i]
            account_id = int(id.strip())
            igrac = {"account_id": account_id, "history": []}
            
            api_response = api_instance.players_account_id_ratings_get(account_id)
            for obj in api_response:
                igrac["history"].append(obj.__dict__)
    
            lista.append(igrac)
            print(red)
            red = red+1
            break
    
    except ApiException as e:
        print("Exception when calling PlayersApi->players_account_id_ratings_get: %s\n" % e)
        print("stigli smo do - ", red)
        f = open("final"+str(red)+".txt", "w")
        f.write(json.dumps(lista))
        f.close()
        time.sleep(32)
        
        
   

f = open("final.txt", "w")
f.write(json.dumps(lista))
f.close()

#print(lista)
[
    {
        "account_id":83573797,
        "match_id":null,
        "solo_competitive_rank":null,
        "competitive_rank":4011,
        "time":"2015-11-18T15:57:17.058Z"
    },
    {
        "account_id":83573797,
        "match_id":2268559035,
        "solo_competitive_rank":3681,
        "competitive_rank":null,
        "time":"2016-04-03T03:01:08.833Z"
    },
    {
        "account_id":83573797,
        "match_id":2651120044,
        "solo_competitive_rank":null,
        "competitive_rank":3422,
        "time":"2016-09-17T16:07:53.051Z"
    },
    {
        "account_id":83573797,
        "match_id":2651392381,
        "solo_competitive_rank":null,
        "competitive_rank":3422,
        "time":"2016-09-17T18:40:14.745Z"
    },
    {
        "account_id":83573797,
        "match_id":2653089689,
        "solo_competitive_rank":null,
        "competitive_rank":3397,
        "time":"2016-09-18T12:09:37.366Z"
    },
    {
        "account_id":83573797,
        "match_id":2653782861,
        "solo_competitive_rank":4024,
        "competitive_rank":null,
        "time":"2016-09-18T17:43:19.804Z"
    },
    {
        "account_id":83573797,
        "match_id":2654979542,
        "solo_competitive_rank":4048,
        "competitive_rank":null,
        "time":"2016-09-19T10:20:56.800Z"
    },
    {
        "account_id":83573797,
        "match_id":2655053043,
        "solo_competitive_rank":4048,
        "competitive_rank":null,
        "time":"2016-09-19T11:23:07.116Z"
    }
]
[
    {
        "match_id":3556849965,
        "match_seq_num":3094040961,
        "start_time":1510443621,
        "lobby_type":7,
        "radiant_team_id":0,
        "dire_team_id":0,
        "players":[{"account_id":4294967295, "player_slot":0, "hero_id":9},
                   {"account_id":313600850,"player_slot":1, "hero_id":44},
                   { "account_id":246685252, "player_slot":2, "hero_id":42 },
                   { "account_id":337316935, "player_slot":3, "hero_id":47 },
                   { "account_id":85349036, "player_slot":4, "hero_id":68 },
                   { "account_id":297682517, "player_slot":128, "hero_id":93 },
                   { "account_id":33288395, "player_slot":129, "hero_id":120 },
                   { "account_id":50757564, "player_slot":130, "hero_id":38 },
                   { "account_id":107830683, "player_slot":131, "hero_id":112 },
                   { "account_id":331424032, "player_slot":132, "hero_id":13 } ]
    }
]