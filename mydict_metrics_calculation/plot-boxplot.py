__author__ = 'Sadir'

import csv
import statistics
import matplotlib as mpl
import matplotlib.pyplot as plt


lists = {}
indices = ["affect/tot", "pers/tot", "impers/tot", "pers/(pers+impers)"]

download_dir = "/Users/Sadir/Documents/Computer_science/Year4/term2/individual_project/results/bristol/table-reviews-info.csv"

def fillList():
    for index in indices:
        lists[index] = []
    with open(download_dir) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        for row in csv_reader:
            for index in indices:
                lists[index].append(float(row[index]))


def plot():
    mpl.use('agg')
    list_to_plot=[]
    for name, list in lists.items():
        maxi = max(list)
        mini = min(list)
        if (maxi == 0 or maxi == mini):
            new_list = list
        else:
            new_list = [(i-mini)/(maxi-mini) for i in list]
        print(name)
        list_to_plot.append(new_list)


    print(list_to_plot)

    data_to_plot = list_to_plot
    fig = plt.figure(1, figsize=(9, 6))

    # Create an axes instance
    ax = fig.add_subplot(111)


    # Create the boxplot
    bp = ax.boxplot(list_to_plot)
    ax.set_xticklabels(indices)


    # Save the figure
    fig.savefig('fig1.png', bbox_inches='tight')



fillList()

plot()

