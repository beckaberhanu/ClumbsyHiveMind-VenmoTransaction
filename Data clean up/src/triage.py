import os.path
import sys

columns = {
    "_id": 0,
    "date_updated": 1,
    "transfer": 2,
    "app.description": 3,
    "app.site_url": 4,
    "app.image_url": 5,
    "app.id": 6,
    "app.name": 7,
    "comments.count": 8,
    "comments.data.0.date_created": 9,
    "comments.data.0.message": 10,
    "comments.data.0.mentions.count": 11,
    "comments.data.0.mentions.data.0.username": 12,
    "comments.data.0.mentions.data.0.user.username": 13,
    "comments.data.0.mentions.data.0.user.about": 14,
    "comments.data.0.mentions.data.0.user.last_name": 15,
    "comments.data.0.mentions.data.0.user.display_name": 16,
    "comments.data.0.mentions.data.0.user.friends_count": 17,
    "comments.data.0.mentions.data.0.user.is_group": 18,
    "comments.data.0.mentions.data.0.user.is_active": 19,
    "comments.data.0.mentions.data.0.user.trust_request": 20,
    "comments.data.0.mentions.data.0.user.email": 21,
    "comments.data.0.mentions.data.0.user.phone": 22,
    "comments.data.0.mentions.data.0.user.profile_picture_url": 23,
    "comments.data.0.mentions.data.0.user.first_name": 24,
    "comments.data.0.mentions.data.0.user.friend_status": 25,
    "comments.data.0.mentions.data.0.user.is_blocked": 26,
    "comments.data.0.mentions.data.0.user.id": 27,
    "comments.data.0.mentions.data.0.user.identity": 28,
    "comments.data.0.mentions.data.0.user.date_joined": 29,
    "comments.data.0.id": 30,
    "comments.data.0.user.username": 31,
    "comments.data.0.user.last_name": 32,
    "comments.data.0.user.friends_count": 33,
    "comments.data.0.user.is_group": 34,
    "comments.data.0.user.is_active": 35,
    "comments.data.0.user.trust_request": 36,
    "comments.data.0.user.phone": 37,
    "comments.data.0.user.profile_picture_url": 38,
    "comments.data.0.user.is_blocked": 39,
    "comments.data.0.user.id": 40,
    "comments.data.0.user.identity": 41,
    "comments.data.0.user.date_joined": 42,
    "comments.data.0.user.about": 43,
    "comments.data.0.user.display_name": 44,
    "comments.data.0.user.first_name": 45,
    "comments.data.0.user.friend_status": 46,
    "comments.data.0.user.email": 47,
    "comments.data.1.user.username": 48,
    "comments.data.1.user.about": 49,
    "comments.data.1.user.last_name": 50,
    "comments.data.1.user.display_name": 51,
    "comments.data.1.user.friends_count": 52,
    "comments.data.1.user.is_group": 53,
    "comments.data.1.user.is_active": 54,
    "comments.data.1.user.trust_request": 55,
    "comments.data.1.user.email": 56,
    "comments.data.1.user.phone": 57,
    "comments.data.1.user.profile_picture_url": 58,
    "comments.data.1.user.first_name": 59,
    "comments.data.1.user.friend_status": 60,
    "comments.data.1.user.is_blocked": 61,
    "comments.data.1.user.id": 62,
    "comments.data.1.user.identity": 63,
    "comments.data.1.user.date_joined": 64,
    "comments.data.1.date_created": 65,
    "comments.data.1.message": 66,
    "comments.data.1.id": 67,
    "comments.data.1.mentions.count": 68,
    "comments.data.1.mentions.data": 69,
    "payment.status": 70,
    "payment.id": 71,
    "payment.date_authorized": 72,
    "payment.merchant_split_purchase.authorization_id": 73,
    "payment.merchant_split_purchase.merchant_name": 74,
    "payment.date_completed": 75,
    # I think transactions with merchants might all be private
    "payment.target.merchant": 76,
    "payment.target.redeemable_target.type": 77,
    "payment.target.redeemable_target.display_name": 78,
    "payment.target.phone": 79,
    "payment.target.user.username": 80,
    "payment.target.user.last_name": 81,
    "payment.target.user.friends_count": 82,
    "payment.target.user.is_group": 83,
    "payment.target.user.is_active": 84,
    "payment.target.user.trust_request": 85,
    "payment.target.user.phone": 86,
    "payment.target.user.profile_picture_url": 87,
    "payment.target.user.is_blocked": 88,
    "payment.target.user.id": 89,
    "payment.target.user.identity": 90,
    "payment.target.user.date_joined": 91,
    "payment.target.user.about": 92,
    "payment.target.user.display_name": 93,
    "payment.target.user.first_name": 94,
    "payment.target.user.friend_status": 95,
    "payment.target.user.email": 96,
    # 'user', 'phone', 'redeemable' or 'email', this columns only ever contains phone, redeemable or email when the transaction is pending. Not sure why.
    "payment.target.type": 97,
    "payment.target.email": 98,
    "payment.audience": 99,
    "payment.actor.username": 100,
    "payment.actor.last_name": 101,
    "payment.actor.friends_count": 102,
    "payment.actor.is_group": 103,
    "payment.actor.is_active": 104,
    "payment.actor.trust_request": 105,
    "payment.actor.phone": 106,
    "payment.actor.profile_picture_url": 107,
    "payment.actor.is_blocked": 108,
    "payment.actor.id": 109,
    "payment.actor.identity": 110,
    "payment.actor.date_joined": 111,
    "payment.actor.about": 112,
    "payment.actor.display_name": 113,
    "payment.actor.first_name": 114,
    "payment.actor.friend_status": 115,
    "payment.actor.email": 116,
    "payment.actor.is_groep": 117,
    "payment.note": 118,
    "payment.amount": 119,
    "payment.action": 120,
    "payment.date_created": 121,
    "payment.date_reminded": 122,
    "note": 123,
    "audience": 124,
    "likes.count": 125,
    "likes.data.0.username": 126,
    "likes.data.0.last_name": 127,
    "likes.data.0.friends_count": 128,
    "likes.data.0.is_group": 129,
    "likes.data.0.is_active": 130,
    "likes.data.0.trust_request": 131,
    "likes.data.0.phone": 132,
    "likes.data.0.profile_picture_url": 133,
    "likes.data.0.is_blocked": 134,
    "likes.data.0.id": 135,
    "likes.data.0.identity": 136,
    "likes.data.0.date_joined": 137,
    "likes.data.0.about": 138,
    "likes.data.0.display_name": 139,
    "likes.data.0.first_name": 140,
    "likes.data.0.friend_status": 141,
    "likes.data.0.email": 142,
    "likes.data.1.username": 143,
    "likes.data.1.about": 144,
    "likes.data.1.last_name": 145,
    "likes.data.1.display_name": 146,
    "likes.data.1.friends_count": 147,
    "likes.data.1.is_group": 148,
    "likes.data.1.is_active": 149,
    "likes.data.1.trust_request": 150,
    "likes.data.1.email": 151,
    "likes.data.1.phone": 152,
    "likes.data.1.profile_picture_url": 153,
    "likes.data.1.first_name": 154,
    "likes.data.1.friend_status": 155,
    "likes.data.1.is_blocked": 156,
    "likes.data.1.id": 157,
    "likes.data.1.identity": 158,
    "likes.data.1.date_joined": 159,
    "mentions.count": 160,
    "mentions.data.0.username": 161,
    "mentions.data.0.user.username": 162,
    "mentions.data.0.user.last_name": 163,
    "mentions.data.0.user.friends_count": 164,
    "mentions.data.0.user.is_group": 165,
    "mentions.data.0.user.is_active": 166,
    "mentions.data.0.user.trust_request": 167,
    "mentions.data.0.user.phone": 168,
    "mentions.data.0.user.profile_picture_url": 169,
    "mentions.data.0.user.is_blocked": 170,
    "mentions.data.0.user.id": 171,
    "mentions.data.0.user.identity": 172,
    "mentions.data.0.user.date_joined": 173,
    "mentions.data.0.user.about": 174,
    "mentions.data.0.user.display_name": 175,
    "mentions.data.0.user.first_name": 176,
    "mentions.data.0.user.friend_status": 177,
    "mentions.data.0.user.email": 178,
    "mentions.data.1.username": 179,
    "mentions.data.1.user.username": 180,
    "mentions.data.1.user.last_name": 181,
    "mentions.data.1.user.friends_count": 182,
    "mentions.data.1.user.is_group": 183,
    "mentions.data.1.user.is_active": 184,
    "mentions.data.1.user.trust_request": 185,
    "mentions.data.1.user.phone": 186,
    "mentions.data.1.user.profile_picture_url": 187,
    "mentions.data.1.user.is_blocked": 188,
    "mentions.data.1.user.id": 189,
    "mentions.data.1.user.identity": 190,
    "mentions.data.1.user.date_joined": 191,
    "mentions.data.1.user.about": 192,
    "mentions.data.1.user.display_name": 193,
    "mentions.data.1.user.first_name": 194,
    "mentions.data.1.user.friend_status": 195,
    "mentions.data.1.user.email": 196,
    "mentions.data.2.user.display_name": 197,
    "mentions.data.2.user.friends_count": 198,
    "mentions.data.2.user.username": 199,
    "mentions.data.2.user.date_joined": 200,
    "mentions.data.2.user.friend_status": 201,
    "mentions.data.2.user.phone": 202,
    "mentions.data.2.user.last_name": 203,
    "mentions.data.2.user.is_blocked": 204,
    "mentions.data.2.user.profile_picture_url": 205,
    "mentions.data.2.user.is_group": 206,
    "mentions.data.2.user.identity": 207,
    "mentions.data.2.user.email": 208,
    "mentions.data.2.user.is_active": 209,
    "mentions.data.2.user.id": 210,
    "mentions.data.2.user.first_name": 211,
    "mentions.data.2.user.about": 212,
    "mentions.data.2.user.trust_request": 213,
    "mentions.data.2.username": 214,
    "mentions.data.3.username": 215,
    "mentions.data.3.user.username": 216,
    "mentions.data.3.user.about": 217,
    "mentions.data.3.user.last_name": 218,
    "mentions.data.3.user.display_name": 219,
    "mentions.data.3.user.friends_count": 220,
    "mentions.data.3.user.is_group": 221,
    "mentions.data.3.user.is_active": 222,
    "mentions.data.3.user.trust_request": 223,
    "mentions.data.3.user.email": 224,
    "mentions.data.3.user.phone": 225,
    "mentions.data.3.user.profile_picture_url": 226,
    "mentions.data.3.user.first_name": 227,
    "mentions.data.3.user.friend_status": 228,
    "mentions.data.3.user.is_blocked": 229,
    "mentions.data.3.user.id": 230,
    "mentions.data.3.user.identity": 231,
    "mentions.data.3.user.date_joined": 232,
    "mentions.data.4.username": 233,
    "mentions.data.4.user.username": 234,
    "mentions.data.4.user.about": 235,
    "mentions.data.4.user.last_name": 236,
    "mentions.data.4.user.display_name": 237,
    "mentions.data.4.user.friends_count": 238,
    "mentions.data.4.user.is_group": 239,
    "mentions.data.4.user.is_active": 240,
    "mentions.data.4.user.trust_request": 241,
    "mentions.data.4.user.email": 242,
    "mentions.data.4.user.phone": 243,
    "mentions.data.4.user.profile_picture_url": 244,
    "mentions.data.4.user.first_name": 245,
    "mentions.data.4.user.friend_status": 246,
    "mentions.data.4.user.is_blocked": 247,
    "mentions.data.4.user.id": 248,
    "mentions.data.4.user.identity": 249,
    "mentions.data.4.user.date_joined": 250,
    "mentions.data.5.username": 251,
    "mentions.data.5.user.username": 252,
    "mentions.data.5.user.about": 253,
    "mentions.data.5.user.last_name": 254,
    "mentions.data.5.user.display_name": 255,
    "mentions.data.5.user.friends_count": 256,
    "mentions.data.5.user.is_group": 257,
    "mentions.data.5.user.is_active": 258,
    "mentions.data.5.user.trust_request": 259,
    "mentions.data.5.user.email": 260,
    "mentions.data.5.user.phone": 261,
    "mentions.data.5.user.profile_picture_url": 262,
    "mentions.data.5.user.first_name": 263,
    "mentions.data.5.user.friend_status": 264,
    "mentions.data.5.user.is_blocked": 265,
    "mentions.data.5.user.id": 266,
    "mentions.data.5.user.identity": 267,
    "mentions.data.5.user.date_joined": 268,
    "mentions.data.6.username": 269,
    "mentions.data.6.user.username": 270,
    "mentions.data.6.user.about": 271,
    "mentions.data.6.user.last_name": 272,
    "mentions.data.6.user.display_name": 273,
    "mentions.data.6.user.friends_count": 274,
    "mentions.data.6.user.is_group": 275,
    "mentions.data.6.user.is_active": 276,
    "mentions.data.6.user.trust_request": 277,
    "mentions.data.6.user.email": 278,
    "mentions.data.6.user.phone": 279,
    "mentions.data.6.user.profile_picture_url": 280,
    "mentions.data.6.user.first_name": 281,
    "mentions.data.6.user.friend_status": 282,
    "mentions.data.6.user.is_blocked": 283,
    "mentions.data.6.user.id": 284,
    "mentions.data.6.user.identity": 285,
    "mentions.data.6.user.date_joined": 286,
    "mentions.data.7.username": 287,
    "mentions.data.7.user.username": 288,
    "mentions.data.7.user.about": 289,
    "mentions.data.7.user.last_name": 290,
    "mentions.data.7.user.display_name": 291,
    "mentions.data.7.user.friends_count": 292,
    "mentions.data.7.user.is_group": 293,
    "mentions.data.7.user.is_active": 294,
    "mentions.data.7.user.trust_request": 295,
    "mentions.data.7.user.email": 296,
    "mentions.data.7.user.phone": 297,
    "mentions.data.7.user.profile_picture_url": 298,
    "mentions.data.7.user.first_name": 299,
    "mentions.data.7.user.friend_status": 300,
    "mentions.data.7.user.is_blocked": 301,
    "mentions.data.7.user.id": 302,
    "mentions.data.7.user.identity": 303,
    "mentions.data.7.user.date_joined": 304,
    "mentions.data.8.username": 305,
    "mentions.data.8.user.username": 306,
    "mentions.data.8.user.about": 307,
    "mentions.data.8.user.last_name": 308,
    "mentions.data.8.user.display_name": 309,
    "mentions.data.8.user.friends_count": 310,
    "mentions.data.8.user.is_group": 311,
    "mentions.data.8.user.is_active": 312,
    "mentions.data.8.user.trust_request": 313,
    "mentions.data.8.user.email": 314,
    "mentions.data.8.user.phone": 315,
    "mentions.data.8.user.profile_picture_url": 316,
    "mentions.data.8.user.first_name": 317,
    "mentions.data.8.user.friend_status": 318,
    "mentions.data.8.user.is_blocked": 319,
    "mentions.data.8.user.id": 320,
    "mentions.data.8.user.identity": 321,
    "mentions.data.8.user.date_joined": 322,
    "mentions.data.9.username": 323,
    "mentions.data.9.user.username": 324,
    "mentions.data.9.user.about": 325,
    "mentions.data.9.user.last_name": 326,
    "mentions.data.9.user.display_name": 327,
    "mentions.data.9.user.friends_count": 328,
    "mentions.data.9.user.is_group": 329,
    "mentions.data.9.user.is_active": 330,
    "mentions.data.9.user.trust_request": 331,
    "mentions.data.9.user.email": 332,
    "mentions.data.9.user.phone": 333,
    "mentions.data.9.user.profile_picture_url": 334,
    "mentions.data.9.user.first_name": 335,
    "mentions.data.9.user.friend_status": 336,
    "mentions.data.9.user.is_blocked": 337,
    "mentions.data.9.user.id": 338,
    "mentions.data.9.user.identity": 339,
    "mentions.data.9.user.date_joined": 340,
    "mentions.data.10.username": 341,
    "mentions.data.10.user.username": 342,
    "mentions.data.10.user.last_name": 343,
    "mentions.data.10.user.friends_count": 344,
    "mentions.data.10.user.is_group": 345,
    "mentions.data.10.user.is_active": 346,
    "mentions.data.10.user.trust_request": 347,
    "mentions.data.10.user.phone": 348,
    "mentions.data.10.user.profile_picture_url": 349,
    "mentions.data.10.user.is_blocked": 350,
    "mentions.data.10.user.id": 351,
    "mentions.data.10.user.identity": 352,
    "mentions.data.10.user.date_joined": 353,
    "mentions.data.10.user.about": 354,
    "mentions.data.10.user.display_name": 355,
    "mentions.data.10.user.first_name": 356,
    "mentions.data.10.user.friend_status": 357,
    "mentions.data.10.user.email": 358,
    "date_created": 359,
    "type": 360,
    "id": 361,
    "authorization.created_at": 362,
    "authorization.amount": 363,
    "authorization.authorization_types": 364,
    "authorization.user.username": 365,
    "authorization.user.friends_count": 366,
    "authorization.user.is_active": 367,
    "authorization.user.display_name": 368,
    "authorization.user.friend_status": 369,
    "authorization.user.email": 370,
    "authorization.user.first_name": 371,
    "authorization.user.identity": 372,
    "authorization.user.last_name": 373,
    "authorization.user.is_blocked": 374,
    "authorization.user.about": 375,
    "authorization.user.profile_picture_url": 376,
    "authorization.user.id": 377,
    "authorization.user.phone": 378,
    "authorization.user.trust_request": 379,
    "authorization.user.date_joined": 380,
    "authorization.user.is_group": 381,
    "authorization.story_id": 382,
    "authorization.payment_method": 383,
    "authorization.point_of_sale.city": 384,
    "authorization.point_of_sale.state": 385,
    "authorization.is_venmo_card": 386,
    "authorization.descriptor": 387,
    "authorization.status": 388,
    "authorization.merchant.image_url": 389,
    "authorization.merchant.display_name": 390,
    "authorization.merchant.id": 391,
    "authorization.merchant.image_datetime_updated": 392,
    "authorization.merchant.datetime_created": 393,
    "authorization.merchant.braintree_merchant_id": 394,
    "authorization.merchant.paypal_merchant_id": 395,
    "authorization.merchant.datetime_updated": 396,
    "authorization.acknowledged": 397,
    "authorization.decline": 398,
    "authorization.id": 399,
    "authorization.captures": 400,
    "authorization.atm_fees": 401,
    "auto_auth_story": 402,
    "user_shared_auth": 403,
}


