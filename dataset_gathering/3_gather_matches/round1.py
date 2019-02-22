"""
    Tries to gather the last 100 matches before the match where the players MMR was recorded.
    Uses the get_match_history api call off the official dota 2 api.
    The get_match_history call is bugged for a lot of players so round2.py is needed.
"""

import dota2api
import datetime
import json
api = dota2api.Initialise("D20C32BC820746E3CB16D031AB2CC2F9", raw_mode=True)


f = open("player_mmr.txt", "r")
reading = f.readlines()
retval = []
br = 0
for line in reading:
	print(br)
	splitovano = line.strip().split(";")
	player = {"account_id": int(splitovano[0]), "solo_mmr": int(splitovano[1]), "last_match": int(splitovano[2]), "match_history": []}

	try:
		matches = api.get_match_history(account_id=player["account_id"], start_at_match_id=player["last_match"], game_mode=22, matches_requested=100, min_players=10)
		
	except:
		print("nista jbg")
		continue
	print("FOUND", len(matches["matches"]))
	player["match_history"] = matches["matches"]
	
	#for mec in matches["matches"]:
	#	vratio = api.get_match_details(match_id=mec["match_id"])
	#	player["match_history"].append(vratio)
		
	retval.append(player)
	br = br+1
	

f = open("player_matches.json", "w")
f.write(json.dumps(retval))
f.close()