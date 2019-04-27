path_to_airbnb_files = "/Users/Sadir/Documents/Computer_science/Year4/term2/individual_project/airbnb_files/london" #manchester/bristol
path_to_wards_files = "/Users/Sadir/Documents/Computer_science/Year4/term2/individual_project/ward_files/london"
dictionary_path= "/Users/Sadir/Documents/Computer_science/Year4/term2/individual_project/dictionaries/LIWC2007_English080730.dic"
path_ward_to_neigh =  "/Users/Sadir/Documents/Computer_science/Year4/term2/individual_project/ward_files/london/conv_ward_tolocal.csv"


import csv
import fiona
import shapely.geometry
import calculation_functions as cf
import shapefile
from shapely.geometry.polygon import Polygon
from shapely.geometry import shape
path_listings_to_neighbourhood = path_to_airbnb_files + "/listings_to_wards.csv"



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
                reviews[row["id"]].scores = cf.getScores(row["comments"])
                ## to remogve
            #if reviews_total == 10000:
                #break
        print(reviews_counted, "/", reviews_total, " reviews were counted")
        return reviews

def get_final_tables():
    print("We are here")
    #neighbourhoods = ward_to_neighbourhood()
    #print(neighbourhoods)
    path_listings = path_to_airbnb_files + "/listings.csv"
    listings = getListings(path_listings)
    neighbourhoods = getListingtoNeighbourhood(path_listings_to_neighbourhood)
    confirmNeighbourhood(listings, neighbourhoods)
    print("listings no ",len(listings))
    reviews = getReviews(listings)
    print("reviews", len(reviews))
    return ({"listings": listings, "reviews": reviews})

'''

def ward_to_neighbourhood():
    with open(path_ward_to_neigh) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        neighbourhoods = {}
        for row in csv_reader:
            if row["LAD16CD"] in ['E09000001', 'E09000002', 'E09000003', 'E09000004', 'E09000005', 'E09000006', 'E09000007', 'E09000008', 'E09000009', 'E09000010', 'E09000011', 'E09000012', 'E09000013', 'E09000014', 'E09000015', 'E09000016', 'E09000017', 'E09000018', 'E09000019', 'E09000020', 'E09000021', 'E09000022', 'E09000023', 'E09000024', 'E09000025', 'E09000026', 'E09000027', 'E09000028', 'E09000029', 'E09000030', 'E09000031', 'E09000032' ,'E09000033']:
                if row["LAD16NM"] not in neighbourhoods.keys():
                    neighbourhoods[row["LAD16NM"]] = []
                neighbourhoods[row["LAD16NM"]].append(row["WD16NM"])
    print(len(neighbourhoods.keys()))
    return neighbourhoods


    def confirmNeighbourhood(listings, neighbourhoods):
    wards = {}
    counter_names = 0
    counter_failed = 0
    counter_manual = 0
    ward_counter = 0
    listing_counter = 0
    print("finding neighbourhoods of listings")
    path_shapefile =path_to_wards_files +"/wards.shp"

    print("phase 1 - matching names")
    for feat in fiona.open(path_shapefile):
        listing_counter = 0
        ward_counter += 1
        print("ward: ", ward_counter)
        ward_properties = feat['properties']
        wards[ward_properties['ward_id']] = Ward(ward_properties['ward_id'], ward_properties['name'], 0, 0)
        shape = shapely.geometry.asShape(feat['geometry'] )
        #print(shape)

        for id, listing in listings.items():
            #this path only if neighbourhood = name_ward
            listing_counter += 1
            if (listing_counter%500 == 0):
                print(listing_counter)
            if listing.counted == True:
                continue
            #print(neighbourhoods)
            if ward_properties['name'] not in neighbourhoods[listing.neighbourhood]:
                continue
            point = shapely.geometry.Point(float(listing.longitude), float(listing.latitude)) # longitude, latitude
            #print("they have the same name! It's ", listing.neighbourhood)
            #print(float(listing.longitude), float(listing.latitude))
            #print (shape.bounds)
            if point.within(shape):
                listing.counted = True
                counter_names += 1
                wards[ward_properties['ward_id']].number_listings += 1
                wards[ward_properties['ward_id']].number_reviews += listing.number_reviews
                listing.neighbourhood = ward_properties['ward_id']
            else:
                print("failed")
            print(counter_names, " listings had neighbourhoods, ", counter_manual, " listings had coordinates, ", counter_failed, " are not counted.")

    print("phase 2 - getting locations")
    ward_counter = 0
    listing_counter = 0
    for feat in fiona.open(path_shapefile):
        listing_counter += 1
        if (listing_counter%500 == 0):
            print(listing_counter)
        ward_properties = feat['properties']
        shape = shapely.geometry.asShape(feat['geometry'] )
        ward_counter += 1
        print("ward: ", ward_counter)
        for id, listing in listings.items():
            if listing.counted == True:
                continue
            point = shapely.geometry.Point(float(listing.longitude), float(listing.latitude)) # longitude, latitude
            if shape.contains(point):
                listing.counted = True
                counter_manual += 1
                wards[ward_properties['ward_id']].number_listings += 1
                wards[ward_properties['ward_id']].number_reviews += listing.number_reviews
                listing.neighbourhood = ward_properties['ward_id']
            #print(counter_names+counter_manual)
            print(counter_names, " listings had neighbourhoods, ", counter_manual, " listings had coordinates, ", counter_failed, " are not counted.")


    print(counter_names, " listings had neighbourhoods, ", counter_manual, " listings had coordinates, ", counter_failed, " are not counted.")

    uncounted = 0
    totreviews = 0
    for id, listing in listings.items():
        if listing.counted == False:
            uncounted+=1
    print("uncounted is: ", uncounted)
    print("total number of reviews is:")

    for name, ward in wards.items():
        print(f'\tNAME: {ward.name}, LISTINGS {ward.number_listings}, REVIEWS {ward.number_reviews}')
        totreviews += ward.number_reviews

    print(totreviews)
        '''