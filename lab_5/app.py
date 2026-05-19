import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

PROVINCES = {
    1: "Вінницька", 2: "Волинська", 3: "Дніпропетровська", 4: "Донецька", 5: "Житомирська",
    6: "Закарпатська", 7: "Запорізька", 8: "Івано-Франківська", 9: "Київська", 10: "Кіровоградська",
    11: "Луганська", 12: "Львівська", 13: "Миколаївська", 14: "Одеська", 15: "Полтавська",
    16: "Рівненська", 17: "Сумська", 18: "Тернопільська", 19: "Харківська", 20: "Херсонська",
    21: "Хмельницька", 22: "Черкаська", 23: "Чернівецька", 24: "Чернігівська", 25: "Республіка Крим"
}

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('vhi_data.csv')
    except:
        np.random.seed(42)
        years = np.repeat(np.arange(1981, 2025), 52 * 25)
        weeks = np.tile(np.repeat(np.arange(1, 53), 25), 2024-1981+1)
        provinces = np.tile(np.arange(1, 26), 52 * (2024-1981+1))
        
        df = pd.DataFrame({
            'Year': years,
            'Week': weeks,
            'Province': provinces,
            'VCI': np.random.uniform(0, 100, size=len(years)),
            'TCI': np.random.uniform(0, 100, size=len(years)),
            'VHI': np.random.uniform(0, 100, size=len(years))
        })
    df['Province_Name'] = df['Province'].map(PROVINCES)
    return df

df = load_data()

st.set_page_config(layout="wide")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title("Аналіз індексів VCI, TCI, VHI по регіонах України")

col1, col2 = st.columns([1, 3])

with col1:
    st.header("Параметри")
    
    def reset_filters():
        st.session_state.indicator = 'VHI'
        st.session_state.province = "Вінницька"
        st.session_state.week_range = (1, 52)
        st.session_state.year_range = (1981, 2024)
        st.session_state.sort_asc = False
        st.session_state.sort_desc = False

    st.button("Скинути фільтри", on_click=reset_filters)

    indicator = st.selectbox("Оберіть часовий ряд:", ('VCI', 'TCI', 'VHI'), key='indicator')
    province = st.selectbox("Оберіть область:", list(PROVINCES.values()), key='province')
    week_range = st.slider("Інтервал тижнів:", 1, 52, (1, 52), key='week_range')
    year_range = st.slider("Інтервал років:", int(df['Year'].min()), int(df['Year'].max()), 
                           (int(df['Year'].min()), int(df['Year'].max())), key='year_range')

    sort_asc = st.checkbox("Сортувати за зростанням", key='sort_asc')
    sort_desc = st.checkbox("Сортувати за спаданням", key='sort_desc')

filtered_df = df[
    (df['Province_Name'] == province) &
    (df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1]) &
    (df['Week'] >= week_range[0]) & (df['Week'] <= week_range[1])
]

if sort_asc and sort_desc:
    st.sidebar.warning("Увімкнено обидва чекбокси сортування! Дані відображаються без сортування.")
elif sort_asc:
    filtered_df = filtered_df.sort_values(by=indicator, ascending=True)
elif sort_desc:
    filtered_df = filtered_df.sort_values(by=indicator, ascending=False)

with col2:
    tab1, tab2, tab3 = st.tabs(["Таблиця даних", "Графік області", "Порівняння областей"])
    
    with tab1:
        st.subheader(f"Дані для області: {province}")
        st.dataframe(filtered_df)
        
    with tab2:
        st.subheader(f"Динаміка {indicator} ({province})")
        if not filtered_df.empty:
            plot_df = filtered_df.sort_values(by=['Year', 'Week'])
            plot_df['Time'] = plot_df['Year'].astype(str) + "-W" + plot_df['Week'].astype(str).str.zfill(2)
            
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(plot_df['Time'], plot_df[indicator], color='tab:blue')
            ax.set_xlabel("Час")
            ax.set_ylabel(indicator)
            
            n = len(plot_df['Time'])
            if n > 15:
                ax.set_xticks(ax.get_xticks()[::n//15])
            plt.xticks(rotation=45)
            st.pyplot(fig)

    with tab3:
        st.subheader(f"Порівняння середнього {indicator} по областях")
        comp_df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1]) &
                     (df['Week'] >= week_range[0]) & (df['Week'] <= week_range[1])]
        
        if not comp_df.empty:
            mean_vals = comp_df.groupby('Province_Name')[indicator].mean().reset_index()
            fig2, ax2 = plt.subplots(figsize=(10, 6))
            sns.barplot(x='Province_Name', y=indicator, data=mean_vals, ax=ax2, color='lightblue')
            
            selected_idx = mean_vals[mean_vals['Province_Name'] == province].index
            if not selected_idx.empty:
                ax2.patches[selected_idx[0]].set_color('red')

            plt.xticks(rotation=90)
            ax2.set_xlabel("Область")
            ax2.set_ylabel(f"Середнє значення {indicator}")
            st.pyplot(fig2)