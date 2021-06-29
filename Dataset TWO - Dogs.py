#!/usr/bin/env python
# coding: utf-8

# # Homework 6, Part Two: A dataset about dogs.
# 
# Data from [a FOIL request to New York City](https://www.muckrock.com/foi/new-york-city-17/pet-licensing-data-for-new-york-city-23826/)

# ## Do your importing and your setup

# In[1]:


import pandas as pd
import numpy as np


# ## Read in the file `NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx` and look at the first five rows

# In[2]:


df = pd.read_excel("NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx",index_col=0)
df.head(5)


# ## How many rows do you have in the data? What are the column types?
# 
# If there are more than 30,000 rows in your dataset, go back and only read in the first 30,000.

# In[3]:


df.shape


# ## Describe the dataset in words. What is each row? List two column titles along with what each of those columns means.
# 
# For example: “Each row is an animal in the zoo. `is_reptile` is whether the animal is a reptile or not”

# In[4]:


df.keys()


# In[5]:


#Each row is information of a dog with a license.
#Animal gender is whether a dog is a female or a male.
#Primary Breed is a primary breed of a dog.


# # Your thoughts
# 
# Think of four questions you could ask this dataset. **Don't ask them**, just write them down in the cell below. Feel free to use either Markdown or Python comments.

# In[6]:


#How many dogs have expired licenses.
#How many % of Samoyed
#How many primary breeds are there?


# # Looking at some dogs

# ## What are the most popular (primary) breeds of dogs? Graph the top 10.

# In[7]:


df['Primary Breed'].value_counts().head(10)


# ## "Unknown" is a terrible breed! Graph the top 10 breeds that are NOT Unknown

# In[8]:


df.drop(df[ df['Primary Breed'] == 'Unknown' ].index , inplace=True)
df['Primary Breed'].value_counts().head(10).plot(kind="bar")


# In[9]:


df = pd.read_excel("NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx",index_col=0)


# ## What are the most popular dog names?

# In[10]:


df['Animal Name'].value_counts().head(11)


# ## Do any dogs have your name? How many dogs are named "Max," and how many are named "Maxwell"?

# In[11]:


df[df['Animal Name']=='Max'].count()


# In[12]:


df[df['Animal Name']=='Maxwell'].count()


# ## What percentage of dogs are guard dogs?
# 
# Check out the documentation for [value counts](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.value_counts.html).

# In[13]:


df['Guard or Trained'].value_counts(normalize = True)


# ## What are the actual numbers?

# In[14]:


df['Guard or Trained'].value_counts()


# ## Wait... if you add that up, is it the same as your number of rows? Where are the other dogs???? How can we find them??????
# 
# Use your `.head()` to think about it, then you'll do some magic with `.value_counts()`

# In[15]:


df[pd.isnull(df['Guard or Trained'])]['License Issued Date'].count()


# ## Fill in all of those empty "Guard or Trained" columns with "No"
# 
# Then check your result with another `.value_counts()`

# In[16]:


df['Guard or Trained'] = df['Guard or Trained'].replace({np.nan:'No'})
df['Guard or Trained'].value_counts()


# ## What are the top dog breeds for guard dogs? 

# In[17]:


df[df['Guard or Trained'] =="Yes"]['Primary Breed'].value_counts()


# ## Create a new column called "year" that is the dog's year of birth
# 
# The `Animal Birth` column is a datetime, so you can get the year out of it with the code `df['Animal Birth'].apply(lambda birth: birth.year)`.

# In[18]:


df['year'] = df['Animal Birth'].apply(lambda birth: birth.year)


# ## Calculate a new column called “age” that shows approximately how old the dog is. How old are dogs on average?

# In[19]:


df['age'] = 2021 - df['year']
df['age'].mean().round(2)


# # Joining data together

# ## Which neighborhood does each dog live in?
# 
# You also have a (terrible) list of NYC neighborhoods in `zipcodes-neighborhoods.csv`. Join these two datasets together, so we know what neighborhood each dog lives in. **Be sure to not read it in as `df`, or else you'll overwrite your dogs dataframe.**

# In[20]:


zip_df = pd.read_csv("zipcodes-neighborhoods.csv",index_col=0)
zip_df.head()


# In[21]:


zip_df.reindex()
zip_df.head()


# In[22]:


zip_df['neighborhood'] = zip_df.index


# In[23]:


zip_df.reindex()
merged_df = df.merge(zip_df, how='left', left_on='Owner Zip Code', right_on='zip')
#merged_df.shape
merged_df.head()


# ## What is the most popular dog name in all parts of the Bronx? How about Brooklyn? The Upper East Side?

# In[24]:


merged_df[merged_df.borough == 'Bronx' ]['Animal Name'].value_counts().head(1)


# In[25]:


merged_df[merged_df.borough == 'Brooklyn' ]['Animal Name'].value_counts().head(10)


# In[26]:


merged_df[merged_df.neighborhood == 'Upper East Side' ]['Animal Name'].value_counts().head(10)


# ## What is the most common dog breed in each of the neighborhoods of NYC?

# In[27]:


merged_df.neighborhood.value_counts().shape


# In[28]:


merged_df.groupby(by='neighborhood')['Primary Breed'].value_counts().to_frame().groupby(by='neighborhood').head(2)


# ## What breed of dogs are the least likely to be spayed? Male or female?

# In[29]:


merged_df.groupby(by = (['Primary Breed','Animal Gender']))['Spayed or Neut']


# ## Make a new column called monochrome that is True for any animal that only has black, white or grey as one of its colors. How many animals are monochrome?

# In[39]:


merged_df['monocolor'] = False

#merged_df.head()


# In[47]:


merged_df['Animal Dominant Color']= merged_df['Animal Dominant Color'].str.upper()
merged_df['Animal Secondary Color']= merged_df['Animal Secondary Color'].str.upper()
merged_df['Animal Third Color']= merged_df['Animal Third Color'].str.upper()


filter1 = merged_df['Animal Dominant Color'].isin(['BLACK', 'WHITE', 'GREY'])
filter2 = merged_df['Animal Secondary Color'].isin(['BLACK', 'WHITE', 'GREY', np.nan])
filter3 = merged_df['Animal Third Color'].isin(['BLACK', 'WHITE', 'GREY', np.nan])

#merged_df.loc[merged_df[filter1 & filter2 & filter3], 'monocolor'] = True

merged_df.loc[filter1 & filter2 & filter3 , 'monocolor']= True


# In[49]:


merged_df.head()


# In[48]:


merged_df['monocolor'].value_counts()


# ## How many dogs are in each borough? Plot it in a graph.

# In[ ]:


dog_population_df = pd.DataFrame(merged_df.groupby(by = 'borough')['Animal Name'].count())
dog_population_df


# ## Which borough has the highest number of dogs per-capita?
# 
# You’ll need to merge in `population_boro.csv`

# In[ ]:


capita_df = pd.read_csv("boro_population.csv", index_col=0)


# In[ ]:


capita_df.head()


# In[ ]:


dog_man_pop_df=dog_population_df.merge(capita_df, left_on='borough', right_on='borough')


# In[ ]:


dog_man_pop_df


# In[ ]:


dog_man_pop_df['dog_per_capita'] = dog_man_pop_df['Animal Name']/dog_man_pop_df.population
dog_man_pop_df.sort_values(by='dog_per_capita', ascending=False)


# ## Make a bar graph of the top 5 breeds in each borough.
# 
# How do you groupby and then only take the top X number? You **really** should ask me, because it's kind of crazy.

# In[ ]:


merged_df.groupby(by='borough')['Primary Breed'].value_counts().to_frame().groupby(by='borough').head(5).plot(kind='bar', figsize=(20, 20),fontsize=25)


# ## What percentage of dogs are not guard dogs?

# In[ ]:


round(0.998971*100, 2)


# In[ ]:


#merged_df.groupby(by= 'monocolor')
c_df = merged_df[['Animal Dominant Color', 'Animal Secondary Color', 'Animal Third Color']].isin({
    'Animal Dominant Color': ['BLACK', 'WHITE', 'GREY', np.nan],
    'Animal Secondary Color': ['BLACK', 'WHITE', 'GREY', np.nan],
    'Animal Third Color': ['BLACK', 'WHITE', 'GREY', np.nan],
})
c_df
#c_df[(c_df['Animal Dominant Color'] & c_df['Animal Secondary Color'] & c_df['Animal Third Color'])]


# In[ ]:





# In[ ]:




