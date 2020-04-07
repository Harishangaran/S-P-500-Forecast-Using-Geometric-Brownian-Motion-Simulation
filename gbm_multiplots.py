# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 14:45:07 2020

@author: harishangaran

GEOMETRIC BROWNIAN MOTION

Plot multiple stock forecast using GBM.

# Parameter Definitions

# So    :   initial stock price
# dt    :   time increment -> a day in our case
# T     :   length of the prediction time horizon(how many time points to predict, same unit with dt(days))
# N     :   number of time points in the prediction time horizon -> T/dt
# t     :   array for time points in the prediction time horizon [1, 2, 3, .. , N]
# mu    :   mean of historical daily returns (drift coefficient)
# sigma :   standard deviation of historical daily returns (diffusion coefficient)
# b     :   array for brownian increments
# W     :   array for brownian path

"""

import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# Grab last 2 year price of the asset from yahoo finance
asset = yf.Ticker('^GSPC').history('504d')
asset['Daily return'] = asset['Close'].pct_change(1)
    
# Get intial price for the GBM to start
# Is the last row of the dataframe in other words latest price
So = asset['Close'][-1]

# Annualised return
mu = asset['Daily return'].mean() * 252

# Annualised standard deviation
sigma = asset['Daily return'].std() * np.sqrt(252)
T = 1
N = 504


# Define function for Geometric Brownian Motion
def GBM(seed):
    
    np.random.seed(seed)                         
    dt = 1./N                                    # time step
    b = np.random.normal(0, 1, int(N))*np.sqrt(dt)  # brownian increments
    W = np.cumsum(b)                             # brownian path   
    t = np.linspace(0,1,N+1)
    x = np.linspace(504,N+504,N+1)
    S = []
    S.append(So)
    for i in range(1,int(N+1)):
        drift = (mu - 0.5 * sigma**2) * t[i]
        diffusion = sigma * W[i-1]
        S_temp = So*np.exp(drift + diffusion)
        S.append(S_temp)
    return S, x


# Define different seed values for different random sequences
s1 = GBM(5)[0]
s2 = GBM(10)[0] 
s3 = GBM(15)[0] 
s4 = GBM(20)[0] 
x = GBM(5)[1]

# X-Axis length for the actual price plot
pt = np.linspace(0,504,504)

# Using ggplot style
plt.style.use('ggplot')

# Subplot of different scenarios
fig,axes = plt.subplots(nrows=2,ncols=2,figsize=(12,8),sharex=True, sharey=True,dpi=300)
fig.suptitle('4 Scenarios of S&P 500 price over the next 2 years using Geometric Brownian Motion')

# Define common x and y axis label
fig.text(0.52, -0.02, 'Trading Days', ha='center')
fig.text(-0.02, 0.48, 'Stock Price $', va='center', rotation='vertical')

# Plot all scenarios
axes[0,0].plot(pt,asset['Close'],label='Actual')
axes[0,0].plot(x,s1,label='Forecast')
axes[0,0].set_title('seed = 5')
axes[0,1].plot(pt,asset['Close'],label='Actual')
axes[0,1].plot(x,s2,label='Forecast')
axes[0,1].set_title('seed = 10')
axes[1,0].plot(pt,asset['Close'],label='Actual')
axes[1,0].plot(x,s3,label='Forecast')
axes[1,0].set_title('seed = 15')
axes[1,1].plot(pt,asset['Close'],label='Actual - last 2 years')
axes[1,1].plot(x,s4,label='Forecast - next 2 years')
axes[1,1].set_title('seed = 20')
plt.legend()
plt.tight_layout()

# Adjust distance of subplots from title
fig.subplots_adjust(top=0.9)

