"""
    Gathers steam-ids of dota 2 players using the official Valve api.
    Fetches a dota 2 matches starting from the given starting_id, only ranked matches are observed.
    For each match, the steam_id of the 10 players is recorded.
"""
import dota2api
import datetime

api = dota2api.Initialise("D20C32BC820746E3CB16D031AB2CC2F9", raw_mode=True)

staring_id = 2734653241


f = open("results.txt", "a")

staring_id = staring_id+3500 #+6500 sledeci put, ili preci na seq_num
for i in range(0, 3000):
	staring_id = staring_id+1
	try:
		match = api.get_match_details(match_id=staring_id)
		print(datetime.datetime.fromtimestamp(match["start_time"]).strftime('%c'))
	except:
		#print("nista jbg")
		continue
	if match["game_mode"]!=22:
		continue
	
	print("FOUND")
	for igrac in match["players"]:
		try:
			if(igrac["account_id"] != 4294967295): #4294967295 is a placehold ID for players that have not set their in-game data as public
				f.write(str(igrac["account_id"])+"\n")
		except:
			print("wtflol")
	staring_id = staring_id+1
