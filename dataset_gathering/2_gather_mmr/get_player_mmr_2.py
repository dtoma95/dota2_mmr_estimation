"""
    Gets most recent MMR and match recorded in 2017 for each player.
    Uses the data that is gathered with get_player_mmr.py
"""

import json

f = open("lost323.txt", "r")
stringo = f.readline()
d = json.loads(stringo)
f.close()

fw = open("player_mmr2.txt", "a")
dropped = 0

for player in d:
	fw.write(str(player["account_id"]) + "\n")
	continue
	if(len(player["history"]) == 0):
		dropped = dropped+1
		continue
	for m in reversed(player["history"]):
		
		
		if m["_match_id"] == None or m["_solo_competitive_rank"] == None:
			continue
		if True: #if(m["_match_id"] < 3614340478 and m["_match_id"] > 2883187036): #ovo znaci da gledamo metcheve koji su samo pre 7.00 (za sad je ovako ali mozemo promeniti, samo treba final.txt da imamo uvek)
			#print(m["_solo_competitive_rank"])
			fw.write(str(player["account_id"]) + ";" + str(m["_solo_competitive_rank"]) + ";" + str(m["_match_id"]) + "\n")
			break
print("izbaceno:( ", dropped)
fw.close()
#print(lista)
