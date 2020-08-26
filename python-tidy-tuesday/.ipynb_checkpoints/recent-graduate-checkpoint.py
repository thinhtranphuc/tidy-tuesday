# %%
# set up
import pandas as pd
from matplotlib import pyplot as plt
from janitor import clean_names
import seaborn as sns
plt.style.use('seaborn-whitegrid')
# %%
# EDA
# set up
recent_grad = pd.read_csv(
    "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2018/2018-10-16/recent-grads.csv")

recent_grad = clean_names(recent_grad)

# %%
# what major categories have the highest earnings ?
# %%

(recent_grad.assign(
    major_median = recent_grad
    .groupby('major_category')['median']
    .transform('median'))
    .sort_values(by='major_median', ascending=False)
    .pipe((sns.catplot, 'data'),
         x='median',
         y='major_category',
         kind='box'))
plt.show()

#%%
sns.catplot(x='median', y='major_category',
                data=recent_grad, kind='box', order=category_order)
plt.show()
# %%
# What are the highest earning majors?
grad_processing = recent_grad.filter(['major', 'major_category', 'median', 'p25th', 'p75th', 'sample_size'])

# %%
top20 = (grad_processing[grad_processing['sample_size'] >= 100]
         .sort_values(by='median', ascending=False)
         .query('sample_size >= 100')
         .head(20))


top20_melt = top20.melt(
    id_vars=['major', 'major_category', 'sample_size'])
#%%
grad_processing = recent_grad.sort_values(
    by='median', ascending=False)[['major', 'major_code', 'major_category', 'sample_size', 'p25th', 'median','p75th']]

sns.set(font_scale=0.5)
plt.figure(figsize=(30,8))
g = (grad_processing[grad_processing['sample_size'] >= 100]
 .head(20)
 .melt(id_vars=['major', 'major_code', 'major_category', 'sample_size'])
 .pipe((sns.catplot, 'data'),
       x='value',
       y='major',
       hue='major_category',
       kind='point',
       join=False))
plt.legend("")
plt.ylabel("")
plt.show()
