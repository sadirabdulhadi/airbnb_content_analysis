import csv
import numpy as np
import matplotlib.pyplot as plt


dictionaries_metrics = {"liwc":["affect/tot", "pers/tot", "pers/(pers+impers)", "impers/tot"], "mydict":["loc", "prof", "soc", "prop", "soc_rel"]}

dictionaries_files = {"liwc": "/Users/Sadir/Documents/Computer_science/Year4/term2/individual_project/results/london/table-reviews-info.csv", "mydict": "/Users/Sadir/Documents/Computer_science/Year4/term2/individual_project/results/london/table-reviews-info-mydict.csv"}

years = ["2014", "2015", "2016", "2017", "2018"]
years_plot = [2014, 2015, 2016, 2017, 2018]

types = {"private": ["Entire home/apt"], "shared": ["Private room", "Shared room"], "combined": ["Private room", "Shared room","Entire home/apt"]}
type_dict = {"liwc": "Type", "mydict": "Listingtype"}
typedict2 = {"combined": "Combined", "private": "Full Home", "shared": "Shared Room"}

def get_per_year_per_metric(dictionary, type):
    i = 0
    download_dir = dictionaries_files[dictionary]
    metricyeardict = {}
    metrics = dictionaries_metrics[dictionary]

    for metric in metrics:
        metricyeardict[metric] = {}

    with open(download_dir) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        for row in csv_reader:
            if row[type_dict[dictionary]] not in type:
                continue
            for metric in metrics:
                if row["Year"] not in metricyeardict[metric].keys():
                    metricyeardict[metric][row["Year"]] = []
                value = float(row[metric])
                if value >= 0:
                    metricyeardict[metric][row["Year"]].append(float(row[metric]))
            i += 1
        print(i)

    return metricyeardict

def get_plot(metric_year_dict, dictionary, type):
    i = 0
    metrics = metric_year_dict.keys()
    averages_metrics = {}
    for metric in metrics:
        averages_metrics[metric] = []
        for year in years:
            #print(metric_year_dict)
            clist = cleanList(metric_year_dict[metric][year])
            #print(clist)
            average = np.mean(clist)
            averages_metrics[metric].append(average)

    for metric in metrics:
        plt.figure()
        plt.plot(years_plot, averages_metrics[metric])
        plt.ylabel(metric)
        #plt.xlabel()
        plt.title(typedict2[type])
        plt.xticks(years_plot)

        name = type + "-" + dictionary + "-" + metric.replace("/","_").replace("(","").replace(")","") + ".png"
        plt.savefig("medians/"+name)
        print("I'm here")


def cleanList(listtoclean):
    while -1 in listtoclean:
        listtoclean.remove(-1)
        print("removing")
    return listtoclean

for dictionary in dictionaries_files.keys():
    for type in types.keys():
        print(type)
        metric_year_dict = get_per_year_per_metric(dictionary, types[type])
        get_plot(metric_year_dict, dictionary, type)
#print(metric_year_dict)
