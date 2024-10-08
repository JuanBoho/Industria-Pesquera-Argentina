import streamlit as st
from streamlit_echarts import st_echarts
import pandas as pd

st.set_page_config(page_title='Industria Pesquera Argentina', layout='wide')
st.markdown(
"""
# Visualización de la Industria Pesquera Argentina
""")

home, desembarcos, especies, flota= st.columns(4)
if home.button("Inicio", use_container_width=True):
    st.switch_page("pescar.py")
if desembarcos.button("Desembarcos", use_container_width=True):
    st.switch_page("pages/desembarcos.py")
if especies.button("Especies", use_container_width=True):
    st.switch_page("pages/especies.py")
if flota.button("Flota", use_container_width=True):
    st.switch_page("pages/flota.py")


st.markdown(
"""
## Capturas Marítimas por Embarcación (2014 -2024)
"""
)


full_data = pd.read_csv('data/desembarques_2014_2024.csv')

col_1, col2 = st.columns([0.2, 0.8])
year = col_1.selectbox(
    'Año',
    ('2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024'),
)

print(year)

total_flota_especie = full_data[['año', 'especie_tipo', 'flota', 'toneladas']].groupby(['año', 'flota', 'especie_tipo']).sum()
total_flota_especie = total_flota_especie['toneladas'][int(year)].reset_index()
# Data preparation
categories = list(total_flota_especie['especie_tipo'].value_counts().to_dict().keys())
fleet_types = list(total_flota_especie['flota'].value_counts().to_dict().keys())


pivot_data = total_flota_especie.groupby(['flota', 'especie_tipo'])['toneladas'].sum().unstack(fill_value=0)

# Get the fleet types (index of the pivot table)
fleet_types = pivot_data.index.tolist()

# Get the species types (columns of the pivot table)
categories = pivot_data.columns.tolist()

# Get the data for each species type
data_crustaceos = [round(d,2) for d in pivot_data['Crustáceos'].tolist()] if 'Crustáceos' in pivot_data else []
data_moluscos = [round(d,2) for d in pivot_data['Moluscos'].tolist()] if 'Moluscos' in pivot_data else []
data_peces = [round(d,2) for d in pivot_data['Peces'].tolist()] if 'Peces' in pivot_data else []



options = {
    'title': {'text': 'Capturas por Flota y Especie', 'subtext': f'{year}', 'x':'left'},
    'tooltip': {
        'trigger': 'axis',
        'axisPointer': {'type': 'shadow'}
    },
    'legend': {
        'data': categories
    },
    'grid': {
        'left': '3%',
        'right': '4%',
        'bottom': '3%',
        'containLabel': True
    },
    'xAxis': {
        'type': 'value'
    },
    'yAxis': {
        'type': 'category',
        'data': fleet_types
    },
    'series': [
        {
            'name': 'Crustáceos',
            'type': 'bar',
            'stack': 'total',
            'label': {'show': False},
            'data': data_crustaceos
        },
        {
            'name': 'Moluscos',
            'type': 'bar',
            'stack': 'total',
            'label': {'show': False},
            'data': data_moluscos
        },
        {
            'name': 'Peces',
            'type': 'bar',
            'stack': 'total',
            'label': {'show': False},
            'data': data_peces
        }
    ]
}

# Display chart in Streamlit
st_echarts(options=options, height='400px')