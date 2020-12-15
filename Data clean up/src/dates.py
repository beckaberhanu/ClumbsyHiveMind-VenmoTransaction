import os
from pprint import pprint

# the venmo dataset only contains data for 71 unique dates
if __name__ == "__main__":
    f = open(os.path.dirname(__file__) + "/../Data/venmo.csv", "r")
    date_ind = f.readline().split(",").index("payment.date_created")
    seen = {}
    for row_ind, line in enumerate(f):
        row = line.split(",")
        if len(row) == 404:
            seen[row[date_ind][:10]] = seen.get(row[date_ind][:10], 0) + 1
            # seen.add(row[date_ind][:10])
        if row_ind % 100000 == 0:
            print(row_ind)
        # if row_ind == 1000000:
        #     break

    pprint(seen)