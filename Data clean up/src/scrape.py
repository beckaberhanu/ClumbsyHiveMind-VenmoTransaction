from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
import os.path

cookies = {
    ## Add cookies for your facebook account below.
    ## You can find your cookies by looking at the first request sent to facebook
    ## in the 'network' tab of the developer tools in your browser. Do not share this publicly!
    ## The pound signs are just placeholders
    "sb": "########################",
    "wd": "###x###",
    "datr": "########################",
    "dpr": "#",
    "c_user": "###############",
    "xs": "##############################################",
    "fr": "############################################################################",
    "spin": "##########################################",
}

driver = webdriver.Chrome(executable_path=os.path.dirname(__file__) + "/chromedriver")
driver_cookies = [
    {"name": key, "domain": "facebook.com", "value": val}
    for key, val in cookies.items()
]
driver.get("https://www.facebook.com")
for i in driver_cookies:
    driver.add_cookie(i)
driver.get("https://www.facebook.com")
num_candidates = 5
num_neighbors = 5


def check_name_match(name, tile_name):
    """
    Function takes in two names and checks if the names are similar enough to be the same person.
    The first names should match exactly but the last name from the [name] variable only has to exist somewhere
    in the [tile_name] variable.
    """
    name_spl = name.lower().split(" ")
    tile_name_spl = tile_name.lower().split(" ")
    return (name_spl[0] == tile_name_spl[0]) and (name_spl[-1] in tile_name_spl)


def filter_tiles(tiles, name):
    """
    Looks through all candidate html elements from facebook search results and returns only the elements
    containing relevant (names must match) and sufficient (account should be public and contain location) information.
    """
    filtered = []
    for ind, tile in enumerate(tiles):
        # Check1: Element should contain three columns. Might be redundant with check2 but better safe then sorry.
        check1 = len(tile.contents) == 3
        # Check2: Account should have the option to add them as friend, otherwise it's probably private
        check2 = len(tile.select('div[aria-label="Add friend"]')) > 0
        lives_in = tile.select(
            "div > span.d2edcug0.hpfvmrgz.qv66sw1b.c1et5uql.oi732d6d.ik7dh3pa.fgxwclzu.knj5qynh.m9osqain span"
        )
        # Check3: Check if element containg location information might exist. Not a gaurantee. Might be redundant with check4.
        check3 = len(lives_in) > 0
        # Check4: Account should have the location information. Otherwise it's not worth our time.
        check4 = False
        if check3:
            for i in lives_in:
                if "Lives in" in i.get_text():
                    check4 = True
                    break
        # Check5: Check if html element containing account name exists. Redundancy for check6.
        check5 = len(tile.select("h2 span > .nc684nl6 > a > span")) > 0
        # Check6: Check name from html element matches the person we are looking for.
        check6 = False
        if check5:
            check6 = check_name_match(
                name, tile.select("h2 span > .nc684nl6 > a > span")[0].get_text()
            )
        # All checks have to pass an account to be worth verifying if that it is the account we are looking for.
        if check1 and check2 and check3 and check4 and check5 and check6:
            filtered.append(tile)
    return filtered


def get_tile_links(tiles):
    """
    Accepts a list of candidate html elements and obtains links to their corresponding facebook profiles.
    """
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


