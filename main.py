import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Research", layout="wide")

st.snow()

@st.cache_data
def load_data() -> yf.Ticker:
    tickerSymbol = 'AAPL'
    tickerData = yf.Ticker(tickerSymbol)
    return tickerData.history(period='1d', start='2010-01-01', end='2024-12-17')

st.write("""
    #  Shown are the stock **closing price** and ***volume*** of Apple!
    ## Closing Price
""")

tickerDf = load_data()

st.line_chart(tickerDf.Close)

st.write("""
    ## Volume Price
""")

st.line_chart(tickerDf.Volume)


with st.sidebar:
    with open('images/AAPL_ticker_close.svg', 'rb') as file:
        st.download_button(
            label='Download svg file with closing price',
            data = file,
            file_name='AAPL_ticker_close.svg',
            mime='image/svg'
        )

    with open('images/AAPL_ticker_volume.svg', 'rb') as file1:
        st.download_button(
            label='Download svg file with volume price',
            data = file1,
            file_name='AAPL_ticker_volume.svg',
            mime='image/svg'
        )