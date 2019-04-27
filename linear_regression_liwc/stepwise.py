import statsmodels.formula.api as smf


#here I'm using PySAL for the first time :) It is the Python spatial analysis library.

#references

##MORAN'S TEST
# the overall pipeline: http://darribas.org/gds_scipy16/ipynb_md/04_esda.html
# interpretation: http://pro.arcgis.com/en/pro-app/tool-reference/spatial-statistics/h-how-spatial-autocorrelation-moran-s-i-spatial-st.htm

# check with matlab.
#
# moran's test -> no gaps give 0.
# check statsmodel -> zero constant.
# R -> stepwise linear regression // without enforcing the VIF.
#
# A city with more areas can also be looked at.
# Table of content
#


import pysal as ps


import statsmodels.api as sm
from scipy import stats
import pandas as pd

import numpy
import matplotlib.pyplot as plt
import geopandas as gpd
import statsmodels.formula.api as smf

import csv
from statsmodels.stats.outliers_influence import variance_inflation_factor


pref= "median-more40_"
city = "london"
property_type = "private"

table_census = "/Users/Sadir/Documents/Computer_science/Year4/term2/individual_project/results/"+city+"/socio-economic.csv"
table_reviews = "/Users/Sadir/Documents/Computer_science/Year4/term2/individual_project/results/"+city+"/dictionary-results/liwc/"+property_type+"/"+property_type
shapefile = "/Users/Sadir/Documents/Computer_science/Year4/term2/individual_project/ward_files/"+city+"/wards.shp"
download_dir = "/Users/Sadir/Documents/Computer_science/Year4/term2/individual_project/results/"+city+"/linear_regression/stepwise-liwc/"+property_type+"/"+property_type+"-sw-"

themes = ["pers_pers+impers.csv", "affect_tot.csv", "pers_tot.csv"]
#themes = ["table-avg_pers_pers+impers.csv", "table-avg_affect_tot.csv", "table-avg_pers_tot.csv"]

years=["2014", "2015", "2016", "2017", "2018", "total"]
years_bis=["2010","2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "total"] #DON'T USE, SIDE EFFECTS

keys_df = []


def forward_selected(data, response):
    """Linear model designed by forward selection.

    Parameters:
    -----------
    data : pandas DataFrame with all possible predictors and response

    response: string, name of response column in data

    Returns:
    --------
    model: an "optimal" fitted statsmodels linear model
           with an intercept
           selected by forward selection
           evaluated by adjusted R-squared
    """
    remaining = set(data.columns)
    remaining.remove(response)
    selected = []
    current_score, best_new_score = 0.0, 0.0
    while remaining and current_score == best_new_score:
        scores_with_candidates = []
        for candidate in remaining:
            formula = "{} ~ {} + 1".format(response,
                                           ' + '.join(selected + [candidate]))
            score = smf.ols(formula, data).fit().rsquared_adj
            scores_with_candidates.append((score, candidate))
        scores_with_candidates.sort()
        best_new_score, best_candidate = scores_with_candidates.pop()
        if current_score < best_new_score:
            remaining.remove(best_candidate)
            selected.append(best_candidate)
            current_score = best_new_score
    formula = "{} ~ {} + 1".format(response,
                                   ' + '.join(selected))
    model = smf.ols(formula, data).fit()
    return model

def remove_empty_rows(dataframe, column):
    return dataframe[dataframe[column] != -1]

def clean_dataframe(census, reviews, year):
    #merge census and reviews, index is "Ward"
    sf = census.merge(reviews, on='Ward', how='inner')
    sf.set_index("Ward", inplace = True)

    #drop all the years except for the one we are studying
    years_bis.remove(year)
    sf.drop(years_bis, axis=1, inplace = True)
    years_bis.append(year)
    #bristol" remove dep index
    #sf.drop(["nonenglish_household", "educated", "number_bedrooms", "students", "dep_children", "stem", "foreign_born", "bohemian"], axis=1, inplace = True) #VIF Bristol
    #manchester
    #sf.drop(["foreign_born", "educated", "median_age", "nonenglish_household", "students"], axis=1, inplace = True)
    #london
    #sf.drop(["household_size", "nonenglish_household", "educated"], axis=1, inplace = True)

    sf.rename(columns={year: 'index'}, inplace = True)
    sf = remove_empty_rows(sf, "index")
    global keys_df
    keys_df = list(sf.columns)
    keys_df.remove("index")
    print('KEYS')
    print(keys_df)

    sf.sort_index(inplace = True)

    return sf

def apply_log(sf):
    #when to apply log: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3591587/
    for column in list(sf.columns):
        values = sf[column].tolist()
        skewness = stats.skewtest(values).statistic
        sf["index"] = sf["index"].replace(0.000000, 0.000001)

        if (skewness > 1.96) or (skewness < - 1.96):
            sf[column] = sf[column].apply(numpy.log)
            print("applied log to ", column)
    return sf

def transform_dataframe(sf):
    cols = list(sf.columns)
    for col in cols:
        zscore = (sf[col] - sf[col].mean())/sf[col].std(ddof=0)
        sf[col] = zscore
    return sf


#the residuals we receive should be clean
def moran(shape, residuals):
    tx = gpd.read_file(shape)

    #only indices that exist in the residuals would be counted
    #print("residuals")
    #print(residuals)
    tx = tx.merge(residuals, right_on='Ward', left_on="ward_id", how='left')
    tx = tx.set_index("ward_id")
    tx["resid"].fillna(value=0, inplace=True)

    '''
    hr10 = ps.Quantiles(tx["resid"], k=10)
    f, ax = plt.subplots(1, figsize=(9, 9))
    tx.assign(cl=hr10.yb).plot(column='cl', categorical=True, k=10, cmap='OrRd', linewidth=0.1, ax=ax, edgecolor='black', legend=True)
    ax.set_axis_off()
    plt.title("HR90 Deciles")
    '''
    plt.show()
    indices_to_keep = tx.index.values

    df = ps.pdio.read_files(shapefile)
    df = df.set_index("ward_id")
    df = df.loc[indices_to_keep]

    W = ps.weights.Rook.from_dataframe(df)
    W.transform = 'r'
    score = ps.Moran(tx['resid'], W)
    return([score.I, score.p_sim])

#here we have the option between queen and rook. rook only considers common edges, queen does consider vertices
#!! We need to apply it to the residuals
#def get_moran(tx):
    #W = ps.rook_from_shapefile(shapefile)


def generate_yearly_dict(theme):
    rsquared = {}
    adjusted = {}
    pvalues = {}
    coeff = {}
    mor = {}

    #set-up:
    for year in years:
        pvalues[year] = {}
        coeff[year] = {}

    for year in years:
        #prep
        print(theme, year)
        census = pd.read_csv(table_census)
        reviews = pd.read_csv(table_reviews + pref + theme)
        sf = clean_dataframe(census, reviews, year)
        print("KEYSSSS")
        print(keys_df)

        apply_log(sf)
        sf = transform_dataframe(sf)
        model = forward_selected(sf, "index")
        print(theme, year)
        print(model.summary())
        residuals_dict = dict(model.resid)
        residuals_df = pd.DataFrame.from_dict(data = residuals_dict, orient = "index", columns = ["resid"])
        residuals_df.index.name = "Ward"

        rsquared[year] = model.rsquared
        adjusted[year] = model.rsquared_adj
        mor[year] = moran(shapefile, residuals_df)

        for key, value in dict(model.pvalues).items():
            pvalues[year][key] = value

        for key, value in dict(model.params).items():
            coeff[year][key] = value

        #getting rsquared
        '''
        print("R-squared", model.rsquared)
        print("Adjusted", model.rsquared_adj)

        #getting pvalues
        print('p-values: ', model.pvalues)

        #getting coefficients
        print('Coefficient: ', model.params)

        #moran's test
        print(moran(shapefile, residuals_df))
        '''
    return[rsquared, adjusted, mor, pvalues, coeff]

        #vif_cal(sf, "index")

def tocsv():
    for theme in themes:
        values = generate_yearly_dict(theme)

        rsquared = values[0]
        adjusted = values[1]
        mor = values[2]
        pvalues = values[3]
        coeff = values[4]

        row_rsquared = []
        row_adjusted = []
        row_mor = []
        row_morp = []
        row_pvalues = {}
        row_coef = {}

        csvw = csv.writer(open(download_dir + theme, "w"))
        csvw.writerow([theme])
        for key in keys_df:
            row_pvalues[key] = []
            row_coef[key] = []

        for year in years:
            row_mor.append(mor[year][0])
            row_morp.append(mor[year][1])
            row_rsquared.append(rsquared[year])
            row_adjusted.append(adjusted[year])
            for key in keys_df:
                if key in coeff[year].keys():
                    row_coef[key].append(coeff[year][key])
                    row_pvalues[key].append(pvalues[year][key])
                else:
                    row_coef[key].append(-1)
                    row_pvalues[key].append(-1)



        #the actual writing part
        print("we are here")
        print(row_adjusted)
        csvw.writerow(["", ""]+years)
        csvw.writerow(["R squared", ""] + row_rsquared)
        csvw.writerow(["Adjusted R squared", ""] + row_adjusted)
        print("KEYS")
        print(keys_df)
        for key in keys_df:
            print(key)
            csvw.writerow([key, "pval"] + row_pvalues[key])
            csvw.writerow([key, "coeff"] + row_coef[key])

        csvw.writerow(["Moran's test", ""] + row_mor)
        csvw.writerow(["Moran's p", ""] + row_morp)


def intersperse(lst, item):
    result = [item] * (len(lst) * 2 - 1)
    result[0::2] = lst
    return result




'''
census = pd.read_csv(table_census)
reviews = pd.read_csv(table_reviews)
sf = clean_dataframe(census, reviews, "2018")

apply_log(sf)
transform_dataframe(sf)
result = lin_reg(sf, "index")
#print(result.summary())
residuals_dict = dict(result.resid)
residuals_df = pd.DataFrame.from_dict(data = residuals_dict, orient = "index", columns = ["resid"])
residuals_df.index.name = "Ward"
#plot_quartiles(shapefile, residuals_df)

#vif_cal(sf, "index")
'''

tocsv()



