import os.path
import json
from pprint import pprint
from geopy.geocoders import Nominatim
from geotext import GeoText


def user_to_displayname(numrows=-1):
    """
    reads the first [numrows] lines of transaction data from the venmo.csv file and returns
    a dictionary mapping a user_ids to its corresponding displayname.
    """
    user_2_name = {}
    print("user to displayname called")
    f = open(os.path.dirname(__file__) + "/../Data/venmo.csv", "r")
    for (row, line) in enumerate(f):
        cells = line.split(",")
        if len(cells) == 404 and row > 0:
            # 89th column contains the actor's (payer's) user id
            if cells[89] not in user_2_name:
                # 93rd column contains the actor's display name
                user_2_name[cells[89]] = cells[93]
            # 109th column contains the target's (receiver's) user id
            if cells[109] not in user_2_name:
                # 113rd column contains the target's display name
                user_2_name[cells[109]] = cells[113]
        if row % 100000 == 0:
            # to view progress
            print(row)
        if row == numrows:
            break
    return user_2_name


def load_user_2_neighbors_dict(input_file, num_rows=-1):
    """
    Reads data from a csv file called [input_file] and return a dictionary mapping
    each user to a list of all other users they have transacted with along with the number
    of transaction between each of the other users in the list.
    """
    f = open(os.path.dirname(__file__) + input_file, "r")
    first_row = f.readline().split(",")
    actor_id_ind = first_row.index("payment.actor.id")
    receiver_id_ind = first_row.index("payment.target.user.id")
    note_ind = first_row.index("note")
    neighbor_dict = {}
    for rw_ind, line in enumerate(f):
        row = line.split(",")
        # each row should have 404 columns otherwise the row is considered defective
        if len(row) == 404:
            actor_id = row[actor_id_ind]
            receiver_id = row[receiver_id_ind]
            # neither the actor_id, nor the reciever should be empty otherwise the row is
            # considered defective
            if actor_id != "" and receiver_id != "":
                if actor_id not in neighbor_dict:
                    neighbor_dict[actor_id] = {}
                if receiver_id not in neighbor_dict:
                    neighbor_dict[receiver_id] = {}

                neighbor_dict[actor_id][receiver_id] = (
                    neighbor_dict[actor_id].get(receiver_id, 0) + 1
                )
                neighbor_dict[receiver_id][actor_id] = (
                    neighbor_dict[receiver_id].get(actor_id, 0) + 1
                )

        if rw_ind % 100000 == 0:
            # report progress
            print("row:", rw_ind)
        if rw_ind == num_rows:
            break
    return neighbor_dict


def create_user_2_neighbors_table(input_file, out_file, num_rows=-1):
    """
    Reads a csv file called [input_file] and creates another file called [out_file]
    which maps each venmo user from the first [num_rows] rows to a list of the displaynames
    of the other venmo users (neighbors) they have transacted with.
        - The neighbors are arranged in the order of the number of transactions they have had
        with their corresponding user.
        - Every row in the file created is ordered with repect the number of neighbors that the
        particular row maps to.
    """
    neighbor_dict = load_user_2_neighbors_dict(input_file, num_rows)
    neighbor_dict = {  # sorting users in descending order of number of neighbors
        i[0]: i[1]
        for i in sorted(neighbor_dict.items(), key=lambda x: len(x[1]), reverse=True)
        if len(i[1]) > 0
    }

    f = open(os.path.dirname(__file__) + "/../Data/Scrape/" + out_file, "w")
    user_2_name = user_to_displayname()
    print("*" * 30, "Writing file", "*" * 30)
    num_lines_written = 0
    for user_id, neighbors in neighbor_dict.items():
        f.write(
            user_id
            + ","
            + user_2_name[user_id].replace('"', "")
            + "|"
            + ",".join(
                [
                    user_2_name[i[0]].replace('"', "")
                    # sorting users in descending order of number of transactions
                    for i in sorted(neighbors.items(), key=lambda x: x[1], reverse=True)
                ]
            )
            + "\n"
        )
        num_lines_written += 1
        if num_lines_written % 100000 == 0:
            print(num_lines_written)
    f.close()


