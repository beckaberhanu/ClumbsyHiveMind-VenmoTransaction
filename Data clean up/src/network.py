import os.path
import json
from pprint import pprint


def generate_nodes_and_edges(input_file, node_file, edge_file):
    f = open(os.path.dirname(__file__) + input_file, "r")
    first_row = f.readline().split(",")
    actor_id_ind = first_row.index("payment.actor.id")
    actor_name_ind = first_row.index("payment.actor.username")

    reciver_id_ind = first_row.index("payment.target.user.id")
    reciever_name_ind = first_row.index("payment.target.user.username")

    transaction_freq = {}
    users = {}
    for rw_ind, line in enumerate(f):
        row = line.split(",")
        if len(row) == 404:
            if row[actor_id_ind] and row[reciver_id_ind]:
                key = tuple(sorted([row[actor_id_ind], row[reciver_id_ind]]))
                transaction_freq[key] = transaction_freq.get(key, 0) + 1

                users[row[actor_id_ind]] = users.get(
                    row[actor_id_ind], [row[actor_name_ind], 0]
                )
                users[row[reciver_id_ind]] = users.get(
                    row[reciver_id_ind], [row[reciever_name_ind], 0]
                )
                users[row[reciver_id_ind]][1] = users[row[reciver_id_ind]][1] + 1
                users[row[actor_id_ind]][1] = users[row[actor_id_ind]][1] + 1

        if rw_ind == num_rows:
            break
    newDict = {key: value for key, value in transaction_freq.items() if value > 2}
    # pprint(users, indent=4)

    w1 = open(os.path.dirname(__file__) + "/../Data/Gephi/" + node_file, "w")
    w1.write("Id,Label,NumTransactions\n")
    for i in users.items():
        out = i[0] + "," + i[1][0] + "," + str(i[1][1]) + "\n"
        w1.write(out)
    w1.close()

    w2 = open(os.path.dirname(__file__) + "/../Data/Gephi/" + edge_file, "w")
    w2.write("Source,Target,Weight,Type\n")
    for i in transaction_freq.items():
        out = str(i[0][0]) + "," + str(i[0][1]) + "," + str(i[1]) + ',"undirected"\n'
        w2.write(out)
    w2.close()


def user_to_displayname(numrows=-1):
    user_2_name = {}
    print("user to displayname called")
    f = open(os.path.dirname(__file__) + "/../Data/venmo.csv", "r")
    for (row, line) in enumerate(f):
        cells = line.split(",")
        if len(cells) == 404 and row > 0:
            if cells[89] not in user_2_name:
                user_2_name[cells[89]] = cells[93]
            if cells[109] not in user_2_name:
                user_2_name[cells[109]] = cells[113]
        if row % 100000 == 0:
            print(row)
        if row == numrows:
            break
    return user_2_name


def load_user_neighbors(input_file, out_file, num_rows=-1):
    f = open(os.path.dirname(__file__) + input_file, "r")
    first_row = f.readline().split(",")
    actor_id_ind = first_row.index("payment.actor.id")
    receiver_id_ind = first_row.index("payment.target.user.id")

    neighbor_dict = {}
    for rw_ind, line in enumerate(f):
        row = line.split(",")
        if len(row) == 404:
            actor_id = row[actor_id_ind]
            receiver_id = row[receiver_id_ind]

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
            print("row:", rw_ind)
        if rw_ind == num_rows:
            break

    neighbor_dict = {
        i[0]: i[1]
        for i in sorted(neighbor_dict.items(), key=lambda x: len(x[1]), reverse=True)
        if len(i[1]) > 0
    }

    f = open(os.path.dirname(__file__) + "/../Data/Scrape/" + out_file, "w")
    user_2_name = user_to_displayname()
    print("*" * 30, "Writing file", "*" * 30)
    num_lines_written = 0
    for key, val in neighbor_dict.items():
        f.write(
            key
            + ","
            + user_2_name[key]
            + "|"
            + ",".join(
                [
                    user_2_name[i[0]]
                    for i in sorted(val.items(), key=lambda x: x[1], reverse=True)
                ]
            )
            + "\n"
        )
        num_lines_written += 1
        if num_lines_written % 100000 == 0:
            print(num_lines_written)
    f.close()

    # with open(out_file, "w") as outfile:
    #     json.dump(neighbor_dict, outfile)

    # return neighbor_dict


# def load_user_data(input_file):

if __name__ == "__main__":
    # generate_nodes_and_edges(
    #     "/../Data/venmo.csv", "nodes_gephi.csv", "edges_gephi.csv", 100000
    # )
    load_user_neighbors("/../Data/venmo.csv", "neighbors2.txt")
