<img src="https://lh3.googleusercontent.com/fife/ABSRlIroeroikbKhshkShenf8fqTrRNN_vhDqRS-JVBZ-1MIw-YxvfH98aQRtnSDzrtoNH7g3cFgE88dcuKO-cTCHinloT2hqgIcIoSokimaE6UJxmeHJQKNo0LqAu3_MTr1CZ7zh-pGI6NU5qzHrK8-y6yGIp1eQ77k-eTdVWDOXLdWtRZJR-zrxZmTJUiG44gPk4Yr7zhmjrugWc0nU3tDt2uMwMzBOCKg4qJf0lGRPdqfNSFVXAoHYq3vPKoYpHrte1WGqET9YYCCPMA1P9YgxrT_v7ayi5ILZ1bC3OmtT8d4ZVmhZt2mobdJalI3m-W57wMsZZB3OrPbUpqSSbyuRRQAwRNkIbp66QC_DRVqtNy9IKdZRCRjgpZAtR4vX_-X0v8m6wy7UkeamDiCcsLGcGJgoXoHZijHYVKW_t5GMoTCRM5ZIPf00Eg1INwMYYgc0821yAufFMutGwy6FNrv7oLLhPSLbvaOkLld1xHzoyFF4NC0bhetP8n1tbaTzacbEUk7U8DnnWhQDz5FezTBHgPZeOfcy2Zt-n7xnxFf9Ws7MQ5lx71PS_uikEiLOz___jjOZSJx5gUUVyH05Bz_5VhDWGgrLsWgRT_sfNx2ls7Tt-vEu-vvJIDKrksZCfMfPzF9GtWYmeSNOfAEQBkNP8-v3Hm4ickCgvnwA6bVfefX9PXBvsETk3NV2m5uZM5bh1Hdnu5V7_sf_qM3GCM3T-xdtA=w3360-h1828-ft" style="width:100%; max-height:300px; object-fit:cover; object-position: 50% 50%; border-radius: 10px; box-shadow: 0px 5px 5px rgba(0,0,0,0.3);">

# Clumsy Hivemind - Collective intelligence final group Project

This repository contains three python scripts each dedicated to a category of tasks we tackled for our project. All three python files are located in the `/src` directory of this repository. The broad categories of problems we tackled using these scripts is outlined in below.

## `traige.py`

- Contains functions that we used to explore our venmo dataset and filter out information that was either invalid or irrelevant to us. For example `triage_infrequent_users()` function removes all transactions that don't involve a user who has transacted with atleast 10 unique other users.

- It also contains functions that divide our larger dataset into smaller csv files dedicated to a particular aspect of data. For example the `get_users_csv()` function creates a csv file only containing user information and excludes transaction details.

## `network.py`

- Contains a group of functions we used to read through our transaction data and contruct csv files representing the nodes and edges we would later use in our gephi network visualizations. The script contains two different functions for constructing nodes and edges for either users or locations because the data used to create these network is structured differently for each.

- This script also contains a function called `scaleWeights()` that can alter the relative strengths of different categories of edges between two users or a user and particular location.

## `scrape.py`

- Contains a group of functions that we used to find the location of venmo users in our venmo dataset by finding their facebook profiles online. We can confirm that a venmo user corresponds to particular account on facebook by checking whether the set of other users that they frequently transact with on venmo or aslo their friends on facebook.
- This script heavily relies on the python `selenium` library to emulate a chrome browser logged into some facebook account. The chromedriver file we used to emulate this browser in selenium is also located in the `/src` directory.
