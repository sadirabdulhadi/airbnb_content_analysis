#here I'm using PySAL for the first time :) It is the Python spatial analysis library.

#references

##MORAN'S TEST
# the overall pipeline: http://darribas.org/gds_scipy16/ipynb_md/04_esda.html
# interpretation: http://pro.arcgis.com/en/pro-app/tool-reference/spatial-statistics/h-how-spatial-autocorrelation-moran-s-i-spatial-st.htm

import pysal as ps


import statsmodels.api as sm
from scipy import stats
import pandas as pd

import numpy
import matplotlib.pyplot as plt
import geopandas as gpd
import statsmodels.formula.api as smf
from statsmodels.stats.outliers_influence import variance_inflation_factor


table_census = "/Users/Sadir/Documents/Computer_science/Year4/term2/individual_project/results/bristol/socio-economic.csv"
table_reviews = "/Users/Sadir/Documents/Computer_science/Year4/term2/individual_project/results/bristol/dictionary-results/liwc/table2_pers_pers+impers.csv"
shapefile = '/Users/Sadir/Documents/Computer_science/Year4/term2/individual_project/ward_files/bristol/wards.shp'

years=["2014", "2015", "2016", "2017", "2018", "total"]
years_bis=["2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "total"] #DON'T USE, SIDE EFFECTS

def remove_empty_rows(dataframe, column):
    return dataframe[dataframe[column] != -1]

def clean_dataframe(census, reviews, year):
    sf = census.merge(reviews, on='Ward', how='inner')
    print(sf)
    sf.drop(sf.columns[[0]], axis=1, inplace=True) #we want 2017
    years_bis.remove(year)
    #print(years_bis)
    sf.drop(years_bis, axis=1, inplace = True)
    years_bis.append(year)
    #print(sf)

    #sf.drop(["number_bedrooms", "foreign_born", "educated", "students", "dep_children", "stem", "nonenglish_household"], axis=1, inplace = True)
    sf.drop(["nonenglish_household", "educated", "number_bedrooms", "students", "dep_children", "stem", "foreign_born", "deprivation_index", "bohemian"], axis=1, inplace = True)
    sf.rename(columns={year: 'index'}, inplace = True)
    sf = remove_empty_rows(sf, "index")
    #print(sf)

    return sf

def apply_log(sf):
    #when to apply log: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3591587/
    for column in list(sf.columns):
        values = sf[column].tolist()
        skewness = stats.skewtest(values).statistic
        if (skewness > 1.96) or (skewness < - 1.96):
            #print(skewness)
            sf[column] = sf[column].apply(numpy.log)
            #print("applied log to ", column)
            values = sf[column].tolist()
            skewness = stats.skewtest(values).statistic
            #print("now it is ", skewness)
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
    #print(est2.resid)
    return est2

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

def plot_quartiles(shape, reviews, year):
    wards_data = ps.pdio.read_files(shape)
    scores_data = pd.read_csv(reviews)
    shp_link = shape
    tx = gpd.read_file(shp_link)
    tx = tx.merge(scores_data, right_on='Ward', left_on="ward_id", how='inner')
    #hr10 = ps.Quantiles(tx[year], k=10)
    #f, ax = plt.subplots(1, figsize=(9, 9))
    #tx.assign(cl=hr10.yb).plot(column='cl', categorical=True, k=10, cmap='OrRd', linewidth=0.1, ax=ax, edgecolor='black', legend=True)
    #ax.set_axis_off()
    #plt.title("HR90 Deciles")
    # plt.show()

    df = ps.pdio.read_files(shapefile)
    df = df.set_index("ward_id")
    scores_data = scores_data.set_index("Ward")
    print(df)
    print(scores_data)
    df = df[scores_data[year] == -1]
    print(df)
    W = ps.weights.Rook.from_dataframe(df)
    W.transform = 'r'
    score = ps.Moran(tx['total'], W)
    print(score.I, score.p_sim)

#here we have the option between queen and rook. rook only considers common edges, queen does consider vertices
#!! We need to apply it to the residuals
#def get_moran(tx):
    #W = ps.rook_from_shapefile(shapefile)


def generate_yearly_dict(index):
    for year in years:
        if year == "total":
            census = pd.read_csv(table_census)
            reviews = pd.read_csv(table_reviews)
            print(year)
            sf = clean_dataframe(census, reviews, year)
            apply_log(sf)
            sf = transform_dataframe(sf)
            print(sf)
            model = lin_reg(sf, "index")
            print(model.summary())
            #getting rsquared
            print(model.rsquared)
            print(model.rsquared_adj)

            #getting pvalues
            print('p-values: ', model.pvalues["distance_to_work"])

            #getting coefficients
            print('Coefficient: ', model.params)

            #moran's test


        #vif_cal(sf, "index")


generate_yearly_dict("yo")
plot_quartiles(shapefile, table_reviews, "2015")

'''
census = pd.read_csv(table_census)
reviews = pd.read_csv(table_reviews)
sf = clean_dataframe(census, reviews)
apply_log(sf)
sf = transform_dataframe(sf)
print(sf)
lin_reg(sf, "index")
vif_cal(sf, "index")

'''