def check_total_num_rows(filename):
    print("check total num rows called")
    fileloc = os.path.dirname(__file__) + "/" + filename
    f = open(fileloc, "r")

    out = 0
    for row in f:
        out += 1
        if out % 100000 == 0:
            print(out)

    f.close()
    print("final:", out)


def check_total_num_payment_rows(filename):
    print("check total num payment rows called")
    fileloc = os.path.dirname(__file__) + "/" + filename
    f = open(fileloc, "r")

    out = 0
    min_ = sys.float_info.max
    for (ind, row) in enumerate(f):
        cells = row.split(",")
        if len(cells) == 404:
            if len(cells[71]) > 2:
                if ind > 0:
                    if min_ > float(cells[71]):
                        min_ = float(cells[71])
                out += 1
        if out % 100000 == 0:
            print(out)

    f.close()
    print("min:", min_)
    print("final:", out)


def check_total_num_comment_rows(filename):
    print("check total num comment rows called")
    fileloc = os.path.dirname(__file__) + "/" + filename
    f = open(fileloc, "r")

    out = 0
    out1 = 0
    for (ind, row) in enumerate(f):
        cells = row.split(",")
        if len(cells) == 404:
            if ind > 0:
                if len(cells[10]) > 2:
                    out += 1
                    # print(cells[10])
                if len(cells[8]) > 0:
                    out1 += int(cells[8])
                    # print(cells[10])
        if ind % int(7000000 * 0.01) == 0:
            print(
                round((ind / 7000000) * 100), "% complete | out:", out, " | out1:", out1
            )
    f.close()
    print("final:", out)


