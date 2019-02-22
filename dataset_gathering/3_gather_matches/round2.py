"""
    Uses a workaround for the bug in the get_match_history api call, but is a lot slower than round1.py
"""

import dota2api
import datetime
import json
import inspect
import operator

api = dota2api.Initialise("D20C32BC820746E3CB16D031AB2CC2F9", raw_mode=True)
#https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?account_id=319739541&start_at_match_id=3011774608&key=D20C32BC820746E3CB16D031AB2CC2F9&date_max=1507380028
f = open("player_matches2817_save.json", "r")
stringo = f.readline()
d = json.loads(stringo)
f.close()
br=0
#http://api.steampowered.com/IEconDOTA2_570/GetHeroes/v0001/?key=D20C32BC820746E3CB16D031AB2CC2F9

heroes = api.get_heroes()
checkpoint = 1
for player in d:
	print(br)
	br = br+1
	listica = []
	if (len(player["match_history"])>=50):
		for p in player["match_history"]:
			print(p)
			break
		continue
	
	try:#player["account_id"]
		for hero in heroes["heroes"]:
			print(hero["id"])
			matches = api.get_match_history(account_id=player["account_id"], start_at_match_id=player["last_match"], hero_id=hero["id"], game_mode=22, matches_requested=100, min_players=10)#
			listica.extend(matches["matches"])
		#print(matches)
	except:
		print("nista jbg")
		if br>1:
			break
		continue
	print("FOUND", len(listica))
	listica = [d for d in listica if d['lobby_type'] == 7]
	listica.sort(key=operator.itemgetter('match_id'), reverse = True)
	player["match_history"] = listica[:100]
    
	f = open("test.json", "w")
	f.write(json.dumps(listica))
	f.close()
	break
	if(br >checkpoint):
		checkpoint = br+100
		f = open("player_matches_"+str(br)+".json", "w")
		f.write(json.dumps(d))
		f.close()
	#for mec in matches["matches"]:
	#	vratio = api.get_match_details(match_id=mec["match_id"])
	#	player["match_history"].append(vratio)
	
	
	

f = open("player_matches3.json", "w")
f.write(json.dumps(d))
f.close()