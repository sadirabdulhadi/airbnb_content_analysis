city = "london"


path_to_airbnb_files = "/Users/Sadir/Documents/Computer_science/Year4/term2/individual_project/airbnb_files/"+city #manchester/bristol
path_to_wards_files = "/Users/Sadir/Documents/Computer_science/Year4/term2/individual_project/ward_files/"+city
dictionary_path= "/Users/Sadir/Documents/Computer_science/Year4/term2/individual_project/dictionaries/LIWC2007_English080730.dic"
path_ward_to_neigh =  "/Users/Sadir/Documents/Computer_science/Year4/term2/individual_project/ward_files/"+city+"/conv_ward_tolocal.csv"

path_listings = path_to_airbnb_files + "/listings.csv"
path_listings_to_neighbourhood = path_to_airbnb_files + "/listings_to_wards.csv"

import csv
import fiona
import shapely.geometry
import calculation_functions as cf
import setup
import shapefile
from shapely.geometry.polygon import Polygon
from shapely.geometry import shape



class Listing:
    def __init__(self, id=0, name = None, neighbourhood=None, longitude=0.0, latitude=0.0, number_reviews=0, counted = False, type = None):
        self.id = id
        self.name = name
        self.neighbourhood = neighbourhood
        self.longitude = longitude
        self.latitude = latitude
        self.number_reviews = number_reviews
        self.counted = counted
        self.type = type

class Ward:
    def __init__(self, id = 0, name=None, number_reviews = 0, number_listings = 0):
        self.id = id
        self.name = name
        self.number_reviews = number_reviews
        self.number_listings = number_listings

class Review:
    def __init__(self, listingID = 0, reviewID = 0, date = None, reviewerID = None, reviewerName = None, comments = None):
        self.listingID = listingID
        self.reviewID = reviewID
        self.date = date
        self.reviewerId = reviewerID
        self.reviewerName = reviewerName
        self.comment = comments
        self.scores = {}




# STEP 1: GET THE LISTINGS IN A LIST AS FOLLOWS - {ID, LISTINGS}
def getListings(path_listings):
    print("adding listings")
    listings = {}
    with open(path_listings) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            line_count += 1
            listings[row["id"]] = Listing(row["id"], row["name"], row["neighbourhood"], row["longitude"], row["latitude"], 0 , False, row["room_type"])
        print(f'{line_count} listings were counted')
        return listings

def getListingtoNeighbourhood(path_listings):
    neighbourhoods = {}
    listings = {}
    with open(path_listings_to_neighbourhood) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            neighbourhoods[row["listing"]] = row["neighbourhood"]
        return neighbourhoods


## STEP 2: ADJUST LOCATIONS
def confirmNeighbourhood(listings, neighbourhoods):
    unavailable = 0
    for id, listing in listings.items():
        if id in neighbourhoods.keys():
            listing.neighbourhood = neighbourhoods[id]
        else:
            unavailable +=1
    print("UNAVAILABLE LISTINGS = ", unavailable)


##STEP 3: GET REVIEWS:
def getReviews(listings):
    path1 = "/Users/Sadir/Documents/Computer_science/Year4/term2/individual_project/dictionaries/mydict/mydict.tsv"
    dictio = setup.Dictionary(path1)
    reviews = {}
    print("getting the reviews")
    file_reviews = path_to_airbnb_files + "/reviews.csv"
    with open(file_reviews) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        reviews_counted = 0
        reviews_total = 0
        for row in csv_reader:
            reviews_total += 1
            if (reviews_total%1000 == 0):
                print(reviews_total)
            if (row["listing_id"] in listings.keys()):
                reviews_counted += 1
                reviews[row["id"]] = Review(row["listing_id"],row["id"],row["date"],row["reviewer_id"],row["reviewer_name"],row["comments"])
                listings[row["listing_id"]].number_reviews += 1
                reviews[row["id"]].scores = cf.getScores(dictio, row["comments"])
                ## to remogve
            #if reviews_total == 10000:
                #break
        print(reviews_counted, "/", reviews_total, " reviews were counted")
        return reviews

def get_final_tables():
    print("We are here")
    listings = getListings(path_listings)
    print("listings no ",len(listings))
    neighbourhoods = getListingtoNeighbourhood(path_listings_to_neighbourhood)
    confirmNeighbourhood(listings, neighbourhoods)
    reviews = getReviews(listings)
    print("reviews", len(reviews))
    return ({"listings": listings, "reviews": reviews})
