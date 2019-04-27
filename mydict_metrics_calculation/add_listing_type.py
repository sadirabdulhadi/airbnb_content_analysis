__author__ = 'Sadir'

city = "london"

path_to_listings_small = "/Users/Sadir/Documents/Computer_science/Year4/term2/individual_project/airbnb_files/"+city+"/listings_to_wards.csv"
path_to_listings_large = "/Users/Sadir/Documents/Computer_science/Year4/term2/individual_project/airbnb_files/"+city+"/listings.csv"
path_to_write = "/Users/Sadir/Documents/Computer_science/Year4/term2/individual_project/airbnb_files/"+city+"/listings_type.csv"

import csv

listings = {}

cats = {"Private room":"shared", "Entire home/apt":"apartment", "Shared room":"shared"}


with open(path_to_listings_small) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                listings[row["listing"]] = {}
                listings[row["listing"]]["loc"] = row["neighbourhood"]


with open(path_to_listings_large) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                if row["id"] in listings.keys():
                    listings[row["id"]]["type"] = cats[row["room_type"]]

csv1 = csv.writer(open(path_to_write, "w"))
csv1.writerow(["listing", "neighbourhood", "type"])
for id, listing in listings.items():
    csv1.writerow([id, listing["loc"], listing["type"]])

print(listings)
