import pandas as pd
import numpy as np
import pysal as ps


import statsmodels.api as sm
from scipy import stats
import pandas as pd

import numpy
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from statsmodels.stats.outliers_influence import variance_inflation_factor


table_census = "/Users/Sadir/Documents/Computer_science/Year4/term2/individual_project/results/bristol/socio-economic.csv"
table_reviews = "/Users/Sadir/Documents/Computer_science/Year4/term2/individual_project/results/bristol/dictionary-results/liwc/table2_pers_pers+impers.csv"
year = "2018"
years=["2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "total"]
def clean_dataframe(census, reviews):
    sf = census.merge(reviews, on='Ward', how='inner')
    #sf.head()
    #sf.info()
    sf.drop(sf.columns[[0]], axis=1, inplace=True) #we want 2017
    years.remove(year)
    sf.drop(years, axis=1, inplace = True)
    #sf.drop(["number_bedrooms", "foreign_born", "educated", "students", "dep_children", "stem", "nonenglish_household"], axis=1, inplace = True)
    sf.drop(["nonenglish_household", "educated", "number_bedrooms", "students", "dep_children", "stem", "foreign_born", "deprivation_index", "bohemian"], axis=1, inplace = True)

    sf.rename(columns={year: 'index'}, inplace = True)
    return sf

def apply_log(sf):
    #when to apply log: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3591587/
    for column in list(sf.columns):
        values = sf[column].tolist()
        skewness = stats.skewtest(values).statistic
        if (skewness > 1.96) or (skewness < - 1.96):
            print(skewness)
            sf[column] = sf[column].apply(numpy.log)
            print("applied log to ", column)
            values = sf[column].tolist()
            skewness = stats.skewtest(values).statistic
            print("now it is ", skewness)
    return sf

def transform_dataframe(sf):
    cols = list(sf.columns)
    for col in cols:
        #col_zscore = col + '_zscore'
        col_zscore = col
        sf[col_zscore] = (sf[col] - sf[col].mean())/sf[col].std(ddof=0)
    return sf

def lin_reg(input_data, dependent_col):
    X1 = input_data.loc[:, input_data.columns != dependent_col]
    y = input_data[[dependent_col]]

    X2 = sm.add_constant(X1)
    est2 = sm.OLS(y, X2.astype(float)).fit()
    print(est2.resid)
    print(est2.summary())


def vif_cal(input_data, dependent_col):
    x_vars=input_data.drop([dependent_col], axis=1)
    xvar_names=x_vars.columns
    max = 0
    max_name = ""
    for i in range(0, xvar_names.shape[0]):
        y = x_vars[xvar_names[i]]
        x = x_vars[xvar_names.drop(xvar_names[i])]
        rsq = smf.ols(formula = "y~x", data = x_vars).fit().rsquared
        vif=round(1/(1-rsq),2)
        if vif > max:
            max_name = xvar_names[i]
            max = vif
        print (xvar_names[i], " VIF = " , vif)
    print("MAX = ", max_name)



census = pd.read_csv(table_census)
reviews = pd.read_csv(table_reviews)
sf = clean_dataframe(census, reviews)
apply_log(sf)
sf = transform_dataframe(sf)
print(sf)
lin_reg(sf, "index")
vif_cal(sf, "index")


