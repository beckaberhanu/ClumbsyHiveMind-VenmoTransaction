<img src="https://lh3.googleusercontent.com/fife/ABSRlIroeroikbKhshkShenf8fqTrRNN_vhDqRS-JVBZ-1MIw-YxvfH98aQRtnSDzrtoNH7g3cFgE88dcuKO-cTCHinloT2hqgIcIoSokimaE6UJxmeHJQKNo0LqAu3_MTr1CZ7zh-pGI6NU5qzHrK8-y6yGIp1eQ77k-eTdVWDOXLdWtRZJR-zrxZmTJUiG44gPk4Yr7zhmjrugWc0nU3tDt2uMwMzBOCKg4qJf0lGRPdqfNSFVXAoHYq3vPKoYpHrte1WGqET9YYCCPMA1P9YgxrT_v7ayi5ILZ1bC3OmtT8d4ZVmhZt2mobdJalI3m-W57wMsZZB3OrPbUpqSSbyuRRQAwRNkIbp66QC_DRVqtNy9IKdZRCRjgpZAtR4vX_-X0v8m6wy7UkeamDiCcsLGcGJgoXoHZijHYVKW_t5GMoTCRM5ZIPf00Eg1INwMYYgc0821yAufFMutGwy6FNrv7oLLhPSLbvaOkLld1xHzoyFF4NC0bhetP8n1tbaTzacbEUk7U8DnnWhQDz5FezTBHgPZeOfcy2Zt-n7xnxFf9Ws7MQ5lx71PS_uikEiLOz___jjOZSJx5gUUVyH05Bz_5VhDWGgrLsWgRT_sfNx2ls7Tt-vEu-vvJIDKrksZCfMfPzF9GtWYmeSNOfAEQBkNP8-v3Hm4ickCgvnwA6bVfefX9PXBvsETk3NV2m5uZM5bh1Hdnu5V7_sf_qM3GCM3T-xdtA=w3360-h1828-ft">

# Clumsy Hivemind - Collective intelligence final group Project

For this project, we wanted to do Open Source Intelligence (OSINT) research by exploring the spending habits of public Venmo transactions. Venmo is a mobile payment service that allows users to pay one another, while sharing a payment message, amount, time of payment and the user’s inputted name. A Venmo transaction can either surface as a payment or a charge between at least two users.

Although users are allowed to specify the visibility of their message within the app, the default setting in the app is to share all transactions publicly. This has raised security and privacy concerns, with large quantities of sensitive, user-specific data being shared to the public, leaving users vulnerable to Open Source Intelligence attacks. Past research, such as in "Security Research of a Social Payments App" by Kraft et al, raises the inherent vulnerabilities associated with being able to change your Venmo username at will, and the lack of differentiation between charges from friends and charges from strangers, in addition to the publicity of the message. This is dissimilar to what most users are familiar with, as for example, typically a payment transaction you make with a credit card, is not broadcasted publicly.

We want to, therefore, extract overarching insights from the spending patterns dataset. We also want to make an exploratory study into what information we can extract from people, such as the whereabouts of a person, or their roommates based on repeated payments with "rent" as a payment note. These insights are aimed to highlight the extent to which users could fall victim to these vulnerabilities

## Python Scipts

This repository contains three python scripts each dedicated to some category of tasks that we had to tackle for our project. All three python files are located in the `/src` directory of this repository. The broad categories of problems we tackled using these scripts is outlined in below.

### `traige.py`

- Contains functions that we used to explore our venmo dataset and filter out information that was either invalid or irrelevant to us. For example `triage_infrequent_users()` function removes all transactions that don't involve a user who has transacted with atleast 10 unique other users.

- It also contains functions that divide our larger dataset into smaller csv files dedicated to a particular aspect of data. For example the `get_users_csv()` function creates a csv file only containing user information and excludes transaction details.

### `network.py`

- Contains a group of functions we used to read through our transaction data and contruct csv files representing the nodes and edges we would later use in our gephi network visualizations. The script contains two different functions for constructing nodes and edges for either users or locations because the data used to create these network is structured differently for each.

- This script also contains a function called `scaleWeights()` that can alter the relative strengths of different categories of edges between two users or a user and particular location.

### `scrape.py`

- Contains a group of functions that we used to find the location of venmo users in our venmo dataset by finding their facebook profiles online. We can confirm that a venmo user corresponds to particular account on facebook by checking whether the set of other users that they frequently transact with on venmo or aslo their friends on facebook.
- This script heavily relies on the python `selenium` library to emulate a chrome browser logged into some facebook account. The chromedriver file we used to emulate this browser in selenium is also located in the `/src` directory.
