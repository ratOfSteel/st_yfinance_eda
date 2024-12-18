import streamlit as st
import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib as mlp
import matplotlib.pyplot as plt

st.set_page_config(page_title="Research", layout="wide")

st.balloons()

url = 'https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv'

@st.cache_data
def load_data(url: str) -> pd.DataFrame:
    data = pd.read_csv(url)
    return data

st.write('''
    # Анализ чаевых в ресторане
''')

data = load_data(url)

@st.cache_data
def add_column() -> pd.DataFrame:
    data['time_order'] = pd.to_datetime(
        np.random.choice(
            pd.date_range(
                start=pd.to_datetime('2023-01-01'), 
                end=pd.to_datetime('2023-01-31')),
            size=data.shape[0]
        )
    )
    return data

data = add_column()
st.dataframe(data.head(5))

@st.cache_data
def convert_df(df: pd.DataFrame) -> pd.DataFrame:
   return df.to_csv(index=False).encode('utf-8')

col1, col2 = st.columns(2)

with col1:
    st.write('''
        ### График динамики чаевых во времени
    ''')

    st.line_chart(data=data, 
                x='tip', 
                y='time_order',
                x_label='Чаевые',
                y_label='Дата')

with col2:
    st.write('''
        ### Гистограмма total_bill
    ''')

    fig = plt.figure(figsize=(5, 3))
    sns.histplot(data['total_bill'], kde=True)  # kde=True добавляет кривую плотности
    plt.xlabel('Итоговый счёт')
    plt.ylabel('Частота')
    st.pyplot(plt)

# plt.savefig('images/hist_total-bill.svg', dpi=fig.dpi)

st.write('''     
    ### Cвязь между итоговым счётом и чаевыми:    
''')

st.scatter_chart(data=data, 
                 x='total_bill', 
                 y='tip', 
                 color='time',
                 x_label='Итоговый счёт',
                 y_label='Чаевые')



st.write('''
    ### Тепловая карта корреляций численных переменных
''')

col3, col4 = st.columns(2)

with col3:
    numeric_tips = data.select_dtypes(include=np.number)

    # Вычисляем матрицу корреляций
    corr_matrix = numeric_tips.corr()

    # Создаем тепловую карту
    fig1 = plt.figure(figsize=(5, 3))
    sns.heatmap(corr_matrix, 
                annot=True,
                cmap=sns.cubehelix_palette(as_cmap=True), 
                fmt='.2f', 
                vmin=0, 
                vmax=1,
                xticklabels=['Итоговый счёт', 'Чаевые', 'Размер'],
                yticklabels=['Размер', 'Чаевые', 'Итоговый счёт'])
    st.pyplot(plt)

    # plt.savefig('images/corr.svg', dpi=fig.dpi)

with col4:
    pass


with st.sidebar:
    st.download_button(
        label="Скачать набор данных",
        data=convert_df(data),
        file_name="file.csv",
        mime="text/csv",
        key='download-csv'
    )
    with open('images/grafic_tips-to-time_order.svg', 'rb') as graf1:
        st.download_button(
            label='Скачать график Динамика чаевых во времени',
            data = graf1,
            file_name='grafic_tips-to-time_order.svg',
            mime='image/svg'
        )
    with open('images/hist_total-bill.svg', 'rb') as graf2:
        st.download_button(
            label='Скачать график Итоговый счёт',
            data = graf2,
            file_name='hist_total-bill.svg',
            mime='image/svg'
        )
    with open('images/scatterplot_tips_totall_bill.svg', 'rb') as graf3:
        st.download_button(
            label='Скачать график Связь между итоговым счётом и чаевыми',
            data = graf3,
            file_name='scatterplot_tips_totall_bill.svg',
            mime='image/svg'
        )
    with open('images/corr.svg', 'rb') as graf4:
        st.download_button(
            label='Скачать график Связь между итоговым счётом и чаевыми',
            data = graf4,
            file_name='corr.svg',
            mime='image/svg'
        )
