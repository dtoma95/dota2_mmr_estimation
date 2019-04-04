import json
import os

ROLES = ["carry", "nuker", "initiator", "disabler", "durable", "escape", "support", "pusher", "jungler"]

CARRY = [1, 113, 81, 72, 94, 10, 89, 44, 35, 67, 109, 19, 95, 73, 99, 49, 59, 54, 77, 114, 28, 18, 42,
         56, 6, 106, 41, 8, 80, 48, 82, 12, 15, 32, 11, 93, 46, 70, 63, 76, 17, 120]

NUKER = [110, 98, 11, 74, 52, 25, 26, 111, 39, 101, 105, 34, 22, 107, 16, 19, 48, 82, 88, 5, 64, 90, 31, 36,
         84, 76, 13, 45, 27, 17, 92, 30, 120, 119, 121]

INITIATOR = [2, 78, 96, 51, 7, 97, 16, 29, 41, 65, 13, 38, 69, 103, 60, 110, 14, 28, 71, 18, 19,
             83, 100, 88, 20, 33, 26, 75, 37, 120]

DISABLER = [3, 26, 13, 27, 2, 38, 78, 81, 51, 69, 49, 7, 104, 97, 60, 14, 16, 71, 18, 29, 100, 42, 41, 89,
            88, 20, 65, 5, 87, 33, 74, 84, 111, 79, 75, 112, 121]

DURABLE = [2, 99, 96, 29, 42, 102, 73, 38, 78, 81, 69, 49, 59, 54, 60, 14, 28, 18, 98, 19, 85, 10, 15, 47]

ESCAPE = [1, 113, 61, 56, 106, 10, 93, 63, 13, 39, 17, 107, 91, 114, 110, 16, 98, 62, 82, 9, 12, 32, 108, 120, 119]

SUPPORT = [91, 83, 20, 5, 50, 90, 31, 111, 112, 30, 102, 57, 40, 68, 3, 66, 87, 58, 26, 84, 86, 79, 27, 101, 119]

PUSHER = [49, 77, 61, 80, 43, 52, 53, 27, 81, 19, 89, 109, 66, 58, 33, 64, 45, 34]

JUNGLER = [66, 58, 33, 53, 2, 65]

with open("heroes.json", "r") as f:
    heroes = json.load(f)

f_write = open("data_all_roles.csv", "w")


def main():

    index_for_header = 0
    for filename in os.listdir("../../../match_details"):
        if ".json" not in filename:
            print(filename)
            continue

        fr = open("../../../match_details/" + filename, "r")
        stringo = fr.readline()
        d = json.loads(stringo)
        fr.close()

        details_for_every_role = initialize()

        if index_for_header == 0:
            header = "account_id,mmr,"
            for dic in details_for_every_role:
                header += ",".join(list(dic.keys()))
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

                        if exact_player["hero_id"] in CARRY:
                            enter_data(0, exact_player, "carry", details_for_every_role)
                        if exact_player["hero_id"] in NUKER:
                            enter_data(1, exact_player, "nuker", details_for_every_role)
                        if exact_player["hero_id"] in INITIATOR:
                            enter_data(2, exact_player, "initiator", details_for_every_role)
                        if exact_player["hero_id"] in DISABLER:
                            enter_data(3, exact_player, "disabler", details_for_every_role)
                        if exact_player["hero_id"] in DURABLE:
                            enter_data(4, exact_player, "durable", details_for_every_role)
                        if exact_player["hero_id"] in ESCAPE:
                            enter_data(5, exact_player, "escape", details_for_every_role)
                        if exact_player["hero_id"] in SUPPORT:
                            enter_data(6, exact_player, "support", details_for_every_role)
                        if exact_player["hero_id"] in PUSHER:
                            enter_data(7, exact_player, "pusher", details_for_every_role)
                        if exact_player["hero_id"] in JUNGLER:
                            enter_data(8, exact_player, "jungler", details_for_every_role)

            line = str(account_id) + "," + str(mmr) + ","

            for role_dict in details_for_every_role:

                role_name = list(role_dict.keys())[0].split("_")[0]
                recorded_games = role_dict[role_name + "_recorded_games"]
                if recorded_games != 0:
                    role_dict[role_name + "_gpm"] /= recorded_games
                    role_dict[role_name + "_xpm"] /= recorded_games
                    role_dict[role_name + "_kills"] /= recorded_games
                    role_dict[role_name + "_deaths"] /= recorded_games
                    role_dict[role_name + "_assists"] /= recorded_games
                    role_dict[role_name + "_lh"] /= recorded_games
                    role_dict[role_name + "_denies"] /= recorded_games
                    role_dict[role_name + "_level"] /= recorded_games

                line += ",".join(str(e) for e in list(role_dict.values()))
                line += ","

            f_write.write(line[:-1] + "\n")

            details_for_every_role = initialize()

    f_write.close()


def enter_data(index, player, role_name, details_for_every_role):
    details_for_every_role[index][role_name + "_gpm"] += player["gold_per_min"]
    details_for_every_role[index][role_name + "_xpm"] += player["xp_per_min"]
    details_for_every_role[index][role_name + "_kills"] += player["kills"]
    details_for_every_role[index][role_name + "_deaths"] += player["deaths"]
    details_for_every_role[index][role_name + "_assists"] += player["assists"]
    details_for_every_role[index][role_name + "_lh"] += player["last_hits"]
    details_for_every_role[index][role_name + "_denies"] += player["denies"]
    details_for_every_role[index][role_name + "_level"] += player["level"]
    details_for_every_role[index][role_name + "_recorded_games"] += 1


def initialize():
    properties = ["GPM", "XPM", "KILLS", "DEATHS", "ASSISTS", "LH", "DENIES", "LEVEL", "RECORDED_GAMES"]

    role_list = []

    for role in ROLES:
        dic = {}
        for prop in properties:
            dic["_".join([role, prop.lower()])] = 0
        role_list.append(dic)

    return role_list


if __name__ == "__main__":
    main()
