from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
import os.path

new_cookie = {
    "sb": "o4PVXzaFYKjdn4W23NHVkCwB",
    "wd": "1680x914",
    "datr": "o4PVXwj91AD17FU4n0MdH1Tu",
    "locale": "en_US",
    "c_user": "100059250804885",
    "xs": "37%3ARuZRSjB5YznFkQ%3A2%3A1607835552%3A-1%3A-1",
    "fr": "14D7jRJqFWhdKELBW.AWVBNfkDqFqEl-WmMeEOc6tzAlE.Bf1YOj.yx.AAA.0.0.Bf1Z-c.AWVVwBKaeXA",
    "dpr": "2",
    "spin": "r.1003093988_b.trunk_t.1607835555_s.1_v.2_",
}
new_cookie2 = {
    "sb": "eQbYX7YaHw3oW7JRU4wm-mS2",
    "wd": "904x914",
    "datr": "eQbYX2B7r0DysxEXlafzFmgr",
    "dpr": "2",
    "c_user": "100059403954417",
    "xs": "12%3Al0qyiE-jF-aTBg%3A2%3A1607992974%3A-1%3A-1",
    "fr": "1g1hEqgHkGHvLX3nm.AWV_mwUyCs7AJMK0J3uZqIqPJpA.Bf2AZ5.6Q.AAA.0.0.Bf2AaO.AWU2GprJZoo",
    "spin": "r.1003097318_b.trunk_t.1607992978_s.1_v.2_",
}
user_2_name = {
    # "2223094500425728367": "Becka Geleto",
    # "1": "Lena Underwood",
    # "2": "Anogh Zaman",
    # "3": "Nadav Skloot",
}
driver = webdriver.Chrome(
    executable_path="/Users/beckaberhanu/Desktop/Academic/College/Semesters/Fifth Semester/Collective-Intelligence/Final Project/Data clean up/src/chromedriver"
)
newcookies = [
    {"name": key, "domain": "facebook.com", "value": val}
    for key, val in new_cookie2.items()
]
driver.get("https://www.facebook.com")
for i in newcookies:
    driver.add_cookie(i)
# print(driver.get_cookies())
num_candidates = 5
num_neighbors = 5


def update_driver_cookie():
    pass


def user_to_displayname(numrows=-1):
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


def check_name_match(name, tile_name):
    name_spl = name.lower().split(" ")
    tile_name_spl = tile_name.lower().split(" ")
    return (name_spl[0] == tile_name_spl[0]) and (name_spl[-1] in tile_name_spl)


def filter_tiles(tiles, name):
    filtered = []
    for ind, tile in enumerate(tiles):
        check1 = len(tile.contents) == 3
        check2 = len(tile.select('div[aria-label="Add friend"]')) > 0
        lives_in = tile.select(
            "div > span.d2edcug0.hpfvmrgz.qv66sw1b.c1et5uql.oi732d6d.ik7dh3pa.fgxwclzu.knj5qynh.m9osqain span"
        )
        check3 = len(lives_in) > 0
        check4 = False
        if check3:
            for i in lives_in:
                if "Lives in" in i.get_text():
                    check4 = True
                    break
        check5 = len(tile.select("h2 span > .nc684nl6 > a > span")) > 0
        check6 = False
        if check5:
            check6 = check_name_match(
                name, tile.select("h2 span > .nc684nl6 > a > span")[0].get_text()
            )
        # print(name)
        # print(tile.select("h2 span > .nc684nl6 > a > span"))
        if name == "Mitu Usha Turii":
            print("*" * 70)
            print(ind, "|", check1, check2, check3, check4, check5, check6)
        # print(tile)
        if check1 and check2 and check3 and check4 and check5 and check6:
            filtered.append(tile)
    return filtered


def get_tile_links(tiles):
    all_href = {}
    for tile in tiles:
        location = ""
        for i in tile.select(
            ".d2edcug0.hpfvmrgz.qv66sw1b.c1et5uql.oi732d6d.ik7dh3pa.fgxwclzu.knj5qynh.m9osqain span"
        ):
            if "Lives in" in i.get_text():
                location = i.get_text()[9:]
                break
        if len(tile.select(".nc684nl6 a:has(> span)")) == 1:
            link = tile.select(".nc684nl6 a:has(> span)")[0].get("href")
            link += "/friends" if ".php" not in link else "&sk=friends"
            all_href[link] = location
    return all_href


