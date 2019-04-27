import pandas as pd
import numpy as np
from sklearn import datasets, linear_model
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
from scipy import stats
import pandas as pd
from patsy import dmatrices
from patsy.builtins import *
import numpy
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from statsmodels.stats.outliers_influence import variance_inflation_factor




table_census = "/Users/Sadir/Documents/Computer_science/Year4/term2/individual_project/results/bristol/socio-economic.csv"
table_reviews = "/Users/Sadir/Documents/Computer_science/Year4/term2/individual_project/results/bristol/dictionary-results/liwc/table2_pers_pers+impers.csv"

census = pd.read_csv(table_census)
reviews = pd.read_csv(table_reviews)
sf = census.merge(reviews, on='Ward', how='inner')
#sf.head()
#sf.info()
sf.drop(sf.columns[[0,15,16,17,18,19,20,22,23]], axis=1, inplace=True) #we want 2017
#sf.drop(["foreign_born", "nonenglish_household", "household_size", "educated", "stem", "bohemian"], axis=1, inplace = True)

sf.rename(columns={'2017': 'index'}, inplace = True)


#calculating z-values
cols = list(sf.columns)


#calculate the z values for the input values
for col in cols:
    #col_zscore = col + '_zscore'
    col_zscore = col
    sf[col_zscore] = (sf[col] - sf[col].mean())/sf[col].std(ddof=0)


#print(sf.describe())


#print the correlation matrix just to see lol
#corr_matrix = sf.corr()
#corr_matrix["2017"].sort_values(ascending=False)
#print(corr_matrix["2017"])


X1 = sf.loc[:, sf.columns != 'index']
y = sf[["index"]]

X2 = sm.add_constant(X1)
print(X2)
est2 = sm.OLS(y, X2.astype(float)).fit()

print(est2.summary())


#eliminating VIF stuff
#https://stats.stackexchange.com/questions/155028/how-to-systematically-remove-collinear-variables-in-python

#gather features
new_list = sf.columns.drop("index")
print(new_list)
for dep in new_list:
    print("*****" + dep + "********")
    features = "+".join(sf.columns.drop(dep))
    y, X = dmatrices(dep+ '~' + features, sf , return_type='dataframe')
    vif = pd.DataFrame()
    vif["VIF Factor"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    vif["features"] = X.columns
    vif.round(1)
    print(vif)


# get y and X dataframes based on this regression:
y, X = dmatrices('index ~' + features, sf , return_type='dataframe')