category1 = [
    "rent",
    "apartment",
    "house",
    "home",
    "🏠",
    "🏡",
    "🏘️",
    "🏚️",
    "electric",
    "electricity",
    "⚡",
    "💡",
    "🔌",
    "water",
    "🚰",
    "💦",
    "💧",
    "wifi",
    "heating",
    "heat",
    "groceries",
    "grocery",
    "costco",
    "target",
    "wholefoods",
    "milk",
    "🥛",
    "oj",
    "eggs",
    "🥚",
    "🛒",
    "bill",
    "bills",
    "furniture",
    "🛋",
]
category2 = [
    "food",
    "pizza",
    "🍕",
    "🍔",
    "🍟",
    "🍜",
    "🍗",
    "🥞",
    "🌮",
    "🌭",
    "🍦",
    "🍣",
    "dinner",
    "lunch",
    "coffee",
    "☕",
    "beer" "🍺",
    "🍻",
    "🍸",
    "wine",
    "🍷",
    "restaurant",
    "🍽️",
    "🍝",
    "cafe",
    "movie",
    "🎟️",
    "🎥",
    "🎬",
    "🍿",
    "concert",
    "🎫",
    "party",
    "💃",
    "🕺",
    "uber",
    "lyft",
    "ride",
    "🚕",
    "🚖",
    "gas",
    "airbnb",
    "flight",
    "✈️",
    "🛩️",
    "🛫",
    "🛬",
]


def findCategory(note):
    """
    Accepts a string [note] as input an determines whether the note best matches a particular
    category of edges. If [note] contains more words from a particular category than others.
    The category is returned as one of the following strings
        - u2u_1: User-to-User edge of category 1
        - u2u_2: ``   `` ``   ``   `` ``       2
        - u2u_3: ``   `` ``   ``   `` ``       3
    """
    num_category1 = [0, "u2u_1"]
    num_category2 = [0, "u2u_2"]
    num_category3 = [0, "u2u_3"]
    for i in note.lower().strip(":").replace("_", " ").split(" "):
        if i in category1:
            num_category1[0] += 1
        elif i in category2:
            num_category2[0] += 1
        else:
            num_category3[0] += 1
    return max(num_category1, num_category2, num_category3)[1]


def generate_user_nodes_and_edges(
    payment_file_in, node_file_out, edge_file_out, num_rows=-1
):
    """
    Reads transaction file called [payment_file_in] and creates a csv file of user nodes called [node_file_out] and
    a csv file of user-to-user edges called [edge_file_out] meant for use in gephi.
    """
    f1 = open(os.path.dirname(__file__) + payment_file_in, "r")
    # first row contains names of columns
    first_row = f1.readline().split(",")
    actor_id_ind = first_row.index("actor_id")
    actor_name_ind = first_row.index("actor_username")

    reciver_id_ind = first_row.index("target_userid")
    reciever_name_ind = first_row.index("target_username")

    transaction_note_ind = first_row.index("note")
    transaction_freq = {}
    users = {}
    for rw_ind, line in enumerate(f1):
        row = line.split(",")
        if row[actor_id_ind] and row[reciver_id_ind]:
            key = tuple(sorted([row[actor_id_ind], row[reciver_id_ind]]))
            category = findCategory(row[transaction_note_ind])
            if key not in transaction_freq:
                transaction_freq[key] = {}
            transaction_freq[key][category] = transaction_freq[key].get(category, 0) + 1

            users[row[actor_id_ind]] = users.get(
                row[actor_id_ind], [row[actor_name_ind], 0]
            )
            users[row[actor_id_ind]][1] = users[row[actor_id_ind]][1] + 1
            users[row[reciver_id_ind]] = users.get(
                row[reciver_id_ind], [row[reciever_name_ind], 0]
            )
            users[row[reciver_id_ind]][1] = users[row[reciver_id_ind]][1] + 1

        if rw_ind == num_rows:
            break

    w1 = open(os.path.dirname(__file__) + "/../Data/Gephi/" + node_file_out, "w")
    w1.write("Id;Label;NumTransactions;Type;Latitude;Longitude\n")
    for i in users.items():
        out = i[0] + ";" + i[1][0] + ";" + str(i[1][1]) + ";User;;\n"
        w1.write(out)
    w1.close()

    # each category of edges has different weights per matching transaction
    category_2_weight = {
        "u2u_1": 20,
        "u2u_2": 10,
        "u2u_3": 4,
    }
    w2 = open(os.path.dirname(__file__) + "/../Data/Gephi/" + edge_file_out, "w")
    w2.write("Source;Target;Weight;Type;Category\n")
    for i in transaction_freq.items():
        for cat, val in i[1].items():
            ## gephi can't handle parallel edges so separating out
            ## each category of edges may be unneccassary. gephi will
            ## sum up their weights anyway.
            weight = category_2_weight[cat] * val
            out = (
                str(i[0][0])
                + ";"
                + str(i[0][1])
                + ";"
                + str(weight)
                + ';"undirected";'
                + cat
                + "\n"
            )
            w2.write(out)
    w2.close()


