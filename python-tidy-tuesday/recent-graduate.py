# %%
# set up
import pandas as pd
from matplotlib import pyplot as plt
from janitor import clean_names
import numpy as np
import seaborn as sns
from pandas.tests.frame.test_sort_values_level_as_str import ascending

sns.set_style('white')
# %%
# EDA
# set up
recent_grad = pd.read_csv(
    "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2018/2018-10-16/recent-grads.csv")

recent_grad = clean_names(recent_grad)
recent_grad['major'] = recent_grad['major'].str.title()
recent_grad

# %%
by_major_category = ((recent_grad
    .assign(median_weighted=recent_grad['median'] * recent_grad['sample_size'])
    .groupby(['major_category']).agg({
    'total': 'sum',
    'women': 'sum',
    'men': 'sum',
    'median_weighted': 'sum',
    'sample_size': 'sum'}).assign(
    share_women=lambda x: x.women / x.total,
    median_salary=lambda x: x.median_weighted / x.sample_size))
                     .sort_values(by='share_women', ascending=False)).reset_index()

# %%
by_major_category\
    .sort_values(by='total', ascending=False)[['major_category', 'women', 'men']]\
    .plot.barh(x='major_category', stacked=True)

plt.show()

# plt.title("What are the most common major categories?")
# plt.xlabel("Total # of graduates")
# plt.ylabel("")
# plt.show()

# %%
# what major categories have the highest earnings ?

(recent_grad.assign(
    major_median=recent_grad
        .groupby('major_category')['median']
        .assign(median=lambda x: np.median(x.median)))
 .sort_values(by='major_median', ascending=False)
 .pipe((sns.catplot, 'data'),
       x='median',
       y='major_category',
       kind='box', stacked=True))
plt.show()

# %%
# What are the highest earning majors?
grad_processing = recent_grad.filter(
    ['major', 'major_category', 'major_code', 'median', 'p25th', 'p75th', 'sample_size'])

# %%
top20 = (grad_processing[grad_processing['sample_size'] >= 100]
         .sort_values(by='median', ascending=False)
         .query('sample_size >= 100')
         .head(20))

# %%
sns.catplot(data=top20, x='major_code', y='median', hue='major_category')
plt.title("What are highest-earning major?")
plt.ylabel("")
plt.show()
# %%
# How the gender breakdown related to typical earning
major_gender = (recent_grad
                .sort_values(by='total')
                .filter(['major', 'women', 'men'])
                .melt(id_vars=['major'], var_name='gender')
                .pivot(index=['major'], columns='gender')
                .head(20))
major_gender['value'].plot.bar(stacked=True)
plt.show()