def find_user(display_name, neighbors):
    """
    Accepts the display name of a venmo user along with a list of the names of other people they have transacted with as
    input. The function then attempts to find a user on facebook with a matching display name and set of friends that
    overlap with the people they have transacted with on venmo. A single overlap in facebook friends and venmo transactions is
    sufficient.
    """
    name = display_name.replace('"', "")
    # URLs can't have empty spaces. %20 is an aliase for an empty space character in URLs
    name_formated = name.replace(" ", "%20")
    driver.get(
        "https://www.facebook.com/search/people/?q=" + name_formated + "&spell=1"
    )
    # wait 2 seconds for content to load. May depend on internet connection.
    time.sleep(2)
    for i in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)
    html = driver.page_source
    # Parse Html intp Beautiful soup object
    soup = BeautifulSoup(html, features="html.parser")
    # Get Html elements containing information for potential users of interest
    p_user_tiles = soup.select(
        '.fjf4s8hc.tu1s4ah4.f7vcsfb0.k3eq2f2k.d2edcug0.rq0escxv div[role="article"] .tr9rh885.wkznzc2l.sjgh65i0.dhix69tm > div > .j83agx80'
    )
    filtered_tiles = filter_tiles(p_user_tiles, name)
    # Links to facebook profiles for potential users of interest
    p_user_links = get_tile_links(filtered_tiles[:num_candidates])
    print(
        "🧑‍ Num Candidates located | Before filter:",
        len(p_user_tiles),
        "| Post filter:",
        len(filtered_tiles),
    )
    if len(p_user_tiles) == 0:
        if driver.current_url[36] == "https://www.facebook.com/checkpoint/":
            print(
                "Oh No! Facebook flagged you. NoOoOoOoOoOoOoO!!!!"
            )  # this should be pretty clear lol!
            exit()
    for link, location in p_user_links.items():
        driver.get(link)
        time.sleep(3)
        # locate and obtain an input element with which we could search for overlapping venmo neighbors
        inputElement = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//input[@placeholder="Search"][@dir="auto"][@type="text"]')
            )
        )
        # counts the number of overlaps between facebook friends and venmo neighbors
        match_count = 0
        for neighbor_name in neighbors[:num_neighbors]:
            neighbor_name = neighbor_name.replace('"', "")
            inputElement.send_keys(neighbor_name)
            # sleep for a second between each search for content to load.
            time.sleep(1.5)
            html = driver.page_source
            soup = BeautifulSoup(html, features="html.parser")
            # find if html elements exists that may contain search results for facebook friends
            friends = soup.select(
                '.j83agx80.btwxx1t3.lhclo0ds.i1fnvgqd .buofh1pr.hv4rvrfc a span[dir="auto"]'
            )
            if len(friends) > 0:
                match_count += check_name_match(neighbor_name, friends[0].get_text())
            for char in range(len(neighbor_name) + 2):
                inputElement.send_keys(Keys.BACK_SPACE)
            # if facebook account overlaps by 5 venmo neighbors, that is sufficient. No need to continue.
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
    """
    This function accepts the location of a file containing the a correspondence between each user and their
    venmo neighbors and tries to locate each venmo user on facebook based on their neighbors.
    """
    print("get_facebook_profile called")
    f = open(os.path.dirname(__file__) + neighbors_file, "r")
    r = open(os.path.dirname(__file__) + "/../Data/Scrape/user_location.tsv", "r")
    # The user ID of the last user to have been located by this program to avoid any redundant searchs
    last_id = ""
    for line in r:
        last_id = line.split("\t")[0]
    r.close()
    print("Last Id:", last_id)
    w = open(os.path.dirname(__file__) + "/../Data/Scrape/user_location.tsv", "a+")
    # only start scraping facebook once you are past the last user id to have already been located
    start_scrape = last_id == ""
    for rw_ind, line in enumerate(f):
        node, neighbors = line.split("|")
        user_id, displayname = node.split(",")
        if (user_id == last_id) and (last_id != ""):
            print("skiped to :", last_id)
            start_scrape = True
            continue
        if not start_scrape:
            continue
        print("-" * 50, "\n" + displayname)
        neighbors = neighbors.replace("\n", "")
        neighbors = neighbors.split(",")
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
            w.write(
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
            # save progress every 10 rows
            w.close()
            print("*" * 20, rw_ind, "| saving progress |", "*" * 20)
            w = open(
                os.path.dirname(__file__) + "/../Data/Scrape/user_location.tsv", "a+"
            )
    w.close()


if __name__ == "__main__":
    # user_to_displayname()
    get_facebook_prof("/../Data/Scrape/neighbors2.txt")
    # get_facebook_prof("/../Data/Scrape/fakeusers.txt")
