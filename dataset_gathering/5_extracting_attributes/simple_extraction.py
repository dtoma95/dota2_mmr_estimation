import dota2api
import datetime
import json
import inspect
import operator
import os
#api = dota2api.Initialise("D20C32BC820746E3CB16D031AB2CC2F9", raw_mode=True)
#heroes = api.get_heroes()
f = open("data.csv", "w")
f.write("account_id,mmr,gpm,xpm,kills,deaths,assists,last_hits,denies,level,recorded_games"+"\n")
 
files = os.listdir("../../data/match_details")
br=0
for filename in files:
    if ".json" not in filename:
        print(filename)
        continue
    
    fr = open("../../data/match_details/" + filename, "r")
    stringo = fr.readline()
    d = json.loads(stringo)
    fr.close()
    #"account_id": 4294967295, "player_slot": 132, "hero_id": 56, 
    #"item_0": 212, "item_1": 98, "item_2": 48, "item_3": 46, "item_4": 168, "item_5": 135, "backpack_0": 0, "backpack_1": 0, "backpack_2": 0, 
    #"kills": 30, "deaths": 8, "assists": 12, "leaver_status": 0, "last_hits": 114, "denies": 2, "gold_per_min": 486, "xp_per_min": 639, "level": 25
    
    
    for player in d:
        account_id = player["account_id"]
        
        GPM = 0
        XPM = 0
        KILLS = 0
        DEATHS = 0
        ASSISTS = 0
        LS = 0
        DENIES = 0
        LEVEL = 0
        RECORDED_GAMES=len(player["match_history"])
        for match in player["match_history"]:
            if(match["game_mode"]!=22):
                RECORDED_GAMES-=1
                continue
            for covek in match["players"]:
                #print(covek)
                if("account_id"in covek and covek["account_id"] == account_id):
                    GPM += covek["gold_per_min"]
                    XPM += covek["xp_per_min"]
                    KILLS += covek["kills"]
                    DEATHS += covek["deaths"]
                    ASSISTS += covek["assists"]
                    LS += covek["last_hits"]
                    DENIES += covek["denies"]
                    LEVEL += covek["level"]
        if (RECORDED_GAMES ==0):
            print("zero")
            continue
        GPM /= RECORDED_GAMES
        XPM /= RECORDED_GAMES
        KILLS /= RECORDED_GAMES
        DEATHS /= RECORDED_GAMES
        ASSISTS /= RECORDED_GAMES
        LS /= RECORDED_GAMES
        DENIES /= RECORDED_GAMES
        LEVEL /= RECORDED_GAMES
            #print(matches)
        #print(br)
        f.write(str(account_id)+","+str(player["solo_mmr"])+","+str(GPM)+","+str(XPM)+","+str(KILLS)+","+str(DEATHS)+","+str(ASSISTS)+","+str(LS)+","+str(DENIES)+","+str(LEVEL)+","+str(RECORDED_GAMES)+"\n")
        br+=1
        #for mec in matches["matches"]:
        #	vratio = api.get_match_details(match_id=mec["match_id"])
        #	player["match_history"].append(vratio)
        
f.close()