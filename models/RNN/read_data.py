import json
import os

DO_ITEMS = False
DO_HEROES = False
DO_ALL_PLAYERS = True
PATH = "../../data/tomislav"

with open("heroes.json", "r") as f:
    heroes = json.load(f)
with open("items.json", "r") as f:
    items = json.load(f)

def read_data1(path):
    f_write = open("one_be_one.csv", "w")

    write_header(f_write)


    for filename in os.listdir(path):
        if ".json" not in filename:
            print(filename)
            continue

        fr = open(path+"/" + filename, "r")
        stringo = fr.readline()
        d = json.loads(stringo)
        fr.close()

        for player in d:
            account_id = player["account_id"]
            recorded_games = len(player["match_history"])
            mmr = player["solo_mmr"]

            for match in player["match_history"]:
                line_data = extract_match_data(match, account_id, mmr)
                if line_data is not None:
                    line = ""
                    for i in line_data:
                        line += str(i)+","
                    f_write.write(line[:-1]+"\n")
        break
    f_write.close()

def write_header(f_write):
    header = "account_id,match_id,mmr,win,is_radiant,duration"
    basic_data = ["gold_per_min", "xp_per_min", "kills", "deaths", "assists", "last_hits", "denies", "level"]

    heroes_one_hot = []
    if DO_HEROES:
        for id in heroes.keys():
            heroes_one_hot.append(heroes[id])
    else:
        basic_data.append("hero_id")

    items_one_hot = []
    if DO_ITEMS:
        for id in items.keys():
            items_one_hot.append(items[id])

    players = ["this_player"]
    if DO_ALL_PLAYERS:
        players.extend(["teammate_1", "teammate_2", "teammate_3", "teammate_4", "enemy_1", "enemy_2", "enemy_3", "enemy_4", "enemy_5"])


    for p in players:
        for b in basic_data:
            header += "," + p + "_" + b
        for h in heroes_one_hot:
            header+= ","+p+"_"+ h
        for i in items_one_hot:
            header+= ","+p+"_"+ i
    f_write.write(header + "\n")

#account_id, mmr, win, is_radiant, duration
#gpm, xpm, denies, lh
def extract_match_data(match, player_id, mmr):
    retval = []
    retval.append(player_id)
    retval.append(match["match_id"])
    retval.append(mmr)


    #"tower_status_radiant": 0,
    #"tower_status_dire": 1830,
    #"barracks_status_radiant": 0,
    #"barracks_status_dire": 63,
    #"radiant_score": 31,
    #"dire_score": 38
    isRadient = False
    covek = None
    for p in match["players"]:
        if player_id == p["account_id"]:
            if p["player_slot"] < 5:
                isRadient = True
            else:
                isRadient = False
            covek = p
            break
    if covek is None:
        print("wtf")
        return None
    if isRadient:
        retval.append( match["radiant_win"])
    else:
        retval.append(not match["radiant_win"])
    retval.append(isRadient)
    retval.append(match["duration"])
    retval.extend(player_details(covek))

    if DO_ALL_PLAYERS:
        # my team
        brojac = 1
        for p in match["players"]:
            try:
                if player_id == p["account_id"]:
                    continue
            except:
                pass
            if isRadient and p["player_slot"] < 5:
                retval.extend(player_details(p))
                brojac += 1
            elif not isRadient and p["player_slot"] > 5:
                retval.extend(player_details(p))
                brojac += 1
        if brojac != 5:
            print("MYTEAM", brojac, match["match_id"])
        # enemy team
        for p in match["players"]:
            try:
                if player_id == p["account_id"]:
                    continue
            except:
                pass
            if isRadient and p["player_slot"] > 5:
                retval.extend(player_details(p))
                brojac += 1
            elif not isRadient and p["player_slot"] < 5:
                retval.extend(player_details(p))
                brojac += 1
        if brojac != 10:
            print("GRESKA", brojac, match["match_id"])

            return None
    return retval

def player_details(covek):
    retval = []
    retval.append(covek["gold_per_min"])
    retval.append(covek["xp_per_min"])
    retval.append(covek["kills"])
    retval.append(covek["deaths"])
    retval.append(covek["assists"])
    retval.append(covek["last_hits"])
    retval.append(covek["denies"])
    retval.append(covek["level"])
    if DO_HEROES:
        onehothero = heroes_one_hot(covek["hero_id"], heroes)
        retval.extend(onehothero)
    else:
        retval.append(covek["hero_id"])
    if DO_ITEMS:
        my_items = [covek["item_0"], covek["item_1"], covek["item_2"], covek["item_3"], covek["item_4"],
                    covek["item_5"], covek["backpack_0"], covek["backpack_1"], covek["backpack_2"]]
        onehotitem = items_one_hot(my_items, items)
        retval.extend(onehotitem)
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
        else:
            index_for_dic = item_id - 2

        retval[index_for_dic] += 1
    return retval

read_data1(PATH)