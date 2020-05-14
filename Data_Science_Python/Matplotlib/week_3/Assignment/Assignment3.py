import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
np.random.seed(12345)

df = pd.DataFrame([np.random.normal(32000,200000,3650), 
                   np.random.normal(43000,100000,3650), 
                   np.random.normal(43500,140000,3650), 
                   np.random.normal(48000,70000,3650)], 
                  index=[1992,1993,1994,1995])



data = df.T


data_1992 = data[[1992]]
data_1992['year']=1992
data_1992.columns=['values', 'year']
data_1993 = data[[1993]]
data_1993['year']=1993
data_1993.columns=['values', 'year']
data_1994 = data[[1994]]
data_1994['year']=1994
data_1994.columns=['values', 'year']
data_1995 = data[[1995]]
data_1995['year']=1995
data_1995.columns=['values', 'year']

big_data = pd.concat([data_1992,data_1993,data_1994,data_1995], axis=0)
big_data.reset_index(inplace=True,drop=True)


labels =[1992, 1993, 1994, 1995]
mean_ = [data[1992].mean(),data[1993].mean(),data[1994].mean(),data[1995].mean()]
std_ = [1.96*((data[1992].std())/np.sqrt(3650)), 1.96*((data[1993].std())/np.sqrt(3650))
        ,1.96*((data[1994].std())/np.sqrt(3650)),1.96*((data[1995].std())/np.sqrt(3650))]
x_pos = np.arange(len(labels))

from matplotlib.cm import ScalarMappable


ci_lb=np.array(mean_)-np.array(std_)
ci_ub=np.array(mean_)+np.array(std_)


l=[]
y=int(input('Enter Y value: '))
data_color = [(x-y) for x in mean_]
for i in range(len(data_color)):
    if (y>ci_lb[i] and y<ci_ub[i]):
        l.append(0.5/((ci_ub[i]-ci_lb[i])/10000))
    elif (y>ci_lb[i] and y>ci_ub[i]):
        l.append(0)
    elif (y<ci_lb[i] and y<ci_ub[i]):
        l.append(1)
data_color=l
my_cmap = plt.cm.get_cmap('seismic')
colors = my_cmap(data_color)
fig, ax = plt.subplots()
barlist=ax.bar(x_pos, mean_, yerr=std_, align='center', ecolor='black', capsize=10,color=colors)
fig.set_size_inches(13.5, 8.5)
plt.axhline(y=y, color='slategrey', linestyle='-')
ax.set_ylabel('mean_values')
ax.set_xlabel('year')
ax.set_xticks(x_pos)
ax.set_xticklabels(labels)
ax.yaxis.grid(True)
ax.xaxis.grid(False)
ax.set_ylim([0,52000])
sm = ScalarMappable(cmap=my_cmap)
sm.set_array([])

cbar = plt.colorbar(sm)
cbar.set_label('Color', rotation=270,labelpad=25)
plt.show()
