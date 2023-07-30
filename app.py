# %%
import yfinance as yf
import pandas as pd
import streamlit as st
from pandas.tseries.offsets import DateOffset

# %%
# tickers=pd.read_csv('ind_nifty100list.csv',usecols=['Symbol_yf'])['Symbol_yf'].to_list()
tickers=(pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0].Symbol).to_list()

# %%
@st.cache_data
def get_data():
    df=yf.download(tickers,start='2018-01-01')
    df=df['Close']
    return df

# %%
df=get_data()

# %%
st.title('Index Component Performance of S&P 500')

# %%
n=st.number_input('Performance Horizon (Months)',min_value=1,max_value=24)

# %%
def get_ret(df,n):
    previous_prices=df[:df.index[-1]-DateOffset(months=n)].tail(1).squeeze()
    recent_prices=df.loc[df.index[-1]]
    ret_df=(recent_prices/previous_prices-1)*100
    return previous_prices.name,ret_df

# %%
date,ret_df=get_ret(df,n)

# %%
winners,losers=ret_df.nlargest(10),ret_df.nsmallest(10)

# %%
winners.name,losers.name='winners','losers'

# %%
st.table(winners)
st.table(losers)

# %%
winner_pick=st.selectbox('Pick a Winner to visualize:',winners.index)
st.line_chart(df[winner_pick][date:])

loser_pick=st.selectbox('Pick a Loser to visualize:',losers.index)
st.line_chart(df[loser_pick][date:])


