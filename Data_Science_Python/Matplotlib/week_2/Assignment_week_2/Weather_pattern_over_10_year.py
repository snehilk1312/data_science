import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd
import matplotlib.dates as mdates
import numpy as np

data = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')
data['Date_Mod']=pd.Series(map(pd.to_datetime, data['Date']))
data = data[data.Date.str.contains('20..-02-29')==False]
data['Year'] = data['Date_Mod'].map(lambda x: x.year)
data_=data[data['Year']==2015]
data = data[data['Year']!=2015]
data_.groupby('Year')
data.groupby('Year')
data=data.set_index('Year')
data_=data_.set_index('Year')
data['day_month']=data['Date_Mod'].map(lambda x: str(x.month*100+x.day).zfill(4))
data_['day_month']=data_['Date_Mod'].map(lambda x: str(x.month*100+x.day).zfill(4))
max_df = data[data['Element']=='TMAX']
min_df = data[data['Element']=='TMIN']
max_max_df=pd.DataFrame(max_df.groupby(['day_month'])['Data_Value'].max())
min_min_df=pd.DataFrame(min_df.groupby(['day_month'])['Data_Value'].min())
max_min_df = pd.merge(max_max_df,min_min_df,how='inner',left_index=True,right_index=True)
max_min_df['day_mont']=max_min_df.index
max_min_df.reset_index(drop=True, inplace=True)
max_min_df['day_mont']=max_min_df['day_mont'].astype(str)
max_min_df['in_year']=pd.Series(map(lambda p: pd.to_datetime(p, format='%m%d'),max_min_df['day_mont']))

max_min_df['str_date']=max_min_df['in_year'].dt.strftime('%m%d')

max_min_df['str_date']=max_min_df['str_date'].astype(int)

d = max_min_df['in_year'].values



observation_dates = np.arange('1900-01-01', '1901-01-01', dtype='datetime64[D]')


data['Year'] = data['Date_Mod'].map(lambda x: x.year)




data_['Year'] = data_['Date_Mod'].map(lambda x: x.year)




data_2015=data_.copy()

data_2015_max=data_2015[data_2015['Element']=='TMAX']
data_2015_min=data_2015[data_2015['Element']=='TMIN']



max_2015_df=pd.DataFrame(data_2015_max.groupby(['day_month'])['Data_Value'].max())
min_2015_df=pd.DataFrame(data_2015_min.groupby(['day_month'])['Data_Value'].min())



max_2015_df['day_month']=max_2015_df.index
max_2015_df.reset_index(drop=True,inplace=True)
min_2015_df['day_month']=min_2015_df.index
min_2015_df.reset_index(drop=True,inplace=True)


max_2015_df.columns=['temp_max','day_month']
min_2015_df.columns=['temp_min','day_month']



max_df_alt = data[data['Element']=='TMAX']
min_df_alt = data[data['Element']=='TMIN']


max_max_df_alt=pd.DataFrame(max_df_alt.groupby(['day_month'])['Data_Value'].max())



min_min_df_alt=pd.DataFrame(min_df_alt.groupby(['day_month'])['Data_Value'].min())


max_min_df_alt = pd.merge(max_max_df_alt,min_min_df_alt,how='inner',left_index=True,right_index=True)


max_min_df_alt['day_mont']=max_min_df_alt.index



max_min_df_alt.reset_index(drop=True, inplace=True)




max_min_df_alt['day_mont']=max_min_df_alt['day_mont'].astype(str)




max_min_df_alt['in_year']=pd.Series(map(lambda p: pd.to_datetime(p, format='%m%d'),max_min_df_alt['day_mont']))


max_min_df_alt['str_date']=max_min_df_alt['in_year'].dt.strftime('%m%d')



max_min_df_alt['str_date']=max_min_df_alt['str_date'].astype(int)


# In[128]:

max_min_df_alt=max_min_df_alt[['Data_Value_x','Data_Value_y','day_mont','in_year']]



comp_df=pd.merge(max_min_df_alt, max_2015_df, how='inner',left_on='day_mont',right_on='day_month')

comp_df=pd.merge(comp_df, min_2015_df, how='inner',left_on='day_mont',right_on='day_month')



comp_df=comp_df[['Data_Value_x','Data_Value_y','day_mont','in_year','temp_max','temp_min']]



final_df=comp_df[(comp_df['temp_max']>comp_df['Data_Value_x']) | (comp_df['temp_min']<comp_df['Data_Value_y']) ]


# In[146]:

final_df_1=comp_df[(comp_df['temp_max']>comp_df['Data_Value_x'])]


final_df_2=comp_df[(comp_df['temp_min']<comp_df['Data_Value_y'])]



final_df_2.drop('temp_max',axis=1,inplace=True)

final_df_1.drop('temp_min',axis=1,inplace=True)




final_df_1.columns=['Data_Value_x', 'Data_Value_y', 'day_mont', 'in_year', 'temp']

final_df_2.columns=['Data_Value_x', 'Data_Value_y', 'day_mont', 'in_year', 'temp']



final_df_2.drop([292],inplace=True)



e = final_df['in_year'].values



bigdata = final_df_1.append(final_df_2)


bigdata = bigdata.sort_values('in_year', ascending=True)

fig= plt.figure(figsize=(15,15))
plt.plot(observation_dates ,max_min_df['Data_Value_x'],max_min_df['in_year'],max_min_df['Data_Value_y'])
ax=plt.gca()
myFmt = mdates.DateFormatter('%d-%m')
ax.xaxis.set_major_formatter(myFmt)
x = plt.gca().xaxis
for item in x.get_ticklabels():
    item.set_rotation(45)
#ax.set_xticks(range(365))
ax.set_xlabel('Date of Year')
ax.set_ylabel('Temperature(in tenths of degrees C)')
ax.set_title('Record Low and High temp by day over the period 2005-2014')
plt.gca().fill_between(d, 
                       max_min_df['Data_Value_x'], max_min_df['Data_Value_y'], 
                       facecolor='blue', 
                       alpha=0.25)
plt.plot(bigdata['in_year'], bigdata['temp'], 'o',c='black')
plt.xticks(rotation='vertical')
#plt.legend(loc=4, frameon=False, title='Legend')
plt.legend(title= 'Legend', labels=['Record High Temp(2005-14)','Record Low Temp(2005-14)','Days in 2015 breaking record max/min of 2004-2014'])
plt.show()