def check_total_num_valid_rows(filename):
    print("check valid num rows called")
    fileloc = os.path.dirname(__file__) + "/" + filename
    f = open(fileloc, "r")

    out = 0
    for row in f:
        if len(row.split(",")) == 404:
            out += 1
            if out % 100000 == 0:
                print(out)
    f.close()
    print("final:", out)


def check_total_num_category_rows(filename, category):
    print("check total num rows called")
    category = set(category)
    fileloc = os.path.dirname(__file__) + "/" + filename
    f = open(fileloc, "r")
    firstline = f.readline()
    note_ind = firstline.split(",").index("note")
    total_num = 0
    for row_ind, line in enumerate(f):
        row = line.split(",")
        if len(row) == 404:
            for i in row[note_ind].lower().strip(":").replace("_", " ").split(" "):
                if i in category:
                    # print(row_ind, ":", row[note_ind])
                    total_num += 1
                    break
        if row_ind % 100000 == 0:
            print(row_ind)
    print("Total:", total_num)
    f.close()


likes_csv = [
    {
        "payment.id": 71,
        "likes.data.0.id": 135,
        "likes.data.0.username": 126,
        "app.name": 7,
        "app.id": 6,
    },
    {
        "payment.id": 71,
        "likes.data.1.id": 157,
        "likes.data.1.username": 143,
        "app.name": 7,
        "app.id": 6,
    },
]