def findLocations(note, geo_cache, geolocator):
    """
    Accepts a string called [note] and returns the coordinates of all possible geographical locations
    mention in it. Function also accepts a geopy - Geolocator object and a dictionary called [geo_cache]
    for all previuosly encoutered locations -- geopy is too slow.
    """
    geotext = GeoText(note)
    out = {}
    for city in geotext.cities:
        # if [country] already in geo_cache, don't bother using the geolocator
        if city in geo_cache:
            loc = geo_cache[city]
        else:
            geo_cache[city] = geolocator.geocode(city)
            loc = geo_cache[city]
        out[city] = (loc.latitude, loc.longitude)
    for country in geotext.countries:
        # if [country] already in geo_cache, don't bother using the geolocator
        if country in geo_cache:
            loc = geo_cache[country]
        else:
            geo_cache[country] = geolocator.geocode(country)
            loc = geo_cache[country]
        out[country] = (loc.latitude, loc.longitude)
    return out


def generate_loc_nodes_and_edges(
    payment_file_in, location_file_in, node_file_out, edge_file_out, num_rows=-1
):
    """
    Reads a venmo transaction file called [payment_file_in] (csv) and a user-to-location file called
    [location_file_in] (tsv) to creates a csv file of location nodes called [node_file_out] and
    a csv file of user-to-location edges called [edge_file_out] meant for use in gephi.

    There are two categories of edges
        - u2l_1: User-to-Location edge determined from users facebook profile
        - u2l_2: ``   `` ``   ``  ``   ``         ``   location mentioned in transaction notes
    """
    f1 = open(os.path.dirname(__file__) + location_file_in, "r")
    location_data = {}
    user_2_loc = {}
    geo_cache = {}
    geolocator = Nominatim(user_agent="beckageleto@gmail.com")
    unique_id = 0
    print("*" * 20, "Stage 1", "*" * 20)
    for rw_ind, line in enumerate(f1):
        row = line.split("\t")
        geo_cache[row[1]] = geo_cache.get(row[1], geolocator.geocode(row[1]))
        loc = geo_cache[row[1]]
        latlong = (loc.latitude, loc.longitude)
        if latlong not in location_data:
            location_data[latlong] = {
                "Id": unique_id,
                "Name": row[1],
                "Num_transactions": 0,
            }
            unique_id += 1
        location_data[latlong]["Num_transactions"] += 1
        locId = location_data[latlong]["Id"]
        user_2_loc[(row[0], locId)] = {
            "u2l_1": row[-1],
            # row[-1] is the represents certainity in the user's location
            # also refered to as match_count when scraping data
        }
        if rw_ind % 3 == 0:
            print(rw_ind)
    f1.close()

    f2 = open(os.path.dirname(__file__) + payment_file_in, "r")
    first_row = f2.readline().split(",")
    actor_id_ind = first_row.index("actor_id")

    target_id_ind = first_row.index("target_userid")

    transaction_note_ind = first_row.index("note")
    print("*" * 20, "Stage 2", "*" * 20)
    for rw_ind, line in enumerate(f2):
        row = line.split(",")
        actor_id = row[actor_id_ind]
        target_id = row[target_id_ind]
        note = row[transaction_note_ind]
        locations = findLocations(note, geo_cache, geolocator)
        for location in locations.items():
            if location[1] not in location_data:
                location_data[location[1]] = {
                    "Id": unique_id,
                    "Name": location[0],
                    "Num_transactions": 0,
                }
                unique_id += 1
            location_data[location[1]]["Num_transactions"] += 1
            locId = location_data[location[1]]["Id"]
            if (actor_id, locId) not in user_2_loc:
                user_2_loc[(actor_id, locId)] = {}
            user_2_loc[(actor_id, locId)]["u2l_2"] = (
                user_2_loc[(actor_id, locId)].get("u2l_2", 0) + 1
            )
            if (target_id, locId) not in user_2_loc:
                user_2_loc[(target_id, locId)] = {}
            user_2_loc[(target_id, locId)]["u2l_2"] = (
                user_2_loc[(target_id, locId)].get("u2l_2", 0) + 1
            )
        if rw_ind % 1000 == 0:
            print(rw_ind)
        if rw_ind == num_rows:
            break

    w1 = open(os.path.dirname(__file__) + "/../Data/Gephi/" + node_file_out, "w")
    w1.write(
        "Id;Label;NumTransactions;Type;Latitude;Longitude\n"
    )  # columns for gephi node file
    for latlong, data in location_data.items():
        out = [
            str(data["Id"]),
            data["Name"],
            str(data["Num_transactions"]),
            "Location",
            str(latlong[0]),
            str(latlong[1]),
        ]
        w1.write(";".join(out) + "\n")
    w1.close()

    # each category of edges has different weights
    category_2_weight = {
        "u2l_1": 40,
        "u2l_2": 5,
    }
    w2 = open(os.path.dirname(__file__) + "/../Data/Gephi/" + edge_file_out, "w")
    w2.write("Source;Target;Weight;Type;Category\n")  # columns for gephi edge file
    for user_loc, data in user_2_loc.items():
        for cat, val in data.items():
            weight = category_2_weight[cat] * val
            out = [
                user_loc[0],
                str(user_loc[1]),
                str(weight),
                '"undirected"',
                cat,
            ]
            w2.write(";".join(out) + "\n")
    w2.close()


