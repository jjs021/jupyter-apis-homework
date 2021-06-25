#!/usr/bin/env python
# coding: utf-8

# In[37]:


import pandas as pd


# In[38]:


df = pd.read_csv("Citywide_Payroll_Data__Fiscal_Year_.csv")


# In[5]:


df.shape


# In[6]:


df.keys()


# In[90]:


df = df[(df['Fiscal Year'] == 2020)]
df.head(10)
#Getting only the latest data


# In[91]:


df =df[(df['Leave Status as of June 30'] == 'ACTIVE')]


# In[92]:


df.shape


# In[93]:


df['Total_Pay'] = df['Regular Gross Paid']+df['Total OT Paid']+df['Total Other Pay']
df['Total_hour'] = df['Regular Hours']+df['OT Hours']


# In[94]:


df.head(3)


# In[95]:


df_sum_pay = df.groupby(by ='Agency Name')['Total_Pay'].sum()


# In[96]:


df_headcount= df.groupby(by ='Agency Name')['Last Name'].count()


# In[97]:


df_average_pay = df_sum_pay/df_headcount


# In[98]:


pd.set_option('display.max_rows', df_average_pay.shape[0]+1)
print(df_average_pay.sort_values(ascending = False))


# In[99]:


df.plot.scatter(x='Total_hour', y='Total_Pay', c='Blue', figsize=(20, 20))
#Some people logged more than 4000 hours of working hours. Don't they sleep?
#why some people work 0 hours and get paid?


# In[103]:


df[(df.Total_hour == 0)& (df.Total_Pay > 0)].sort_values('Total_Pay',ascending = False).head(20)
#There are people who recorded 0 hours but paid a lot. 


# In[ ]:





# In[ ]:




