import json
import os

with open("heroes.json", "r") as f:
    heroes = json.load(f)

f_write = open("data_all_heroes.csv", "w")


def main():

    # do 23 je i-1
    # do 114 je i-2
    # do 121 je i-6

    index_for_header = 0
    for filename in os.listdir("../../../match_details"):
        if ".json" not in filename:
            print(filename)
            continue

        fr = open("../../../match_details/" + filename, "r")
        stringo = fr.readline()
        d = json.loads(stringo)
        fr.close()

        details_for_every_hero = initialize()

        if index_for_header == 0:
            header = "account_id,mmr,"
            for dic in details_for_every_hero:
                header += ",".join(list(dic.keys())[1:])
                header += ","

            header = header[:-1]

            f_write.write(header + "\n")
            index_for_header += 1

        for player in d:
            account_id = player["account_id"]
            recorded_games = len(player["match_history"])
            mmr = player["solo_mmr"]

            for match in player["match_history"]:
                if match["game_mode"] != 22:
                    recorded_games -= 1
                    continue
                for exact_player in match["players"]:
                    if "account_id" in exact_player and exact_player["account_id"] == account_id:

                        if exact_player["hero_id"] < 24:
                            index_for_dic = exact_player["hero_id"] - 1
                        elif exact_player["hero_id"] < 115:
                            index_for_dic = exact_player["hero_id"] - 2
                        else:
                            index_for_dic = exact_player["hero_id"] - 6

                        hero_name = heroes[str(exact_player["hero_id"])]
                        details_for_every_hero[index_for_dic][hero_name + "_gpm"] += exact_player["gold_per_min"]
                        details_for_every_hero[index_for_dic][hero_name + "_xpm"] += exact_player["xp_per_min"]
                        details_for_every_hero[index_for_dic][hero_name + "_kills"] += exact_player["kills"]
                        details_for_every_hero[index_for_dic][hero_name + "_deaths"] += exact_player["deaths"]
                        details_for_every_hero[index_for_dic][hero_name + "_assists"] += exact_player["assists"]
                        details_for_every_hero[index_for_dic][hero_name + "_lh"] += exact_player["last_hits"]
                        details_for_every_hero[index_for_dic][hero_name + "_denies"] += exact_player["denies"]
                        details_for_every_hero[index_for_dic][hero_name + "_level"] += exact_player["level"]
                        details_for_every_hero[index_for_dic][hero_name + "_recorded_games"] += 1

            line = str(account_id) + "," + str(mmr) + ","

            for hero_dict in details_for_every_hero:

                hero_name = hero_dict[list(hero_dict.keys())[0]]
                recorded_games = hero_dict[hero_name + "_recorded_games"]
                if recorded_games != 0:
                    hero_dict[hero_name + "_gpm"] /= recorded_games
                    hero_dict[hero_name + "_xpm"] /= recorded_games
                    hero_dict[hero_name + "_kills"] /= recorded_games
                    hero_dict[hero_name + "_deaths"] /= recorded_games
                    hero_dict[hero_name + "_assists"] /= recorded_games
                    hero_dict[hero_name + "_lh"] /= recorded_games
                    hero_dict[hero_name + "_denies"] /= recorded_games
                    hero_dict[hero_name + "_level"] /= recorded_games

                line += ",".join(str(e) for e in list(hero_dict.values())[1:])
                line += ","

            f_write.write(line[:-1] + "\n")

            details_for_every_hero = initialize()

    f_write.close()


def initialize():
    properties = ["GPM", "XPM", "KILLS", "DEATHS", "ASSISTS", "LH", "DENIES", "LEVEL", "RECORDED_GAMES"]

    hero_list = []

    for hero_id in heroes.keys():
        dic = {hero_id: heroes[hero_id]}
        for prop in properties:
            dic["_".join([heroes[hero_id], prop.lower()])] = 0
        hero_list.append(dic)

    return hero_list


if __name__ == '__main__':
    main()