def scaleWeights(input_file, scale=1, power=1):
    f = open(os.path.dirname(__file__) + input_file, "r")
    firstline = f.readline()
    weight_ind = firstline.split(";").index("Weight")
    rows = []
    for i in f:
        row = i.split(";")
        row[weight_ind] = str((float(row[weight_ind]) ** power) * scale)
        rows.append(row)
    f.close()
    w = open(os.path.dirname(__file__) + input_file, "w")
    w.write(firstline)
    for i in rows:
        w.write(";".join(i))
    w.close()


if __name__ == "__main__":
    scaleWeights("/../Data/Gephi/loc_edges_gephi.csv", scale=100, power=1)
    # scaleWeights("user_edges_gephi.csv", scale = 1, power = 1)
    # generate_user_nodes_and_edges(
    #     "/../Data/venmo_freq_triaged.csv",
    #     "user_nodes_gephi.csv",
    #     "user_edges_gephi.csv",
    # )
    # generate_loc_nodes_and_edges(
    #     "/../Data/venmo_freq_triaged.csv",
    #     "/../Data/Scrape/user_location.tsv",
    #     "loc_nodes_gephi.csv",
    #     "loc_edges_gephi.csv",
    # )
    # load_user_neighbors("/../Data/venmo.csv", "neighbors2.txt")
