import csv
import statistics
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt



lists = {}
averages = {}
median = {}
std_dev = {}
skewness = {}
kurtosis = {}

final_list={}
#years = ["2011", "2011", "2011", "2011", "2011", "2012", "2012", "2012", "2012", "2012", "2013", "2013", "2013", "2013", "2013", "2014", "2014", "2014", "2014", "2014", "2015", "2015", "2015", "2015", "2015", "2016", "2016", "2016", "2016", "2016", "2017", "2017", "2017", "2017", "2017", "2018",  "2018",  "2018", "2018",  "2018", "total", "total", "total", "total", "total"]
years_simple = ["2010","2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "total"]

parameters = ["average", "median", "std-dev", "skewness", "kurtosis"]
indices = ["affect/tot", "pers/tot", "impers/tot", "pers/(pers+impers)"]
indices_bis = ["affect_tot", "pers_tot", "impers_tot", "pers_pers+impers"]


download_dir = "/Users/Sadir/Documents/Computer_science/Year4/term2/individual_project/results/london/table-reviews-info.csv" #manchester/bristol
results_dir = "/Users/Sadir/Documents/Computer_science/Year4/term2/individual_project/results/london/dictionary-results/liwc/private/delete"

type = ["Private room", "Shared room"]
#type = ["Entire home/apt"]

def fillList():
    print("fill-list")
    with open(download_dir) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        for row in csv_reader:
            if row["Type"] not in type:
                continue
            if row["Area"] not in lists:
                lists[row["Area"]] = {}
            if row["Year"] not in lists[row["Area"]].keys():
                lists[row["Area"]][row["Year"]] = []
            lists[row["Area"]][row["Year"]].append(float(row[indices[i]]))

    #the following chunk generates a table with : Ward -> number of reviews in ward



def cleanLists():
    print("clean-list")
    for ward, yearly_lists in lists.items():
        for yearly_lists, index_list in yearly_lists.items():
            while -1 in index_list:
                index_list.remove(-1)

def getAverages():
    count_peryear = {}

    for year in years_simple:
        count_peryear[year] = 0
    for ward, yearly_lists in lists.items():
        total_array = []
        for year, index_list in yearly_lists.items():
            count_peryear[year] += len(index_list)
            if ward not in averages:
                averages[ward] = {}
                median[ward] = {}
                std_dev[ward] = {}
                skewness[ward] = {}
                kurtosis[ward] = {}

            total_array += index_list

            #attt manchester specific
            if len(lists[ward][year]) < 40: # was == []
                averages[ward][year] = -1
                median[ward][year] = -1
                std_dev[ward][year] = -1
                skewness[ward][year] = -1
                kurtosis[ward][year] = -1
                continue

            averages[ward][year] = statistics.mean(lists[ward][year])
            median[ward][year] = statistics.median(lists[ward][year])

            if len(lists[ward][year])>1 :
                std_dev[ward][year] = statistics.stdev(lists[ward][year])
            else:
                std_dev[ward][year] = [-1]

            skewness[ward][year] = stats.skew(lists[ward][year])
            kurtosis[ward][year] = stats.kurtosis(lists[ward][year])



        if len(total_array) < 40:
                total_array = [-1]
                averages[ward]["total"] = -1
                median[ward]["total"] = -1
                std_dev[ward]["total"] = -1
                skewness[ward]["total"] = -1
                kurtosis[ward]["total"] = -1
                continue

        skewness[ward]["total"] = stats.skew(total_array)
        kurtosis[ward]["total"] = stats.kurtosis(total_array)
        averages[ward]["total"] = statistics.mean(total_array)
        median[ward]["total"] = statistics.median(total_array)
        if len(total_array)>1 :
            std_dev[ward]["total"] = statistics.stdev(total_array)
        else:
            std_dev[ward]["total"] = -1
        skewness[ward]["total"] = stats.skew(total_array)
        kurtosis[ward]["total"] = stats.kurtosis(total_array)
    print(count_peryear)



def generateCSV():
    print("generate csv")
    dir = results_dir + "median-more40_" + indices_bis[i] + ".csv" #where you want the file to be downloaded to
    csv1 = csv.writer(open(dir, "w"))

    column1TitleRow = ["Ward"] + years_simple
    csv1.writerow(column1TitleRow)

    #column2TitleRow = [""] + ["mean", "median", "std-dev", "skew", "kurtosis"]*9
    #column2TitleRow = [""] + ["median"]*9

    #csv1.writerow(column2TitleRow)

    for ward, yearly_lists in averages.items():
        row = [ward]
        for year in years_simple:
            if year in averages[ward].keys():
                #row += [str(averages[ward][year])]
                row += [str(median[ward][year])]
                #row += [str(std_dev[ward][year])]
                #row += [str(skewness[ward][year])]
                #row += [str(kurtosis[ward][year])]
            else:
                #row += ["-1", "-1", "-1", "-1", "-1"]
                row += ["-1"]
        csv1.writerow(row)

def print_distributions(year, statistic):
    statistic_year = []
    for ward, years in statistic.items():
        print(years)
        statistic_year.append(years[year])
    print(statistic_year)

    sns.distplot(statistic_year);
    plt.show()

for i in range(0,4):
    print("i is: ")
    lists = {}
    averages = {}
    fillList()
    cleanLists()
    getAverages()
    #print_distributions("2018", median)
    generateCSV()



