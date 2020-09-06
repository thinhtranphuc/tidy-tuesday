#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import nltk
plt.style.use("seaborn-whitegrid")
#%% data
medium_datasci = pd.read_csv(
    "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2018/2018-12-04/medium_datasci.csv") \
    .drop('x1', axis=1)  # remove verticle, column x1
#%%
medium_datasci.head()
# %% Who has the most posts?
medium_datasci['publication'].value_counts().head(10).sort_values().plot(kind="barh")

#%% ## What is the distribution of claps?
bins = np.arange(medium_datasci['claps'].min(), medium_datasci['claps'].max(), 100)
medium_datasci['claps'].plot(kind="hist", logx=True, bins=bins)

#%% What is the tag about?
medium_datasci.filter(like="tag").head()  # select columns contain tag

# %% Which tag is the most popular?
medium_datasci.filter(like="tag").sum().sort_values().plot(kind='barh')

#%% Tranformation
medium_melt = medium_datasci.melt(
    id_vars=medium_datasci.drop(medium_datasci.filter(like="tag").columns.to_list(), axis=1),
    var_name="tag"). \
    query("value == 1")

medium_melt.head()
medium_melt['tag'].value_counts()

#%% Which tag has the most claps?
medium_melt.groupby('tag')['claps'].median().sort_values().plot(kind="barh")

#%% How about the reading times?
# Ifelse
reading_time_simplified = np.where(medium_datasci['reading_time'] < 10, medium_datasci['reading_time'], 10)
# Create bins
bins = np.arange(reading_time_simplified.min(), reading_time_simplified.max(), .5)
# Plot
pd.Series(np.where(medium_datasci['reading_time'] < 10, medium_datasci['reading_time'], 10)).plot(kind="hist",
                                                                                                  bins=bins)
plt.title("Distribution of reading times")
plt.xlabel("Reading times")

#%% Text Mining
import spacy
import en_core_web_sm

nlp = en_core_web_sm.load()


#%%
# example of using SpaCy to tokenize a simple string

def tokenize(sent):
    doc = nlp.tokenizer(sent)
    return [token.text for token in doc]


words_tokenize = medium_datasci['title'].astype(str).apply(tokenize).apply(pd.Series)
unnest_words_tokenize = words_tokenize.stack().reset_index(level=0).rename(columns={"level_0": "post_id", 0: "word"})

#%%
stop_words = pd.DataFrame(nltk.corpus.stopwords.words('english')).rename(columns={0: "word"})
medium_words_pre = pd.merge(medium_datasci.reset_index().rename(columns={"index": "post_id"}), unnest_words_tokenize)
medium_words = pd.merge(medium_words_pre, stop_words, how='left', indicator=True)

#%%
medium_words = medium_words[medium_words['_merge'] == "left_only"].drop('_merge', axis=1)
medium_words = medium_words[
    (medium_words['word'].str.contains('[a-zA-Z]')) & (~medium_words['word'].isin(['nan', 'part', 'de']))]
medium_words['word'].value_counts().head(20).sort_values().plot(kind='barh')
plt.title("Common words in Medium post titles")
plt.xlabel("frequency")
