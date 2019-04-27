import csv
import numpy as np

city = "london"
path_to_airbnb_files = "/Users/Sadir/Documents/Computer_science/Year4/term2/individual_project/airbnb_files/"+city #manchester/bristol
file_reviews = path_to_airbnb_files + "/reviews.csv"

len_reviews={}
average_len_year = []
number_comments = []

years= ["2010","2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018"]


#get files in len_reviews
with open(file_reviews) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        reviews_counted = 0
        reviews_total = 0
        for row in csv_reader:
            reviews_total += 1
            if (reviews_total%1000 == 0):
                print(reviews_total)
            reviews_counted += 1
            if row['date'][:4] not in len_reviews.keys():
                len_reviews[row['date'][:4]] = []
            len_reviews[row['date'][:4]].append(len(row["reviewer_name"]))
        print(reviews_counted, "/", reviews_total, " reviews were counted")
        print(len_reviews)


for year in years:
    average_len_year.append(np.mean(len_reviews[year]))
    number_comments.append(len(len_reviews[year]))
print(average_len_year)
print(number_comments)
