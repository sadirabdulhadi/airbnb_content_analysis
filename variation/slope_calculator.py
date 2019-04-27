from scipy.stats import linregress
import csv

file_root = "/Users/Sadir/Documents/Computer_science/Year4/term2/individual_project/results/london/dictionary-results"
dictionaries = ["liwc","mydict"]
metrics = {"liwc":["affect_tot", "impers_tot", "pers_pers+impers", "pers_tot"], "mydict":["loc", "prof", "soc", "prop", "soc_rel"]}
types = ["shared", "combined", "private"]


for dictionary in dictionaries:
    for type in types:
        for metric in metrics[dictionary]:
            results = {}
            to_read = file_root + "/" + dictionary + "/" + type + "/" + type + "median-more40_" + metric + ".csv"
            to_write = file_root + "/variations/" + dictionary + "/"+ type + "/"+ type + "variations" + metric + ".csv"
            with open(to_read) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    values = [float(row["2014"]), float(row["2015"]), float(row["2016"]), float(row["2017"]), float(row["2018"])]
                    values = list(filter(lambda a: a != -1, values))
                    print(values)
                    indices = []
                    for i in range(0, len(values)):
                        indices.append(i)
                    if len(values) <= 1:
                        results[row["Ward"]] = -1
                        continue

                    regress = linregress(indices, values)
                    slope = regress.slope
                    results[row["Ward"]] = slope

            with open(to_write, 'w', newline='') as csvfile:
                fieldnames = ['Ward', "metric_change"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for ward, value in results.items():
                    writer.writerow({'Ward': ward, 'metric_change': value})




'''
slope = result.slope
intercept = result.intercept

point1x = 0
point1y = intercept
point2x = 9
point2y = slope * point2x + intercept

import matplotlib.pyplot as plt
plt.plot(a,b, 'ro')
plt.plot([point1x,point2x], [point1y,point2y])

plt.ylabel('some numbers')
plt.show()
'''