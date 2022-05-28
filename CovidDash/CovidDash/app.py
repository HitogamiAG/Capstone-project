import json
import streamlit as st
import pandas as pd
import requests
import io
from sqlalchemy import create_engine
import os
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import plotly as pt
import plotly.graph_objs as go
import plotly.express as px
from updateData import updateFunction
from getData import getDataFromDB

updateFunction()

#make page on full screen
#st.set_page_config(layout="wide")

# declare the variable
fiat = ['USDT']
tokens = ['AAVE', 'ADA']
st.title('Welcome to the Crypto Analysis App')
st.markdown("""
This application provides a brief analysis of the "Coinbase" crypto market
""")
# code for gif
def lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
crypto_gif = lottie_url("https://assets5.lottiefiles.com/packages/lf20_pmyyjcm7.json")
st_lottie(crypto_gif, quality="high", key="hello")

# declaring columns for sidebar,tables, and for graphs
col1 = st.sidebar
col2, col3 = st.columns((2,1))

select_token = col1.selectbox('Select criptocurrency', tokens)
select_fiat = col1.selectbox('select fiat',fiat)

# filters selectbox
#st.sidebar.title("Filters")
#select_token = st.sidebar.selectbox('Tokens', tokens)
#select_fiat = st.sidebar.selectbox('Fiat', fiat)

with st.sidebar:
    selected = option_menu(
        menu_title="Main page",
        options=["Tables", "Charts"],
        icons=["table", "bar-chart-fill"],
        default_index=0
    )
if selected == "Tables":
    st.title(f"Now you are on page with visualization {selected}")
if selected == "Charts":
    st.title(f"Here you can see the visualization part {selected}")


table_name_day = select_token + select_fiat + '_d'

df_day = getDataFromDB(table_name_day)

# ---------------------------
# VISUALIZAION
# ---------------------------
df_change_day_1d = pd.concat([df_day.symbol, df_day.date, df_day.open],axis=1)
df_change_day_1d = df_change_day_1d.set_index('symbol')
open_price = df_change_day_1d['open'].to_list()

list2 = [0]
for i in range(1, len(open_price)):
    list2.append(open_price[i]-open_price[i-1])
df_change_day_1d['percentage_change_1d'] = list2

df_change_day_1d['color'] = df_change_day_1d['percentage_change_1d'].map(lambda x:'red' if x<0 else 'green')

# to change color of "% change" column
fill_colors = []
n = len(df_change_day_1d)
for col in df_change_day_1d:
    if col!='percentage_change_1d':
        fill_colors.append(['white']*n)
    else:
        fill_colors.append(df_change_day_1d["color"].to_list())
col2.write(df_change_day_1d)

df_change_day_1d['positive_change'] = df_change_day_1d['percentage_change_1d'] > 0
df_change_day_1d_few = df_change_day_1d.iloc[0:5,:] # cutting only few rows to show how does price change

col3.write('Daily % change of the coin')

plt.figure(figsize=(5,5))
plt.subplots_adjust(top = 1, bottom = 0)
colors = ['green' if x > 0 else 'red' for x in df_change_day_1d_few['percentage_change_1d']]
df_change_day_1d_few['percentage_change_1d'].plot(kind='barh', color=df_change_day_1d_few.positive_change.map({True: 'g', False: 'r'}))
col3.pyplot(plt)

fig1 = go.Figure()
fig1.add_scattergl(x=df_day.index, y=df_day.close,
                  line={'color': 'green'},name='Up trend')
fig1.add_scattergl(x=df_day.index, y=df_day.close.where(df_day.close <= df_day.open[1]),
                  line={'color': 'red'},name='Down trend')
fig1.add_hline(y=df_day.open[0])
fig1.update_layout(go.Layout(xaxis = {'showgrid': False},
                            yaxis = {'showgrid': False}),
                  title=f'{select_token} Daily Trends in Comparison to Open Price',
                  yaxis_title=f'Price ({select_fiat})',template='plotly_dark',
                  xaxis_rangeslider_visible=False)
st.plotly_chart(fig1, use_container_width=True)


df_day_MA = df_day.copy()
df_day_MA['avg_25'] = df_day_MA.high.rolling(window = 25).mean()
df_day_MA['avg_50'] = df_day_MA.high.rolling(window = 50).mean()
df_day_MA['avg_75'] = df_day_MA.high.rolling(window = 75).mean()

fig2 = go.Figure(data=
                [go.Candlestick(x=df_day_MA.index,
                                open=df_day_MA.open,
                                high=df_day_MA.high,
                                low=df_day_MA.low,
                                close=df_day_MA.close,
                                name=f'{select_token}'),
                 go.Scatter(x=df_day_MA.index, y=df_day_MA.avg_25,
                            line=dict(color='yellow',width=1),name='MA25'),
                 go.Scatter(x=df_day_MA.index, y=df_day_MA.avg_50,
                            line=dict(color='green',width=1),name='MA50'),
                 go.Scatter(x=df_day_MA.index, y=df_day_MA.avg_75,
                            line=dict(color='red',width=1),name='MA75')])

fig2.update_layout(go.Layout(xaxis = {'showgrid': False},
                            yaxis = {'showgrid': False}),
                  title=f'{select_token} Price Fluctuation with Moving Averages',
                  yaxis_title=f'Price ({select_fiat})',
                  xaxis_rangeslider_visible=False)

st.plotly_chart(fig2, use_container_width=True)


df_day_few = df_day.iloc[0:20,:]
df_day_few['MA5'] = df_day_few.open.rolling(window = 5).mean()

my_pie_chart = px.pie(df_day_few,
                      title = 'Pie Chart',
                      values = 'MA5',
                      names = 'date')
st.plotly_chart(my_pie_chart)

st.write(df_day)

# -----------------------------
