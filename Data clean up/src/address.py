import os.path
import requests
import json
from pprint import pprint
from geotext import GeoText


def update_dict(data, city, note, username):
    if username in data:
        for i in range(len(data[username])):
            if data[username][i]["city"] == city:
                if note not in data[username][i]["context"]:
                    data[username][i]["unique_freq"] = (
                        data[username][i]["unique_freq"] + 1
                    )
                data[username][i]["freq"] = data[username][i]["freq"] + 1
                data[username][i]["context"].append(note)
                break
    else:
        data[username] = [
            {"city": city, "unique_freq": 1, "freq": 1, "context": [note]}
        ]

    pass


if __name__ == "__main__":

    # r = requests.get("https://www.anywho.com/people/lena+underwood/")

    f = open(os.path.dirname(__file__) + "/../Data/venmo.csv", "r")
    header = f.readline().split(",")
    note_ind = header.index("note")
    actor_ind = header.index("payment.actor.username")
    target_ind = header.index("payment.target.user.username")
    users_loc = {}
    for (row_ind, line) in enumerate(f):
        row = line.split(",")
        if len(row) == 404:
            note = row[note_ind]
            geotext = GeoText(note, country="US")
            for city in geotext.cities:
                update_dict(users_loc, city, note, row[actor_ind])
                update_dict(users_loc, city, note, row[target_ind])
        if row_ind == 5000000:
            break
        # if len(geotext.cities) > 0:
        #     if row[actor_ind] not in users_loc:
        #         users_loc[row[actor_ind]] = []
        #     users_loc[row[actor_ind]].extend(
        #         [{"city": i, "context": note} for i in geotext.cities]
        #     )
        #     if row[target_ind] not in users_loc:
        #         users_loc[row[target_ind]] = []
        #     users_loc[row[target_ind]].extend(
        #         [{"city": i, "context": note} for i in geotext.cities]
        #     )
        # print(geotext.cities, ":", note)
    multiple_cities = {}
    for i in users_loc.items():
        x = 0
        for j in i[1]:
            x += j["unique_freq"]
        if x > 1:
            print(i[1])
            multiple_cities[i[0]] = i[1]
    # pprint(users_loc, indent=4, width=80, compact=True)
    print(",ajdbfmhsbc")
    with open("data.json", "w") as outfile:
        json.dump(multiple_cities, outfile)

    # print(len(multple_cities))
    # print(GeoText.index.cities["chicago"])