def get_likes_csv(filename, outname, num_rows):
    print(
        "get_likes_csv function called, writing to:",
        outname,
        "| number of rows being read",
        num_rows,
    )
    fileloc = os.path.dirname(__file__) + "/" + filename
    f = open(fileloc, "r")

    csv_out = ""
    for (row, line) in enumerate(f):
        cells = line.split(",")
        csv_row = []
        if len(cells) == 404 and row > 0:
            if len(cells[135]) > 0:  # check if comment.data.0.id exists
                for index in likes_csv[0].values():
                    csv_row.append(cells[index])
                csv_out += ",".join(csv_row) + "\n"
                csv_row = []
            if len(cells[157]) > 0:  # check if comment.data.1.id exists
                for index in likes_csv[1].values():
                    csv_row.append(cells[index])
                csv_out += ",".join(csv_row) + "\n"
        elif row == 0:
            csv_out += (
                ",".join(["payment_id", "user_id", "username", "app.name", "app.id"])
                + "\n"
            )
        if row == num_rows:
            break
        if row % int(num_rows * 0.01) == 0:
            print(round((row / num_rows) * 100), "% complete")
    f.close()
    outloc = os.path.dirname(__file__) + "/" + outname
    w = open(outloc, "w")
    w.write(csv_out)
    w.close()