def find_user(user_name, neighbors):
    name = user_name.replace('"', "")
    name = user_name.replace("'", "")
    name_formated = name.replace(" ", "%20")
    driver.get(
        "https://www.facebook.com/search/people/?q=" + name_formated + "&spell=1"
    )
    time.sleep(2)
    for i in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)
    html = driver.page_source
    soup = BeautifulSoup(html, features="html.parser")
    p_user_tiles = soup.select(
        '.fjf4s8hc.tu1s4ah4.f7vcsfb0.k3eq2f2k.d2edcug0.rq0escxv div[role="article"] .tr9rh885.wkznzc2l.sjgh65i0.dhix69tm > div > .j83agx80'
    )  # potential user tile, div
    filtered_tiles = filter_tiles(p_user_tiles, name)
    p_user_links = get_tile_links(
        filtered_tiles[:num_candidates]
    )  # potential user links
    print(
        "🧑‍ Num Candidates located | Before filter:",
        len(p_user_tiles),
        "| Post filter:",
        len(filtered_tiles),
    )
    # print("Candidate Links:", p_user_links.items())
    # if len(p_user_tiles) == 0:
    #     if driver.current_url[36] == "https://www.facebook.com/checkpoint/":
    #         update_driver_cookie():
    for link, location in p_user_links.items():
        driver.get(link)
        time.sleep(3)
        inputElement = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//input[@placeholder="Search"][@dir="auto"][@type="text"]')
            )
        )
        match_count = 0
        for neighbor_name in neighbors[:num_neighbors]:
            neighbor_name = neighbor_name.replace('"', "")
            neighbor_name = neighbor_name.replace("'", "")
            inputElement.send_keys(neighbor_name)
            time.sleep(1)
            html = driver.page_source
            soup = BeautifulSoup(html, features="html.parser")
            friends = soup.select(
                '.j83agx80.btwxx1t3.lhclo0ds.i1fnvgqd .buofh1pr.hv4rvrfc a span[dir="auto"]'
            )
            if len(friends) > 0:
                match_count += check_name_match(neighbor_name, friends[0].get_text())
            for char in range(len(neighbor_name) + 2):
                inputElement.send_keys(Keys.BACK_SPACE)
            if match_count == 5:
                break
        if match_count > 0:
            return {
                "facebook_link": link,
                "location": location,
                "match_count": match_count,
            }
    return False


def get_facebook_prof(neighbors_file):
    f = open(os.path.dirname(__file__) + neighbors_file, "r")
    r = open(os.path.dirname(__file__) + "/../Data/Scrape/user_location.tsv", "r")
    last_id = ""
    for line in r:
        last_id = line.split("\t")[0]
    r.close()
    print(last_id)
    w1 = open(os.path.dirname(__file__) + "/../Data/Scrape/user_location.tsv", "a+")
    start_scrape = False
    for rw_ind, line in enumerate(f):
        node, neighbors = line.split("|")
        user_id, displayname = node.split(",")
        if user_id == last_id:
            start_scrape = True
            continue
        if not start_scrape:
            continue
        print("-" * 50, "\n" + displayname)
        neighbors = neighbors.replace("\n", "")
        neighbors = neighbors.split(",")
        # print("Neighbors: ",  neighbors)
        social = find_user(displayname, neighbors)
        if social:
            print(
                "✅ found ✅| location:",
                social["location"],
                "url",
                social["facebook_link"],
                "| match count:",
                str(social["match_count"]),
            )
            w1.write(
                "\t".join(
                    [
                        user_id,
                        social["location"],
                        social["facebook_link"],
                        str(social["match_count"]),
                    ]
                )
                + "\n"
            )
        else:
            print("❌ Not found")
        if (rw_ind > 0) and (rw_ind % 10 == 0):
            w1.close()
            print("*" * 20, rw_ind, "| saving progress |", "*" * 20)
            w1 = open(
                os.path.dirname(__file__) + "/../Data/Scrape/user_location.tsv", "a+"
            )
    # w1.close()


if __name__ == "__main__":
    # user_to_displayname()
    # get_facebook_prof("/../Data/Scrape/neighbors2.txt")

    # user_2_name = {
    #     "1": '"Colton Underwood"',
    #     "2": "Lena Underwood",
    #     "3": "Nadav Skloot",
    #     "4": "Kyaw Za Zaw",
    #     "5": "Anogh Zaman",
    # }
    get_facebook_prof("/../Data/Scrape/fakeusers.txt")
