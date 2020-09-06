#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
plt.style.use("fivethirtyeight")


#%%
tt_path = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2019/2019-05-28/winemag-data-130k-v2.csv"
wine_ratings = pd.read_csv(tt_path)

wine_ratings.head()

#%%
wine_ratings["title"].str.extract("(20\d\d)").value_counts().plot(kind="bar")
wine_ratings["year"] = wine_ratings["title"].str.extract("(20\d\d)")
wine_ratings["year"] = wine_ratings["year"].fillna(0).astype(int)
#%%
wine_ratings["country"].value_counts().head()

wine_ratings["designation"].value_counts().head()

wine_ratings[wine_ratings["year"] != 0]["year"].plot(kind="hist", bins=50, rot=90)
plt.show()

wine_ratings["points"].plot(kind="hist")
plt.show()

wine_ratings["price"].plot(kind="kde",logx=True)
plt.show()


#%%
wine_ratings[["price", "points"]].plot(x="price", y="points", kind="scatter", logx=True)
wine_ratings[["price", "points"]].plot(x="price", y="points", kind="line", logx=True)
plt.show()

#%%
top7 = wine_ratings["country"].value_counts()[:7].index
wine_ratings.loc[~wine_ratings["country"].isin(top7), "country"] = "other"
wine_ratings_pivot = wine_ratings.pivot(
    columns="country",
    values="points"
)
wine_ratings_pivot.reindex(wine_ratings_pivot.median().sort_values().index, axis = 1).plot(kind="box", vert=False)
plt.show()