user_csv = [
    {
        "payment.target.user.id": 89,
        "payment.target.user.username": 80,
        "payment.target.user.first_name": 94,
        "payment.target.user.last_name": 81,
        "payment.target.user.display_name": 93,
    },
    {
        "payment.actor.id": 109,
        "payment.actor.username": 100,
        "payment.actor.first_name": 114,
        "payment.actor.last_name": 101,
        "payment.actor.display_name": 113,
    },
    {
        "likes.data.0.id": 135,
        "likes.data.0.username": 126,
        "likes.data.0.first_name": 140,
        "likes.data.0.last_name": 127,
        "likes.data.0.display_name": 139,
    },
    {
        "likes.data.1.id": 157,
        "likes.data.1.username": 143,
        "likes.data.1.first_name": 154,
        "likes.data.1.last_name": 145,
        "likes.data.1.display_name": 146,
    },
    {
        "comments.data.0.user.id": 40,
        "comments.data.0.user.username": 31,
        "comments.data.0.user.first_name": 45,
        "comments.data.0.user.last_name": 32,
        "comments.data.0.user.display_name": 44,
    },
    {
        "comments.data.1.user.id": 62,
        "comments.data.1.user.username": 48,
        "comments.data.1.user.first_name": 59,
        "comments.data.1.user.last_name": 50,
        "comments.data.1.user.display_name": 51,
    },
    {
        "comments.data.0.mentions.data.0.user.id": 27,
        "comments.data.0.mentions.data.0.user.username": 13,
        "comments.data.0.mentions.data.0.user.first_name": 24,
        "comments.data.0.mentions.data.0.user.last_name": 15,
        "comments.data.0.mentions.data.0.user.display_name": 16,
    },
    {
        "mentions.data.0.user.id": 171,
        "mentions.data.0.user.username": 162,
        "mentions.data.0.user.first_name": 176,
        "mentions.data.0.user.last_name": 163,
        "mentions.data.0.user.display_name": 175,
    },
    {
        "mentions.data.1.user.id": 189,
        "mentions.data.1.user.username": 180,
        "mentions.data.1.user.first_name": 194,
        "mentions.data.1.user.last_name": 181,
        "mentions.data.1.user.display_name": 193,
    },
    {
        "mentions.data.2.user.id": 210,
        "mentions.data.2.user.username": 199,
        "mentions.data.2.user.first_name": 211,
        "mentions.data.2.user.last_name": 203,
        "mentions.data.2.user.display_name": 197,
    },
    {
        "mentions.data.3.user.id": 230,
        "mentions.data.3.user.username": 216,
        "mentions.data.3.user.first_name": 227,
        "mentions.data.3.user.last_name": 218,
        "mentions.data.3.user.display_name": 219,
    },
    {
        "mentions.data.4.user.id": 248,
        "mentions.data.4.user.username": 234,
        "mentions.data.4.user.first_name": 245,
        "mentions.data.4.user.last_name": 236,
        "mentions.data.4.user.display_name": 237,
    },
]


