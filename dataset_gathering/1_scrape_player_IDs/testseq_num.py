"""
    Different form scrape_IDs.py because it uses the match sequential numbers instead of match_id
    Gathers steam-ids of dota 2 players using the official Valve api.
    Fetches a dota 2 matches starting from the given starting_id, only ranked matches are observed.
    For each match, the steam_id of the 10 players is recorded.
"""

import dota2api
import datetime
api = dota2api.Initialise("D20C32BC820746E3CB16D031AB2CC2F9", raw_mode=True)

staring_id = 2386665066


f = open("igraci_raw.txt", "w")

#staring_id = staring_id+6500 #+6500 sledeci put, ili preci na seq_num
for i in range(0, 160):
	#staring_id = staring_id+1
	try:
		matches = api.get_match_history_by_seq_num(start_at_match_seq_num=staring_id)
		#print(datetime.datetime.fromtimestamp(match["start_time"]).strftime('%c'))
	except:
		#print("nista jbg")
		continue
	for match in matches["matches"]:
		if match["game_mode"]!=22:
			continue
	
		#print(datetime.datetime.fromtimestamp(match["start_time"]).strftime('%c'))
		#print(match["match_seq_num"])
		
		for igrac in match["players"]:
			try:
				
				if(igrac["account_id"] != 4294967295): #4294967295 je placeholder id za ljude koji nisu stavili da im ingame-data bude public
					#print(igrac["account_id"])
					f.write(str(igrac["account_id"])+"\n")
			except:
				print("wtflol")
	#print(datetime.datetime.fromtimestamp(matches["matches"][-1]["start_time"]).strftime('%c'))
	print(matches["matches"][-1]["match_seq_num"])
	
	staring_id = matches["matches"][-1]["match_seq_num"]+1
