import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.io as pio
pio.renderers.default='png'

df = pd.read_csv("movies.csv")

print(df.shape)
print(df.columns)

# Dealing with missing values

print(df.isnull().sum())

df.drop(columns=['id', 'imdb_id', 'homepage', 'cast', 'tagline', 'overview', 'budget_adj'], inplace=True)

df.dropna(how='any', subset=['genres', 'director'], inplace=True)

df['production_companies'] = df['production_companies'].fillna(0)
df['keywords'] = df['keywords'].fillna(0)

print(df.isnull().sum())


"""------------------ Data Analysis ----------------"""

df['popularity'] = df['popularity'].round(2)

# new columns insertion
df.insert(3, 'profit', df.revenue - df.budget)
df.insert(4, 'roi', df.profit/df.budget)
df['roi'] = df['roi'].round(2)


# visualizing data

df['roi'].value_counts()
df.isnull().sum()

non_finite_values = ~np.isfinite(df['roi'])
non_finite_values.sum()

df['roi'] = df['roi'].replace([np.inf, -np.inf], np.nan)

df1 = df[['popularity', 'budget', 'revenue', 'profit', 'roi', 'vote_count', 'vote_average', 'release_year']]

df1.hist(bins=20, figsize=(14,12))
plt.show()

df.popularity.value_counts()

df2 = df.groupby(['release_year'])['roi'].mean()
df2.plot(kind='line')

# Popularity
df3 = df.groupby('release_year')['popularity'].sum()
df3.plot(kind='line', color='red')
plt.xlabel('Year', fontsize=12)
plt.ylabel('Popularity')

# Rating 
df4 = df.groupby('release_year')['vote_average'].mean()
df4.plot(kind='line',)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Rating')

df5 = df.plot.scatter(x='popularity', y='vote_average', c='green', figsize=(6,4))
df5.set_xlabel('Popularity', color='DarkRed')
df5.set_ylabel('Vote_Average', color='DarkRed')
df5.set_title('Popularity vs Vote Average', fontsize=15)

df.genres.value_counts()

split = ['genres']
for i in split:
    df[i] = df[i].apply(lambda x: x.split("|"))
df.head(3)

df.genres.value_counts()

df = df.explode('genres')

df7 = df.groupby('genres')['popularity'].sum().sort_values(ascending=True)
df7

df7.plot.barh(x = 'genres', y='popularity', color='red', figsize=(12,6))

df.dtypes

df['release_date'] = pd.to_datetime(df['release_date'])

df['extracted_month'] = df['release_date'].dt.month

df8 = df.groupby('extracted_month')['popularity'].sum()
df8.plot(kind='bar')

data = {
        'extracted_month': df8.index,
        'popularity': df8.values
}
df8 = pd.DataFrame(data)

index_to_month = {
        1 : 'Jan',
        2: 'Feb',
        3: 'Mar',
        4: 'Apr',
        5: 'May',
        6: 'Jun',
        7: 'Jul',
        8: 'Aug',
        9: 'Sep',
        10: 'Oct',
        11: 'Nov',
        12: 'Dec'
    }

df8.extracted_month = df8.extracted_month.map(index_to_month)

df8.plot(kind='bar', x = 'extracted_month', y='popularity', color='DarkBlue')


df9 = df.groupby('extracted_month')['revenue'].sum()
df9

data = {
        'extracted_month': df9.index,
        'revenue': df9.values
        }
df9 = pd.DataFrame(data)

df9.extracted_month = df9.extracted_month.map(index_to_month)
df9.plot(kind='bar', x = 'extracted_month', y='revenue', color='DarkBlue')
plt.title('Revenue By Month')
plt.xlabel('Revenue')
plt.ylabel('Month')
plt.show()


df10 = df.groupby('original_title')['profit'].sum().sort_values(ascending=False).head(5)
df10

df10.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
plt.title('Top 5 Movies By Profit', color='red')


df11 = df.production_companies.value_counts()[1:].head(5)

explode_list = [0,0.04,0,0,0]
df11.plot(kind='pie', figsize= (12,6), autopct='%1.1f%%', startangle=90, labels=None, pctdistance=1.14, explode=explode_list)
plt.title('Top 5 Production companies By Movie Count', color='blue')
plt.legend(labels= df11.index, loc='upper right')
plt.axis('equal')
plt.show()


df12 = df.keywords.value_counts()[1:].head(15)
df12.index

data = {
        'keywords': df12.index,
        'value': df12.values
}
df12 = pd.DataFrame(data)

fig = px.treemap(df12, path=['keywords'], values='value')
fig.show()














