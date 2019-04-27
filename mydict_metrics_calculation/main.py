import calculate_scores_listings as csl
import csv
from langdetect import detect
import re

city = "london"
#this is the part where we calculate the things per review
download_dir = "/Users/Sadir/Documents/Computer_science/Year4/term2/individual_project/results/" + city + "/table-reviews-info-mydict.csv"
tables = csl.get_final_tables()
reviews = tables["reviews"]
listings = tables["listings"]


def generateCSV():
    numberOfTotalReviews = len(reviews)
    numberOfMissingReviews = 0
    numberOfNonMissingReviews = 0
    csv1 = csv.writer(open(download_dir, "w"))

    columnTitleRow = ["ReviewId", "Year", "Area", "Listingtype", "Review", "prof", "loc", "prop", "soc", "soc_rel"]
    csv1.writerow(columnTitleRow)
    print("flag 1")
    i = 0
    for reviewID, review in reviews.items():
        try:

            if (detect(review.comment) != "en"):
                numberOfMissingReviews += 1
                continue

        except:
            continue
        print(i)
        i += 1

        if review.listingID in listings:
            length = len(re.findall("[a-zA-Z_]+", review.comment))
            if (length == 0):
                numberOfMissingReviews += 1
                continue

            numberOfNonMissingReviews += 1
            reviewID = review.reviewID
            year = review.date[:4]
            location = listings[review.listingID].neighbourhood
            type = listings[review.listingID].type
            reviewItself = review.comment
            prof = review.scores['prof']
            loc = review.scores['loc']
            prop = review.scores['prop']
            soc = review.scores['soc']
            soc_rel = review.scores['soc_rel']

            row = [reviewID, year, location, type, reviewItself, prof, loc, prop, soc, soc_rel]
            csv1.writerow(row)
        else:
            numberOfMissingReviews +=1

    if (numberOfNonMissingReviews+numberOfMissingReviews == numberOfTotalReviews):
        print("yess")
        print(numberOfMissingReviews)


generateCSV()