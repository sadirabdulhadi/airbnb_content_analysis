__author__ = 'Sadir'
import pandas as pd
import numpy as np


import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

file_root = "/Users/Sadir/Documents/Computer_science/Year4/term2/individual_project/results/london/dictionary-results"
socio_econ = "/Users/Sadir/Documents/Computer_science/Year4/term2/individual_project/results/london/socio-economic.csv"
dictionaries = ["liwc","mydict"]
metrics = {"liwc":["affect_tot.csv", "impers_tot.csv", "pers_pers+impers.csv", "pers_tot.csv"], "mydict":["loc.csv", "prof.csv", "soc.csv", "prop.csv", "soc_rel.csv"]}
types = ['combined']
city = "London"
pref= "median-more40_"



def remove_neg(lista):
    while -1 in lista:
        lista.remove(-1)
        print(lista)
    return lista


def generate_table_dependent():
    metric_array = {}

    for dictionary in dictionaries:
        for prop_type in types:
            for metric in metrics[dictionary]:
                table_reviews = "/Users/Sadir/Documents/Computer_science/Year4/term2/individual_project/results/"+city+"/dictionary-results/"+dictionary+"/"+prop_type+"/"+prop_type + pref + metric
                data = pd.read_csv(table_reviews)
                metric_array[metric] = remove_neg(list(data['total'].values))

    print("Metric & Mean & Std & Min & 25\% & 50\% & 75\% & Max \\\\")
    for dictionary in dictionaries:
        for prop_type in types:
            for metric in metrics[dictionary]:
                sns.distplot(metric_array[metric])
                plt.plot()
                plt.show()
                print(metric[:-4], "&", round(np.mean(metric_array[metric]),3), "&", round(np.std(metric_array[metric]),3),  "&", round(min(metric_array[metric]),3), "&", round(np.percentile(metric_array[metric], 25),3), "&", round(np.percentile(metric_array[metric], 50),3), "&", round(np.percentile(metric_array[metric], 75),3), "&", round(max(metric_array[metric]),3),  "\\\\")

def generate_table_socioecon():
    metric_array = {}
    data = pd.read_csv(socio_econ)
    print(list(data))
    for metric in list(data)[1:]:
        metric_array[metric] = list(data[metric].values)
        print("Metric & Mean & Std & Min & 25\% & 50\% & 75\% & Max \\\\")

    for metric in list(data)[1:]:
        sns.distplot(metric_array[metric])
        plt.plot()
        plt.show()
        print(metric, "&", round(np.mean(metric_array[metric]),3), "&", round(np.std(metric_array[metric]),3),  "&", round(min(metric_array[metric]),3), "&", round(np.percentile(metric_array[metric], 25),3), "&", round(np.percentile(metric_array[metric], 50),3), "&", round(np.percentile(metric_array[metric], 75),3), "&", round(max(metric_array[metric]),3),  "\\\\")







generate_table_socioecon()

