import dota2api
import json

api = dota2api.Initialise("D20C32BC820746E3CB16D031AB2CC2F9", raw_mode=True)

def main():

    heroes = {}
    for h in api.get_heroes()["heroes"]:
        heroes[h["id"]] = "_".join(h["name"].split("_")[3:])

    items = {}
    for i in api.get_game_items()["items"]:
        if i["id"] > 300:
            print(i["id"])
        items[i["id"]] = "_".join(i["name"].split("_")[1:])

    f = open("heroes.json", "w")
    f.write(json.dumps(heroes, indent=4, sort_keys=True))
    f.close()

    f = open("items.json", "w")
    f.write(json.dumps(items, indent=4, sort_keys=True))
    f.close()


if __name__ == '__main__':
    main()
