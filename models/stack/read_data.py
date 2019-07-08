import json
import os
import numpy as np
from items_CNN.encoder_model import get_items_model
from team_CNN.encoder_model import get_team_model

DO_ITEMS = True
DO_HEROES = True
DO_ALL_PLAYERS = True
PATH = "../../data/player_match_details"

items_encoder = get_items_model("items_CNN/")
team_encoder = get_team_model("team_CNN/")

with open("items_CNN/heroes.json", "r") as f:
    heroes = json.load(f)
with open("items_CNN/items.json", "r") as f:
    items = json.load(f)

def read_data(batchsize):
    x = []
    y = []
    player_total = 0
    for filename in os.listdir(PATH):
        if ".json" not in filename:
            print(filename)
            continue

        fr = open(PATH+"/" + filename, "r")
        stringo = fr.readline()
        d = json.loads(stringo)
        fr.close()

        for player in d:
            account_id = player["account_id"]
            recorded_games = len(player["match_history"])
            mmr = player["solo_mmr"]

            retval = []
            if len(player["match_history"])<batchsize:
                print("SKIP PLYAER")
                continue
            br = 0
            for match in player["match_history"]:
                line_data = extract_match_data(match, account_id)
                if line_data is None:
                    continue
               # if len(line_data) != 94:
                  #  print(len(line_data))
               # print(len(line_data))
                retval.append(np.array(line_data, dtype=float))
                br+=1
                if br == 50:
                    break
            if len(retval) == 50:
                y.append(mmr)
                x.append(np.array(retval, dtype=float))
                player_total += 1
                print(player_total)
               # if(player_total == 15):
                #    return x,y

    return x, y
#mmr, win, is_radiant, duration
#gpm, xpm, denies, lh
def extract_match_data(match, player_id):
    retval = []
   # retval.append(player_id)
    #retval.append(match["match_id"])
    retval.append(match["duration"]/6000)


    #"tower_status_radiant": 0,
    #"tower_status_dire": 1830,
    #"barracks_status_radiant": 0,
    #"barracks_status_dire": 63,
    #"radiant_score": 31,
    #"dire_score": 38
    isRadient = False
    covek = None
    for p in match["players"]:
        try:
            if player_id == p["account_id"]:
                if p["player_slot"] < 5:
                    isRadient = True
                else:
                    isRadient = False
                covek = p
                break
        except:
            pass
    if covek is None:
        print("wtf")
        return None
    if isRadient:
        if match["radiant_win"]:
            retval.append(1)
        else:
            retval.append(0)
        retval.append(1)#retval.append(isRadient)
    else:
        if match["radiant_win"]:
            retval.append(0)
        else:
            retval.append(1)
        retval.append(0)#retval.append(isRadient)
    #retval.append(isRadient)
    #retval.append(match["duration"])
    retval.extend(player_details(covek))

    if DO_ALL_PLAYERS:
        # my team
        brojac = 0
        my_team = []
        for p in match["players"]:
            if isRadient and p["player_slot"] < 5:
                my_team.append(player_details(p))
                brojac += 1
            elif not isRadient and p["player_slot"] > 5:
                my_team.append(player_details(p))
                brojac += 1
        if brojac != 5:
            print("MYTEAM", brojac, match["match_id"])
        # enemy team
        enemy_team = []
        for p in match["players"]:
            if isRadient and p["player_slot"] > 5:
                enemy_team.append(player_details(p))
                brojac += 1
            elif not isRadient and p["player_slot"] < 5:
                enemy_team.append(player_details(p))
                brojac += 1
        if brojac != 10:
            print("GRESKA", brojac, match["match_id"])

            return None

        team_data = []
        team_data.append(my_team)
        team_data.append(enemy_team)

        team_data = np.array(team_data, dtype=float)

        team_data = team_data.reshape(len(team_data), team_data[0].shape[0], team_data[0].shape[1], 1)

        encoded_data = team_encoder.predict(team_data)

        for i in encoded_data[0][0]:
            retval.append(i[0])
        for i in encoded_data[1][0]:
            retval.append(i[0])
    return retval

def player_details(covek):
    retval = []
    retval.append(covek["gold_per_min"]/1000)
    retval.append(covek["xp_per_min"]/1000)
    retval.append(covek["kills"]/50)
    retval.append(covek["deaths"]/50)
    retval.append(covek["assists"]/50)
    retval.append(covek["last_hits"]/1000)
    retval.append(covek["denies"]/50)
    retval.append(covek["level"]/25)
    if DO_HEROES:
        onehothero = heroes_one_hot(covek["hero_id"], heroes)
        retval.extend(onehothero)
    else:
        retval.append(int(covek["hero_id"])/129)
    if DO_ITEMS:
        my_items = [covek["item_0"], covek["item_1"], covek["item_2"], covek["item_3"], covek["item_4"],
                    covek["item_5"], covek["backpack_0"], covek["backpack_1"], covek["backpack_2"]]
        onehotitem = items_one_hot(my_items, items)
        retval.extend(onehotitem)
    retval.extend([0,0])
    return retval

def main_player_details(covek):
    retval = []
    retval.append(covek["gold_per_min"]/1000)
    retval.append(covek["xp_per_min"]/1000)
    retval.append(covek["kills"]/50)
    retval.append(covek["deaths"]/50)
    retval.append(covek["assists"]/50)
    retval.append(covek["last_hits"]/1000)
    retval.append(covek["denies"]/50)
    retval.append(covek["level"]/25)
    if DO_HEROES:
        onehothero = heroes_one_hot(covek["hero_id"], heroes)
        retval.extend(onehothero)
    else:
        retval.append(int(covek["hero_id"])/129)
    if DO_ITEMS:
        my_items = [covek["item_0"], covek["item_1"], covek["item_2"], covek["item_3"], covek["item_4"],
                    covek["item_5"], covek["backpack_0"], covek["backpack_1"], covek["backpack_2"]]
        onehotitem = items_one_hot(my_items, items)
        encoded_data = items_encoder.predict(onehotitem)

        retval.extend(encoded_data[0])
    return retval


def heroes_one_hot(hero_id, heroes):
    retval = []
    for key in heroes.keys():
        retval.append(0)

    if hero_id < 24:
        index_for_dic = hero_id - 1
    elif hero_id < 115:
        index_for_dic = hero_id - 2
    else:
        index_for_dic = hero_id - 6

    retval[index_for_dic] = 1
    return retval

def items_one_hot(my_items, items):
    retval = []
    for key in items.keys():
        retval.append(0)
    for item_id in my_items:
        if item_id == 0:
            continue
        if item_id < 265:
            index_for_dic = item_id - 1
        elif item_id < 272:
            index_for_dic = item_id - 2
        elif item_id < 279:
            index_for_dic = item_id - 4
        elif item_id == 279:
            index_for_dic = item_id - 5
        else:
            continue
        retval[index_for_dic] += 1
    return retval