def get_users_csv(filename, outname, num_rows):
    print(
        "get_users_csv function called, writing to:",
        outname,
        "| number of rows being read",
        num_rows,
    )
    fileloc = os.path.dirname(__file__) + "/" + filename
    f = open(fileloc, "r")

    csv_out = ""
    seen = set()
    numrows = 0
    for (row, line) in enumerate(f):
        cells = line.split(",")
        if len(cells) == 404 and row > 0:
            for i in user_csv:
                csv_row = []
                indeces = list(i.values())
                if (len(cells[indeces[0]]) > 0) and (cells[indeces[0]] not in seen):
                    for index in indeces:
                        csv_row.append(cells[index])
                    csv_out += ",".join(csv_row) + "\n"
                    seen.add(cells[indeces[0]])
                    numrows += 1
        elif row == 0:
            csv_out += (
                ",".join(
                    [
                        "user_id",
                        "username",
                        "first_name",
                        "last_name",
                        "display_name",
                    ]
                )
                + "\n"
            )
        if row == num_rows:
            break
        if row % int(num_rows * 0.01) == 0:
            print(round((row / num_rows) * 100), "% complete")
    f.close()
    print("Num of Rows:", numrows, " | Num elements in set", len(seen))

    outloc = os.path.dirname(__file__) + "/" + outname
    w = open(outloc, "w")
    w.write(csv_out)
    w.close()


