import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

main_path = "/Users/Sadir/Documents/Computer_science/Year4/term2/individual_project/results/london/socio-economic.csv"

#second_path = "/Users/Sadir/Documents/Computer_science/Year4/term2/individual_project/code/liwc_metrics_calculation/yamama.csv"
#https://www.statisticssolutions.com/wp-content/uploads/wp-post-to-pdf-enhanced-cache/1/correlation-pearson-kendall-spearman.pdf
data = pd.read_csv(main_path, index_col=0)
#data.drop(["foreign_born", "nonenglish_household", "household_size", "educated", "stem", "bohemian"], axis=1, inplace = True)
corr = data.corr('spearman')
fig = plt.figure()
ax = fig.add_subplot(111)
cax = ax.matshow(corr,cmap='coolwarm', vmin=-1, vmax=1)
fig.colorbar(cax)
ticks = np.arange(0,len(data.columns),1)
ax.set_xticks(ticks)
plt.xticks(rotation=90)
ax.set_yticks(ticks)
ax.set_xticklabels(data.columns)
ax.set_yticklabels(data.columns)
plt.show()