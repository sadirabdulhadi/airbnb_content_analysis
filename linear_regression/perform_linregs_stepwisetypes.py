#This file should perform all linregs and stepwise linregs for both dictionaries

import pysal as ps


import statsmodels.api as sm
from scipy import stats
import pandas as pd

import numpy
import matplotlib.pyplot as plt
import geopandas as gpd
from statsmodels.iolib.summary2 import summary_col
import statsmodels.formula.api as smf


city = "London"
table_census = "/Users/Sadir/Documents/Computer_science/Year4/term2/individual_project/results/"+city+"/socio-economic.csv"
shapefile = "/Users/Sadir/Documents/Computer_science/Year4/term2/individual_project/ward_files/"+city+"/wards.shp"


pref= "median-more40_"
file_root = "/Users/Sadir/Documents/Computer_science/Year4/term2/individual_project/results/london/dictionary-results"
saving_file = "/Users/Sadir/Documents/Computer_science/Year4/term2/individual_project/results/london/total-linreg/raw_val"
dictionaries = ["mydict","liwc"]
metrics = {"liwc":["affect_tot.csv", "impers_tot.csv", "pers_pers+impers.csv", "pers_tot.csv"], "mydict":["loc.csv", "prof.csv", "soc.csv", "prop.csv", "soc_rel.csv"]}
types = ["combined", "shared", "private"]
#types = ["shared", "private"]

