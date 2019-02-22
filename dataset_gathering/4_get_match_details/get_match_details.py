"""
    Calls the get_match_details end-point, of the official dota 2 api, for each match that was gathered before.
"""

import dota2api
import datetime
import json
import inspect
import operator

api = dota2api.Initialise("D20C32BC820746E3CB16D031AB2CC2F9", raw_mode=True)
#https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?account_id=319739541&start_at_match_id=3011774608&key=D20C32BC820746E3CB16D031AB2CC2F9&date_max=1507380028
f = open("player_match_details_204.json", "r")
stringo = f.readline()
d = json.loads(stringo)
f.close()
br=0
#http://api.steampowered.com/IEconDOTA2_570/GetHeroes/v0001/?key=D20C32BC820746E3CB16D031AB2CC2F9

heroes = api.get_heroes()
checkpoint = 2734
last_save = 2734
for player in d:
	br = br+1
	print(br)
	if (br<last_save):
		continue
	
	
	listica = []
	
	try:#player["account_id"]
		broj = 0
		for m in player["match_history"]:
			broj = broj+1
			mec = api.get_match_details(match_id=m["match_id"])
			listica.append(mec)
			print(broj)
		#print(matches)
	except:
		print("nista jbg")
		if br>1:
			break
		continue
	player["match_history"] = listica
	if(br >checkpoint):
		checkpoint = br+100
		
		f = open("player_match_details"+str(last_save)+"_"+str(br)+".json", "w")
		f.write(json.dumps(d[last_save: br]))
		f.close()
		last_save = br
	#for mec in matches["matches"]:
	#	vratio = api.get_match_details(match_id=mec["match_id"])
	#	player["match_history"].append(vratio)
	
	
	

f = open("player_match_details.json", "w")
f.write(json.dumps(d[checkpoint:br]))
f.close()