comment_csv = [
    {
        "comments.data.0.id": 30,
        "payment.id": 71,
        "comments.data.0.date_created": 9,
        "comments.data.0.user.username": 31,
        "comments.data.0.user.id": 40,
        "comments.data.0.message": 10,
        "comments.data.0.mentions.count": 11,
        "app.name": 7,
        "app.id": 6,
    },
    {
        "comments.data.1.id": 67,
        "payment.id": 71,
        "comments.data.1.date_created": 65,
        "comments.data.1.user.username": 48,
        "comments.data.1.user.id": 62,
        "comments.data.1.message": 66,
        "comments.data.1.mentions.count": 68,
        "app.name": 7,
        "app.id": 6,
    },
]


def get_comments_csv(filename, outname, num_rows):
    print(
        "get_comments_csv function called, writing to:",
        outname,
        "| number of rows being read",
        num_rows,
    )
    fileloc = os.path.dirname(__file__) + "/" + filename
    f = open(fileloc, "r")
    csv_out = ""
    for (row, line) in enumerate(f):
        cells = line.split(",")
        csv_row = []
        if len(cells) == 404 and row > 0:
            if len(cells[30]) > 0:  # check if comment.data.0.id exists
                for index in comment_csv[0].values():
                    csv_row.append(cells[index])
                csv_out += ",".join(csv_row) + "\n"
                csv_row = []
            if len(cells[62]) > 0:  # check if comment.data.1.id exists
                for index in comment_csv[1].values():
                    csv_row.append(cells[index])
                csv_out += ",".join(csv_row) + "\n"
        elif row == 0:
            csv_out += (
                ",".join(
                    [
                        "comment_id",
                        "payment_id",
                        "date_created",
                        "author_username",
                        "author_user.id",
                        "message",
                        "mention_count",
                        "app_name",
                        "app_id",
                    ]
                )
                + "\n"
            )
        if row == num_rows:
            break
        if row % int(num_rows * 0.01) == 0:
            print(round((row / num_rows) * 100), "% complete")
    f.close()
    outloc = os.path.dirname(__file__) + "/" + outname
    w = open(outloc, "w")
    w.write(csv_out)
    w.close()


payment_csv = {
    "payment.id": 71,
    "payment.status": 70,
    "payment.date_created": 121,
    "payment.date_completed": 75,
    "payment.target.user.username": 80,
    "payment.target.user.id": 89,
    "payment.actor.username": 100,
    "payment.actor.id": 109,
    "payment.action": 120,
    "note": 123,
    "app.id": 6,
}


