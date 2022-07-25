import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import streamlit as st


@st.cache
def ytd(ticker):
    df = yf.download(ticker , period= 'ytd')
    df_close = df['Close']
    df_ytd = df_close.div(df_close.iloc[0]).mul(100)
    return df_ytd
def extract_mCap(ticker_list):
    df = pd.DataFrame()
    for stock in ticker_list :
        fin_data = yf.Ticker(stock).get_info()
        df.loc[str(stock),'marketCap']=fin_data['marketCap']
    return df
def extract_growth(ticker_list):
    df = pd.DataFrame()
    for stock in ticker_list :
        fin_data = yf.Ticker(stock).get_analysis()
        df.loc[str(stock),'EST GROWTH']=fin_data.loc['0Y','Revenue Estimate Growth']
    return df
def extract_value(ticker_list ,attr):
    df = pd.DataFrame()
    for stock in ticker_list :
        df.loc[str(stock),str(attr)]= yf.Ticker(stock).financials.iloc[:,0][attr]
    return df
def make_table(ticker_list):
    ##Creating table for P/S , Revenue , Estimate Growth ##
    rev = extract_value(ticker_list,'Total Revenue').dropna(axis=0)
    ##sum_rev = pd.DataFrame(rev.sum(axis=1),columns = ['Revenue'])
    cap = extract_mCap(ticker_list)
    growth = extract_growth(ticker_list)
    table = rev.join(cap).join(growth)
    table['P/S'] = table['marketCap'].div(table['Total Revenue'])
    return table
html= pd.read_html('https://stockmarketmba.com/stocksinthesp500.php')
symbol = [i for i in html[0]['Symbol']]

path = 'nasdaq_screener.csv'
world_index_path = 'World Index.csv'
NYSE = pd.read_csv(path)
info = pd.DataFrame(NYSE)[['Symbol','Market Cap','Country','Sector','Industry']]
world_index = pd.read_csv(world_index_path)
NYSE_ticker = [ i for i in NYSE['Symbol']]
NYSE_sector = [i for i in NYSE['Sector'].unique()]


## List of SAAS company
st.image('TECH STOCK WARRIOR (2).png')
st.title('Welcome to Tech Stock Warrior (นักรบหุ้นนอก)')
st.write('Streamlit เป็น Open-Source application ที่ออกแบบมาสำหรับ Data Sciencetist ต้องการใช้เครื่องมือในการเผยแพร่ไอเดียบน Web Application โดยไม่ต้องอาศัยความรู้ HTML CSS หรือ Java Script ให้ยุ่งยาก และ App นี้เขียนขึ้นโดย [นักรบหุ้นนอก](https://www.facebook.com/techstockwarrior) page เล็กๆที่ต้องการนำเสนอมุมมองการคิดด้านการลงทุนที่แตกต่างออกไป')
st.header('ภาพรวมของ Index ต่างๆตั้งแต่ต้นปี')
path = 'nasdaq_screener.csv'
NYSE = pd.read_csv(path)
world_index = pd.read_csv(world_index_path)
NYSE_ticker = [ i for i in NYSE['Symbol']]
NYSE_sector = [i for i in NYSE['Sector'].unique()]
index_list = [i for i in world_index['Symbol'].head(15)]
index_name = [i for i in world_index['Name'].head(15)]
index_data = yf.download(index_list , start = '2022-01-04')
index_data_fillna = index_data.fillna(method ='ffill')
index_ytd = index_data_fillna['Close'].div(index_data['Close'].iloc[0]).mul(100)
index_ytd.columns = index_name
index_ytd.drop(['Vix','BEL 20'] ,axis =1 , inplace = True)
st.line_chart(index_ytd)

html= pd.read_html('https://stockmarketmba.com/stocksinthesp500.php')
NYSE_symbol = NYSE['Symbol']
symbol = [i for i in html[0]['Symbol']]
st.title('YTD Performance')
st.write('The chart below shows how selected stock has performed YTD')
selected_stock= st.multiselect('Please select stock from list below', NYSE_symbol ,default='MSFT')
data = ytd(selected_stock)
st.line_chart(data)


st.header('The Appendix of all stock in NYSE')
st.dataframe(info)

