#%%
# set up
import pandas as pd
from matplotlib import pyplot as plt
from janitor import clean_names
import numpy as np
import seaborn as sns
plt.style.use('seaborn-whitegrid')
#%%
# EDA
# set up
tt_path = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2018/2018-10-16/recent-grads.csv"
recent_grad = pd.read_csv(tt_path)

recent_grad = clean_names(recent_grad)
recent_grad['major'] = recent_grad['major'].str.title()
recent_grad.head()
#%%
by_major_category = recent_grad \
    .assign(median_weighted = recent_grad['median'] * recent_grad['sample_size'])\
    .groupby('major_category')['total', 'women', 'men', 'median_weighted', 'sample_size'].sum()\
    .assign(share_women = lambda x: x['women']/x['total'],
            median_weight = lambda x: x['median_weighted']/x['total'])

p1 = by_major_category.sort_values(by='total')[['women', 'men']].plot(kind="barh", stacked=True)
p1.set_xticks(np.arange(0, 1000000, 500000))
plt.xlabel("")
plt.suptitle("What is the most popular major category", fontsize=10)
plt.title("Contribution by gender", fontsize=16)
plt.show()

#%%
# what major categories have the highest earnings ?
recent_grad_pivot = recent_grad[["major_category", "median"]]\
    .pivot(columns="major_category", values="median")

recent_grad_pivot.reindex(recent_grad_pivot.median().sort_values().index, axis=1)\
    .plot(kind="box", vert=False)
plt.suptitle("What major categories have the highest earnings?", fontsize=10)
plt.show()
#%%
recent_grad.plot(x="sample_size", y="median", kind="scatter", logx=True)
plt.suptitle("What is the sample size between median?", fontsize=10)
plt.show()


#%%
recent_grad_process = recent_grad\
    [recent_grad["sample_size"] >= 100]\
    .sort_values(by="median")\
    .head(20)\
    .plot(x="median", y="major", kind="scatter")

plt.show()