import calculate_scores_listings as csl
import csv
from langdetect import detect
import re

#this is the part where we calculate the things per review
download_dir = "/Users/Sadir/Documents/Computer_science/Year4/term2/individual_project/results/london/table-reviews-info-test-average.csv"
tables = csl.get_final_tables()
reviews = tables["reviews"]
listings = tables["listings"]


def generateCSV():
    numberOfTotalReviews = len(reviews)
    numberOfMissingReviews = 0
    numberOfNonMissingReviews = 0
    csv1 = csv.writer(open(download_dir, "w"))

    columnTitleRow = ["ReviewId", "Year", "Area", "Type", "Review", "affect/tot", "pers/tot", "impers/tot","pers/(pers+impers)"]
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

        if (i%1000 == 0):

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
            affect_tot = review.scores['affect/tot']
            pers_tot = review.scores['pers/tot']
            impers_tot = review.scores['impers/tot']
            pers_rel = review.scores['pers/(pers+impers)']
            row = [reviewID, year, location, type, reviewItself, affect_tot, pers_tot, impers_tot, pers_rel]
            csv1.writerow(row)
        else:
            numberOfMissingReviews +=1

    if (numberOfNonMissingReviews+numberOfMissingReviews == numberOfTotalReviews):
        print("yess")
        print(numberOfMissingReviews)


generateCSV()