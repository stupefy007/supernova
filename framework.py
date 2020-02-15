#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 19:55:49 2020

@author: zhuhx
"""


import pandas_datareader.data as web
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import empyrical as ep

def get_performance_summary(returns):
    stats = {'annualized_returns': ep.annual_return(returns),
             'cumulative_returns': ep.cum_returns_final(returns),
             'annual_volatility': ep.annual_volatility(returns),
             'sharpe_ratio': ep.sharpe_ratio(returns),
             'sortino_ratio': ep.sortino_ratio(returns),
             'max_drawdown': ep.max_drawdown(returns)}
    return pd.Series(stats)

# 扒SP500 Index 和成分股数据
Stockprice = web.DataReader('^GSPC', 'yahoo','2000-01-01','2019-12-31')
Stockprice.drop(['High','Low','Open','Close','Volume','Adj Close'],axis=1,inplace=True)
raw = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
symbols = raw[0]['Symbol'].tolist()
symbols.append('^GSPC')
symbols[69] = 'BRK-B'
symbols[81] = 'BF-B'

for symbol in symbols:
    data = web.DataReader(symbol, 'yahoo','2000-01-01','2019-12-31')
    Stockprice[symbol] = data['Adj Close']
Stockreturns = Stockprice.pct_change()

# 画图：Benchmark，equal-weighted portfolio
ret = Stockreturns.copy()
ret.drop('^GSPC',axis=1,inplace=True)
ew=np.ones(505)/505
Stockreturns['Portfolio_ew'] = ret.mul(ew,axis=1).sum(axis=1)
plt.figure(figsize=(16,9))
font = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 24}

((1+Stockreturns['^GSPC']).cumprod()-1).plot()
((1+Stockreturns['Portfolio_ew']).cumprod()-1).plot()
plt.legend(['SP 500','Portfolio_EW'], loc=2)
# Stockreturns['^GSPC'].cumsum().plot()
# Stockreturns['^Portfolio_ew'].cumsum().plot()
plt.grid()
plt.ylabel('Cumulative Return',size=16)
plt.xlabel('Day(s)',size=16)
plt.title('Benchmark',fontdict=font)

# performance指标

# get_performance_summary(Stockreturns['^GSPC'])
# get_performance_summary(Stockreturns['Portfolio_ew'])