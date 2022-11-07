# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 09:12:35 2021

@author: zanna
"""
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame
import os
import numpy as np
import datetime
os.chdir('C:/Users/zanna/Downloads/')
df=pd.read_parquet('taq_20210301.parquet')
print(df)


day = '2021-03-01'
df['ts'] = pd.to_datetime(day + ' '+ (df['Time']).astype(str), format = '%Y-%m-%d %H%M%S%f')


ret=df.set_index('ts').groupby('Symbol').resample('1min').last()
ret=ret.reset_index(0, drop=True)
ret['ret']=ret.groupby('Symbol')['Trade Price'].pct_change()

ret
df[df.Symbol=='DIS']

dis=ret[ret.Symbol == 'DIS']

x=dis.index.values
y=dis['Trade Price'].values

fig, ax= plt.subplots(figsize=(7,2))
ax.plot(x,y,color='dodgerblue', label= 'Disney Stock Price')
ax.legend(loc='upper left')
ax.plot(x,y)
ax.set_ylim(192, 198)
ax.set_yticks([192,194, 196, 198])
ax.set_yticklabels(['$192',194, 196, '$198'])
ax.set_ylabel('price')
ax.set_xlabel('time')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.show()
fig.savefig('dis_price.jpeg', dpi=400)
#analyze retail activity
#what type of stocks do retail traders like

df['dvol']=df['Trade Volume']*df['Trade Price']
daily=pd.DataFrame()
daily['dvol']=df.groupby('Symbol').dvol.sum()
daily['avg_price']=df.groupby('Symbol')['Trade Price'].mean()
daily['ret_vol']=ret.groupby('Symbol').ret.std()  #volatility
daily['avg_td_size']=df.groupby('Symbol')['Trade Volume'].mean()
daily
daily.dvol.rank(pct=True)
daily['retail_rank']=daily.dvol.rank(pct=True)//.1  # decile 
daily.groupby('retail_rank').avg_price.mean().plot.bar()
daily.groupby('retail_rank').ret_vol.mean().plot.bar()