years=["2014", "2015", "2016", "2017", "2018", "total"]
years_bis=["2010","2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "total"] #DON'T USE, SIDE EFFECTS

models_vif = {}
models_stepwise = {}

def remove_empty_rows(dataframe, column):
    return dataframe[dataframe[column] != -1]

def clean_dataframe(census, reviews, year, stepwise):
    #merge census and reviews, index is "Ward"
    sf = census.merge(reviews, on='Ward', how='inner')
    sf.set_index("Ward", inplace = True)

    #drop all the years except for the one we are studying
    years_bis.remove(year)
    sf.drop(years_bis, axis=1, inplace = True)
    years_bis.append(year)
    if stepwise == False:
        sf.drop(["nonenglish_household", "household_size", "educated", "deprivation"], axis=1, inplace = True)
    sf.rename(columns={year: 'index'}, inplace = True)
    global keys_df
    keys_df = list(sf.columns)
    keys_df.remove("index")
    print('KEYS')
    print(keys_df)
    sf = remove_empty_rows(sf, "index")
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

def lin_reg(input_data, dependent_col):
    X1 = input_data.loc[:, input_data.columns != dependent_col]
    y = input_data[[dependent_col]]

    X2 = sm.add_constant(X1)
    est2 = sm.OLS(y, X2.astype(float)).fit()
    return est2

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

def generate_yearly_dict(table_reviews, table_census):
    models = []
    mor = []
    morp = []

    for year in years:
        #prep
        census = pd.read_csv(table_census)
        reviews = pd.read_csv(table_reviews)
        sf = clean_dataframe(census, reviews, year, False)
        apply_log(sf)
        sf = transform_dataframe(sf)
        model = lin_reg(sf, "index")
        models.append(model)
        print(model.summary())
        residuals_dict = dict(model.resid)
        residuals_df = pd.DataFrame.from_dict(data = residuals_dict, orient = "index", columns = ["resid"])
        residuals_df.index.name = "Ward"
        mor_index = moran(shapefile, residuals_df)
        mor.append(round(mor_index[0], 2))
        morp.append(round(mor_index[1], 2))

    dfoutput = summary_col(models,stars=True,float_format='%0.2f',
              info_dict={'R2':lambda x: "{:.2f}".format(x.rsquared), 'Adj-R2': lambda x: "{:.2f}".format(x.rsquared_adj), 'F-stat': lambda x: "{:.2f}".format(x.f_pvalue)})
    print(dfoutput)
    html_format = dfoutput.as_html()
    summ = pd.read_html(html_format, header=0, index_col=0)[0]
    columns = list(summ)
    morans = pd.Series(dict(zip(columns, mor)))
    morans.name = "Moran's test"
    moransp = pd.Series(dict(zip(columns, morp)))
    moransp.name = "Moran's p"
    print(columns)
    summ = summ.append(morans)
    summ = summ.append(moransp)
    print(list(summ.index))
    summ = summ[summ.index.notnull()] #remove NaN rows

    cols = ['R2', 'Adj-R2', 'F-stat', 'median_age', 'bohemian', 'stem', 'foreign_born', 'diversity', 'number_bedrooms', 'dep_children', 'economic_activity', 'students', 'distance_to_center', 'distance_to_work', "Moran's test", "Moran's p"]
    summ = summ.reindex(index=cols)
    summ.fillna('-')

    print(summ)

    latex_format = format_table(summ.to_latex())

    return latex_format

    #return[rsquared, adjusted, mor, pvalues, coeff, fpval]

        #vif_cal(sf, "index")
def format_table(table):
    table = table.replace("index III", "Full homes")
    table = table.replace("index II", "Shared rooms")
    table = table.replace("index I", "All properties")
    table = table.replace("NaN", "")
    table = table.replace(r"\toprule", "")
    table = table.replace(r"\bottomrule", "")
    table = table.replace(r"\midrule", "")
    table = table.replace("\\\\", "\\\\     \hline")
    table = table.replace("\\begin{tabular}{llll}", "\\begin{table}[!hbt] \\begin{tabular}{llll}")
    table = table.replace("\\end{tabular}", "\\end{tabular} \\end{table}")











    return table

'''
    table = table.replace("\\\\", "\\\\     \\cline{2-5}")
    table = table.replace("Adj-R2", "\multicolumn{2}{l}{Adj-R2}")
    table = table.replace("R2                   &", "\multicolumn{2}{l}{R2}&")
    table = table.replace("F-stat", "\multicolumn{2}{l}{F-stat}")
    table = table.replace("Moran's test", "\multicolumn{2}{l}{Moran's test}")
    table = table.replace("Moran's p", "\multicolumn{2}{l}{Moran's p}")


    table = table.replace("All properties", "& All properties")
    table = table.replace("distance\_to\_work", "\multirow{2}{*}{Category 6} & distance\_to\_work ")
    table = table.replace("deprivation", "\multirow{3}{*}{Category 5} & deprivation")
    table = table.replace("number\_bedrooms", "\multirow{3}{*}{Category 4} & number\_bedrooms")
    table = table.replace("nonenglish\_household", "\multirow{3}{*}{Category 3} & nonenglish\_household")
    table = table.replace("bohemian", "\multirow{3}{*}{Category 2} & bohemian")
    table = table.replace("median\_age", "Category 1                  & median\_age")
    table = table.replace("stem", "&stem")
    table = table.replace("educated", "&educated")
    table = table.replace("foreign\_born", "&foreign\_born")
    table = table.replace("household\_size", "&household\_size")
    table = table.replace("students", "&students")
    table = table.replace("distance\_to\_center", "&distance\_to\_center")
    table = table.replace("diversity", "&diversity")
    table = table.replace("economic\_activity", "&economic\_activity")
    table = table.replace("dep\_children", "&dep\_children")
'''

def generate_latex(models, mor, morp):

    dfoutput = summary_col(models,stars=True,float_format='%0.2f',
              info_dict={'R2':lambda x: "{:.2f}".format(x.rsquared), 'Adj-R2': lambda x: "{:.2f}".format(x.rsquared_adj), 'F-stat': lambda x: "{:.2f}".format(x.f_pvalue)})
    html_format = dfoutput.as_html()
    summ = pd.read_html(html_format, header=0, index_col=0)[0]
    columns = list(summ)
    morans = pd.Series(dict(zip(columns, mor)))
    morans.name = "Moran's test"
    moransp = pd.Series(dict(zip(columns, morp)))
    moransp.name = "Moran's p"
    print(columns)
    summ = summ[summ.index.notnull()] #remove NaN rows
    summ = summ.append(morans)
    summ = summ.append(moransp)
    cols = ['R2', 'Adj-R2', 'F-stat', 'median_age', 'students', 'dep_children', 'number_bedrooms', 'household_size', 'educated', 'bohemian', 'stem', 'economic_activity', 'deprivation', 'nonenglish_household', 'foreign_born', 'diversity', 'distance_to_center', 'distance_to_work', "Moran's test", "Moran's p"]
    summ = summ.reindex(index=cols)
    summ.fillna('-')
    print(summ)

    latex_format = format_table(summ.to_latex())
    print(latex_format)
    return latex_format

def generate_dict_stepwise(table_reviews, table_census):

    for year in ["total"]:
        #prep
        census = pd.read_csv(table_census)
        reviews = pd.read_csv(table_reviews)
        sf = clean_dataframe(census, reviews, year, True)
        apply_log(sf)
        sf = transform_dataframe(sf)
        model = forward_selected(sf, "index")
        print(model.summary())
        residuals_dict = dict(model.resid)
        residuals_df = pd.DataFrame.from_dict(data = residuals_dict, orient = "index", columns = ["resid"])
        residuals_df.index.name = "Ward"
        mor_index = moran(shapefile, residuals_df)
        return model, round(mor_index[0], 2), round(mor_index[1], 2)




final_list = ""

models = ""

for dictionary in dictionaries:
    print("we are here!")
    for metric in metrics[dictionary]:
        print("METRIC")
        print(metric)
        model = []
        mor = []
        morp = []
        for prop_type in types:
            table_reviews = "/Users/Sadir/Documents/Computer_science/Year4/term2/individual_project/results/"+city+"/dictionary-results/"+dictionary+"/"+prop_type+"/"+prop_type + pref + metric
            final_saving_file = "/Users/Sadir/Documents/Computer_science/Year4/term2/individual_project/results/london/total-linreg/raw_val_2/"+ dictionary + "/" +metric
            result = generate_dict_stepwise(table_reviews, table_census)
            model.append(result[0])
            mor.append(result[1])
            morp.append(result[2])
        dfoutput = summary_col(model,stars=True,float_format='%0.2f',info_dict={'R2':lambda x: "{:.2f}".format(x.rsquared), 'Adj-R2': lambda x: "{:.2f}".format(x.rsquared_adj), 'F-stat': lambda x: "{:.2f}".format(x.f_pvalue)})
        html_format = dfoutput.as_html()
        summ = pd.read_html(html_format, header=0, index_col=0)[0]
        columns = list(summ)
        morans = pd.Series(dict(zip(columns, mor)))
        morans.name = "Moran's test"
        moransp = pd.Series(dict(zip(columns, morp)))
        moransp.name = "Moran's p"
        print(columns)
        summ = summ[summ.index.notnull()] #remove NaN rows
        summ = summ.append(morans)
        summ = summ.append(moransp)
        cols = ['R2', 'Adj-R2', 'F-stat', 'median_age', 'bohemian', 'stem', 'educated', 'nonenglish_household', 'foreign_born', 'diversity', 'number_bedrooms', 'household_size', 'dep_children', 'deprivation', 'economic_activity', 'students', 'distance_to_work', 'distance_to_center',  "Moran's test", "Moran's p"]
        summ = summ.reindex(index=cols)
        summ.fillna('-')
        print(summ)
        latex_format = format_table(summ.to_latex())
        models += latex_format
        models += "\\\\"
        models += "\captionof{table}{Stepwise: "+metric.replace("_", "-")+ "} \label{tab:"+metric.replace("_", "-")+"-roomtype}"
        print(metric)

        print(latex_format)
print(models)