def get_payments_csv(filename, outname, num_rows):
    print(
        "get_payments_csv function called, writing to:",
        outname,
        "| number of rows being read",
        num_rows,
    )
    fileloc = os.path.dirname(__file__) + "/" + filename
    f = open(fileloc, "r")
    csv_out = ""
    for (row, line) in enumerate(f):
        cells = line.split(",")
        csv_row = []
        if len(cells) == 404 and row > 0:
            if len(cells[71]) > 0:  # check if payment.id exists
                for index in payment_csv.values():
                    csv_row.append(cells[index])
                csv_out += ",".join(csv_row) + "\n"
        elif row == 0:
            csv_out += (
                ",".join(
                    [
                        "payment_id",
                        "status",
                        "date_created",
                        "date_completed",
                        "target_username",
                        "target_user_id",
                        "target_type",
                        "actor_username",
                        "actor_id",
                        "actor_is_group",
                        "action",
                        "note",
                        "mentions_count",
                        "likes_count",
                        "app_id",
                        "app_name",
                    ]
                )
                + "\n"
            )
        if row == num_rows:
            break
        if row % int(num_rows * 0.01) == 0:
            print(round((row / num_rows) * 100), "% complete")
    f.close()
    outloc = os.path.dirname(__file__) + "/" + outname
    w = open(outloc, "w")
    w.write(csv_out)
    w.close()


def triage_infrequent_users(filename, outname, column_2_index, num_rows=-1):
    filename = os.path.dirname(__file__) + "/" + filename
    outname = os.path.dirname(__file__) + "/" + outname
    f = open(filename, "r")
    f.readline()
    user_neighbors = {}
    actor_column = payment_csv["payment.actor.id"]
    target_column = payment_csv["payment.target.user.id"]
    print("*" * 20, "Stage 1", "*" * 20)
    for rw_ind, line in enumerate(f):
        row = line.split(",")

        if len(row) == 404:  # avoid defective rows
            actor_id = row[actor_column]
            target_id = row[target_column]
            if actor_id != "" and target_id != "":
                user_neighbors[actor_id] = user_neighbors.get(actor_id, set([]))
                user_neighbors[actor_id].add(target_id)
                user_neighbors[target_id] = user_neighbors.get(target_id, set([]))
                user_neighbors[target_id].add(actor_id)
        if rw_ind == num_rows:
            break
        if rw_ind % int([num_rows, 7000000][num_rows == -1] * 0.01) == 0:
            print(
                round((rw_ind / [num_rows, 7000000][num_rows == -1]) * 100),
                "% complete",
            )
    f.close()
    valid_users = set(
        [user for user, neighbors in user_neighbors.items() if len(neighbors) >= 10]
    )
    del user_neighbors

    f = open(filename, "r")
    f.readline()
    w = open(outname, "w")
    w.write(
        ",".join(
            [
                "payment_id",
                "payment_status",
                "date_created",
                "date_completed",
                "target_username",
                "target_userid",
                "actor_username",
                "actor_id",
                "payment_action",
                "note",
                "app.id",
            ]
        )
        + "\n"
    )
    print("*" * 20, "Stage 2", "*" * 20)
    for rw_ind, line in enumerate(f):
        row = line.split(",")
        if len(row) == 404:  # avoid defective rows
            actor_id = row[actor_column]
            target_id = row[target_column]
            if (actor_id in valid_users) or (target_id in valid_users):
                newline = []
                for _, ind in column_2_index.items():
                    newline.append(row[ind])
                w.write(",".join(newline) + "\n")
        if rw_ind == num_rows:
            break
        if rw_ind % int([num_rows, 7000000][num_rows == -1] * 0.01) == 0:
            print(
                round((rw_ind / [num_rows, 7000000][num_rows == -1]) * 100),
                "% complete",
            )
    w.close()


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

# Notes
# total number of rows 7178768
# total number of rows with 404 cmns is 6961247
# all of the rows with 404 columns represent a payment transaction
# comments on public transaction are uncommon but about 910 of them exist
if __name__ == "__main__":
    # get_likes_csv("../Data/venmo.csv", "../Data/likes_500thousand.csv", 500000)
    # get_comments_csv("../Data/venmo.csv", "../Data/comments_500thousand.csv", 500000)
    # get_users_csv("../Data/venmo.csv", "../Data/users_500thousand.csv", 500000)
    # get_payments_csv("../Data/venmo.csv", "../Data/payments_500thousand.csv", 500000)
    # check_total_num_rows("../Data/venmo.csv")
    # check_total_num_valid_rows("venmo.csv")
    # check_total_num_payment_rows("venmo.csv")
    # check_total_num_category_rows("../Data/venmo.csv", category2)
    triage_infrequent_users(
        "../Data/venmo.csv", "../Data/venmo_freq_triaged.csv", payment_csv
    )
