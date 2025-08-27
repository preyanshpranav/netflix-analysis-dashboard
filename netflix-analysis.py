#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

# Load the dataset
df = pd.read_csv("netflix_titles.csv")

# Show basic structure
print("Shape:", df.shape)
df.head()


# In[2]:


df.isnull().sum()


# In[3]:


df = df[df['date_added'].notnull()]


# In[4]:


df['director'].fillna('Unknown', inplace=True)
df['cast'].fillna('Unknown', inplace=True)
df['country'].fillna('Unknown', inplace=True)


# In[5]:


df.isnull().sum()


# In[6]:


df['rating'].fillna('Not Rated', inplace=True)
df['duration'].fillna('Unknown', inplace=True)


# In[7]:


df.isnull().sum()


# In[10]:


import matplotlib.pyplot as plt

# Count how many Movies and TV Shows are there
type_counts = df['type'].value_counts()

# Create labels with exact numbers
labels = [f"{label} ({count})" for label, count in zip(type_counts.index, type_counts.values)]

# Create pie chart
plt.figure(figsize=(6, 6))
plt.pie(
    type_counts,
    labels=labels,
    colors=['pink', 'lightblue'],
    startangle=90
)

# Add title
plt.title("Number of Movies and TV Shows on Netflix")
plt.show()


# In[11]:


import pandas as pd
import matplotlib.pyplot as plt

# Drop missing countries
df_countries = df.dropna(subset=['country'])

# Split countries where there are multiple (e.g. "India, United States")
df_countries = df_countries.assign(country=df_countries['country'].str.split(', '))

# Explode so each row has one country
df_countries = df_countries.explode('country')

# Count how many times each country appears
country_counts = df_countries['country'].value_counts().head(10)

# Plot bar chart
plt.figure(figsize=(10, 6))
plt.barh(country_counts.index, country_counts.values, color='skyblue')
plt.xlabel("Number of Titles")
plt.title("Top 10 Countries with Most Netflix Titles")
plt.gca().invert_yaxis()  # Most titles at the top
plt.tight_layout()
plt.show()


# In[12]:


# Convert date_added to datetime
df['date_added'] = pd.to_datetime(df['date_added'])

# Extract year from date
df['year_added'] = df['date_added'].dt.year

# Drop NaN years (just 10 of them as you saw before)
df_years = df.dropna(subset=['year_added'])

# Count number of titles added each year
year_counts = df_years['year_added'].value_counts().sort_index()

# Plot it
plt.figure(figsize=(10, 6))
plt.plot(year_counts.index, year_counts.values, marker='o', linestyle='-', color='orange')
plt.title("Number of Titles Added to Netflix Each Year")
plt.xlabel("Year")
plt.ylabel("Number of Titles")
plt.grid(True)
plt.tight_layout()
plt.show()


# In[13]:


# Strip extra spaces
df['date_added'] = df['date_added'].str.strip()

# Convert to datetime safely
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')


# In[14]:


# Now extract year from the cleaned 'date_added'
df['year_added'] = df['date_added'].dt.year


# In[15]:


# Optional check
print(df['date_added'].isna().sum(), "rows could not be converted to datetime")


# In[16]:


# Convert 'date_added' to datetime
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')

# Extract year from 'date_added'
df['year_added'] = df['date_added'].dt.year


# In[17]:


import seaborn as sns
import matplotlib.pyplot as plt

# Set the visual style
sns.set(style='whitegrid')

# Create the bar plot
plt.figure(figsize=(12, 6))
sns.countplot(data=df, x='year_added', order=sorted(df['year_added'].dropna().unique()))
plt.title('Netflix Content Added Over the Years', fontsize=16)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Number of Titles Added', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# In[18]:


import seaborn as sns
import matplotlib.pyplot as plt

# Set the plot style
sns.set(style='whitegrid')

# Drop missing year values to avoid issues
df_filtered = df.dropna(subset=['year_added'])

# Create a grouped bar plot
plt.figure(figsize=(14, 7))
sns.countplot(data=df_filtered, x='year_added', hue='type', order=sorted(df_filtered['year_added'].unique()))
plt.title('Netflix Content Added Per Year by Type', fontsize=16)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Number of Titles Added', fontsize=12)
plt.legend(title='Type')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# In[19]:


# Make sure 'listed_in' and 'year_added' are not null
df_genres = df.dropna(subset=['listed_in', 'year_added']).copy()

# Split genres into separate rows
df_genres['genre'] = df_genres['listed_in'].str.split(', ')
df_genres = df_genres.explode('genre')


# In[20]:


# Group and count how many times each genre was added per year
genre_trend = df_genres.groupby(['year_added', 'genre']).size().reset_index(name='count')

# Get top 5 genres overall
top_5_genres = genre_trend.groupby('genre')['count'].sum().nlargest(5).index

# Filter only top genres
genre_trend_top5 = genre_trend[genre_trend['genre'].isin(top_5_genres)]

# Plot the trend
plt.figure(figsize=(14, 7))
sns.lineplot(data=genre_trend_top5, x='year_added', y='count', hue='genre', marker='o')
plt.title('Top 5 Genres Added to Netflix Over the Years', fontsize=16)
plt.xlabel('Year Added', fontsize=12)
plt.ylabel('Number of Titles', fontsize=12)
plt.legend(title='Genre')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# In[21]:


country_year_df=df.dropna(subset=['country', 'year_added'])
country_year_df=country_year_df.groupby(['country', 'year_added']).size().reset_index(name='count')
#Plot top 5 countries over time
top_countries = country_year_df.groupby('country')['count'].sum().sort_values(ascending=False).head(5).index
filtered_df = country_year_df[country_year_df['country'].isin(top_countries)]

import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))
sns.lineplot(data=filtered_df, x='year_added', y='count', hue='country', marker='o')
plt.title('Top 5 Countries by Netflix Content Added Over Years')
plt.xlabel('Year')
plt.ylabel('Number of Titles Added')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()


# In[22]:


import seaborn as sns
import matplotlib.pyplot as plt

# Split the multiple genres into a list
df['listed_in'] = df['listed_in'].astype(str)
genres_series = df['listed_in'].str.split(', ')
all_genres = genres_series.explode()

# Count frequency of each genre
genre_counts = all_genres.value_counts().head(15)  # top 15

# Plot
plt.figure(figsize=(12,6))
sns.barplot(y=genre_counts.index, x=genre_counts.values, palette="plasma")
plt.title("Top 15 Most Common Genres on Netflix", fontsize=14)
plt.xlabel("Number of Titles")
plt.ylabel("Genre")
plt.tight_layout()
plt.show()


# In[23]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Convert 'date_added' to datetime (if not done already)
df['date_added'] = pd.to_datetime(df['date_added'])

# Extract year and month
df['year_added'] = df['date_added'].dt.year
df['month_added'] = df['date_added'].dt.month_name()

# Group by Year and Month
content_heatmap = df.groupby(['year_added', 'month_added']).size().unstack().fillna(0)

# Reorder months
months_order = ['January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December']
content_heatmap = content_heatmap[months_order]

# Plot
plt.figure(figsize=(14,6))
sns.heatmap(content_heatmap, cmap='YlGnBu', linewidths=.5, annot=True, fmt='.0f')
plt.title('Netflix Content Additions by Year and Month', fontsize=16)
plt.xlabel('Month')
plt.ylabel('Year')
plt.tight_layout()
plt.show()



# In[24]:


# Drop nulls and split multiple directors
director_data = df.dropna(subset=['director'])
directors_series = director_data['director'].str.split(', ', expand=True).stack()
top_directors = directors_series.value_counts().head(10)

# Plot
plt.figure(figsize=(10,5))
sns.barplot(x=top_directors.values, y=top_directors.index, palette='Set2')
plt.title("Top 10 Directors by Number of Titles on Netflix")
plt.xlabel("Number of Titles")
plt.ylabel("Director")
plt.tight_layout()
plt.show()


# In[25]:


# Drop nulls and split multiple actors
actor_data = df.dropna(subset=['cast'])
actors_series = actor_data['cast'].str.split(', ', expand=True).stack()
top_actors = actors_series.value_counts().head(10)

# Plot
plt.figure(figsize=(10,5))
sns.barplot(x=top_actors.values, y=top_actors.index, palette='Paired')
plt.title("Top 10 Actors on Netflix")
plt.xlabel("Number of Appearances")
plt.ylabel("Actor")
plt.tight_layout()
plt.show()


# In[26]:


# Clean up nulls
genre_country_df = df.dropna(subset=['country', 'listed_in'])

# Take first country and genre for each title for simplicity
genre_country_df['main_country'] = genre_country_df['country'].apply(lambda x: x.split(',')[0])
genre_country_df['main_genre'] = genre_country_df['listed_in'].apply(lambda x: x.split(',')[0])

# Create pivot table
pivot = genre_country_df.pivot_table(index='main_genre', columns='main_country', aggfunc='size', fill_value=0)

# Show top 10 countries and top 10 genres only
top_countries = pivot.sum().sort_values(ascending=False).head(10).index
top_genres = pivot.loc[:, top_countries].sum(axis=1).sort_values(ascending=False).head(10).index
filtered_pivot = pivot.loc[top_genres, top_countries]

# Plot heatmap
plt.figure(figsize=(12, 6))
sns.heatmap(filtered_pivot, annot=True, fmt='d', cmap='coolwarm')
plt.title('Top Genres by Country on Netflix')
plt.xlabel('Country')
plt.ylabel('Genre')
plt.tight_layout()
plt.show()


# In[27]:


df['month_added'] = df['date_added'].dt.month_name()
df['year_added'] = df['date_added'].dt.year


# In[28]:


import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(12,6))
sns.countplot(x='month_added', data=df, 
              order=['January','February','March','April','May','June','July','August','September','October','November','December'], 
              palette='magma')

plt.title("Monthly Netflix Content Additions (Across All Years)", fontsize=14)
plt.xticks(rotation=45)
plt.xlabel("Month")
plt.ylabel("Number of Titles Added")
plt.tight_layout()
plt.show()


# In[29]:


plt.figure(figsize=(10,5))
sns.countplot(x='year_added', data=df, palette='coolwarm')
plt.title("Year-wise Netflix Content Additions", fontsize=14)
plt.xlabel("Year")
plt.ylabel("Number of Titles")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# In[30]:


df['month_year'] = df['date_added'].dt.to_period('M').astype(str)

monthly_trend = df.groupby('month_year').size().reset_index(name='count')

plt.figure(figsize=(14,6))
sns.lineplot(data=monthly_trend, x='month_year', y='count', marker='o')
plt.xticks(rotation=90)
plt.title("Netflix Monthly Content Addition Trend")
plt.xlabel("Month-Year")
plt.ylabel("Number of Titles")
plt.tight_layout()
plt.show()


# In[ ]:




