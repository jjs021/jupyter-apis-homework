#!/usr/bin/env python
# coding: utf-8

# # Homework 5, Part 2: Answer questions with pandas
# 
# **Use the Excel file to answer the following questions.** This is a little more typical of what your data exploration will look like with pandas.

# ## 0) Setup
# 
# Import pandas **with the correct name** .

# In[1]:


import pandas as pd


# ## 1) Reading in an Excel file
# 
# Use pandas to read in the `richpeople.xlsx` Excel file, saving it as a variable with the name we'll always use for a dataframe.
# 
# > **TIP:** You will use `read_excel` instead of `read_csv`, *but you'll also need to install a new library*. You might need to restart your kernel afterward!

# In[4]:


df = pd.read_excel('richpeople.xlsx')


# ## 2) Checking your data
# 
# Display the number of rows and columns in your data. Also display the names and data types of each column.

# In[5]:


df.shape[0]


# In[6]:


df.shape[1]


# In[7]:


df.head()


# ## 3) Who are the top 10 richest billionaires? Use the `networthusbillion` column.

# In[8]:


df.sort_values('networthusbillion', ascending= False).head(10)


# ## 4) How many male billionaires are there compared to the number of female billionares? What percent is that? Do they have a different average wealth?
# 
# > **TIP:** The last part uses `groupby`, but the count/percent part does not.
# > **TIP:** When I say "average," you can pick what kind of average you use.

# In[9]:


df.groupby("gender").count()


# In[10]:


count = df.groupby(by ="gender").name.count()
total = count.sum()

male = count['male']
female = count['female']

print ("male billionaires are", round((male/total)*100, 2),"% and female billionaires are",round((female/total)*100,2),"%.")


# In[11]:


df.groupby(by ="gender").mean('networthusbillion').networthusbillion


# ## 5) What is the most common source/type of wealth? Is it different between males and females?
# 
# > **TIP:** You know how to `groupby` and you know how to count how many times a value is in a column. Can you put them together???
# > **TIP:** Use percentages for this, it makes it a lot more readable.

# In[12]:


df.groupby(by ='sourceofwealth').count().sort_values(by='name', ascending= False).name.head()


# In[13]:


count_source_by_gender = df.groupby(by =["gender",'sourceofwealth']).size()
count_source_by_gender_df = count_source_by_gender.to_frame(name = 'count').reset_index()
count_source_by_gender_df[(count_source_by_gender_df.gender=='male')].nlargest(10, 'count')


# In[14]:


count_source_by_gender_df[(count_source_by_gender_df.gender=='female')].nlargest(10, 'count')


# In[15]:


df_by_source = df['sourceofwealth'].to_frame(name = "sourceofwealth")
df_by_source['malecount'] = [1 if g == 'male' else 0 for g in df['gender']]
df_by_source['femalecount'] = [1 if g == 'female' else 0 for g in df['gender']]
df_by_source['total'] = 1
df_by_source = df_by_source.groupby(by='sourceofwealth')[['malecount', 'femalecount', 'total']].sum().sort_values(by='total', ascending=False)
df_by_source['malepercent'] = [round(row['malecount']/row['total']*100,2) for i, row in df_by_source.iterrows()]
#df_by_source['femalepercent'] = [round(c/t*100,2) for c,t in df_by_source['femalecount', 'total']]
df_by_source['femalepercent'] = [round(row['femalecount']/row['total']*100,2) for i, row in df_by_source.iterrows()]
df_by_source[df_by_source.total > 1].sort_values(by='femalepercent', ascending=False).head(10)


# ## 6) What companies have the most billionaires? Graph the top 5 as a horizontal bar graph.
# 
# > **TIP:** First find the answer to the question, then just try to throw `.plot()` on the end
# >
# > **TIP:** You can use `.head()` on *anything*, not just your basic `df`
# >
# > **TIP:** You might feel like you should use `groupby`, but don't! There's an easier way to count.
# >
# > **TIP:** Make the largest bar be at the top of the graph
# >
# > **TIP:** If your chart seems... weird, think about where in the process you're sorting vs using `head`

# In[16]:


companies = df.groupby(by='company').size().to_frame(name='num').sort_values(by='num', ascending=False)
ax = companies[(companies.num > 1)].head().plot(kind='barh')
ax.invert_yaxis()


# ## 7) How much money do these billionaires have in total?

# In[17]:


companies_num = df['company'].value_counts()
companies_bil = df.groupby(by='company')['networthusbillion'].sum().to_frame(name = 'totalnetworthusbillion')
companies_bil['billionaires'] = companies_num
companies_bil.sort_values(by=['billionaires','totalnetworthusbillion'], ascending=False)


# ## 8) What are the top 10 countries with the most money held by billionaires?
# 
# I am **not** asking which country has the most billionaires - this is **total amount of money per country.**
# 
# > **TIP:** Think about it in steps - "I want them organized by country," "I want their net worth," "I want to add it all up," and "I want 10 of them." Just chain it all together.

# In[18]:


df.groupby(by='countrycode')['networthusbillion'].sum().to_frame(name='totalusbillion').nlargest(10, 'totalusbillion')


# ## 9) How old is an average billionaire? How old are self-made billionaires  vs. non self-made billionaires? 

# In[19]:


df['age'].mean()


# In[20]:


df.groupby(by='selfmade')['age'].mean().to_frame(name='avg age')


# ## 10) Who are the youngest billionaires? Who are the oldest? Make a graph of the distribution of ages.
# 
# > **TIP:** You use `.plot()` to graph values in a column independently, but `.hist()` to draw a [histogram](https://www.mathsisfun.com/data/histograms.html) of the distribution of their values

# In[25]:


#Youngest
df.sort_values('age', ascending= True).head(1)


# In[27]:


#Oldest
df.sort_values('age', ascending= False).head(1)


# In[38]:


#Distribution of age
df.groupby(by='age').count()['name'].plot(kind='bar')


# ## 11) Make a scatterplot of net worth compared to age

# In[39]:


df.plot.scatter(x='age', y='networthusbillion', c='Blue')


# ## 13) Make a bar graph of the wealth of the top 10 richest billionaires
# 
# > **TIP:** When you make your plot, you'll need to set the `x` and `y` or else your chart will look _crazy_
# >
# > **TIP:** x and y might be the opposite of what you expect them to be

# In[44]:


df.set_index('name', inplace=True, drop=False)
df.sort_values('networthusbillion', ascending= False).head(10).plot.bar(y ='networthusbillion')


# In[ ]:




