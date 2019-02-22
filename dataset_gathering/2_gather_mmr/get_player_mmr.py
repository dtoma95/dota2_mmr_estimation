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
