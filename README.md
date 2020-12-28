<img src="https://lh3.google.com/u/0/d/1OscP1yLxSY3XjfN9WzsD1DDE-paQd_Xi=w3360-h1828-iv1" style="width:100%; max-height:400px; object-fit:cover; object-position: 50% 50%;">

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
