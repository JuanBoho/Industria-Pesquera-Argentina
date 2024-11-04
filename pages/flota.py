import pandas as pd
import streamlit as st
from streamlit_echarts import st_echarts
from utils.layouts import page_config, nav_layout

page_config() # Config
nav_layout('flota') # Nav


st.header("Capturas Marítimas por Embarcación (2014 -2024)", anchor=False)

# UI - Year Select
years = [str(y) for y in range(2014,2025,1)]
year_select, gap = st.columns([0.2, 0.8])
year = year_select.selectbox('Año', tuple(years))


# Data
full_data = pd.read_csv('data/desembarques_2014_2024.csv')


# Group
idx_cols = ['año', 'especie_tipo', 'flota', 'toneladas']
gr_cols = ['año', 'flota', 'especie_tipo']
total_flota_especie = full_data[idx_cols].groupby(gr_cols).sum()
total_flota_especie = total_flota_especie['toneladas'][int(year)].reset_index()


# Data preparation
categories = list(total_flota_especie['especie_tipo'].value_counts().to_dict().keys())
fleet_types = list(total_flota_especie['flota'].value_counts().to_dict().keys())
group_ = ['flota', 'especie_tipo']
pivot_data = total_flota_especie.groupby(group_)['toneladas'].sum().unstack(fill_value=0)


# Flota
fleet_types = pivot_data.index.tolist()

# Especies
categories = pivot_data.columns.tolist()


# Capturas por flota y especie
data_crustaceos = [round(d,2) for d in pivot_data['Crustáceos'].tolist()] if 'Crustáceos' in pivot_data else []
data_moluscos = [round(d,2) for d in pivot_data['Moluscos'].tolist()] if 'Moluscos' in pivot_data else []
data_peces = [round(d,2) for d in pivot_data['Peces'].tolist()] if 'Peces' in pivot_data else []


# Plot
options = {
    'title': {
        'text': 'Capturas por Flota y Especie',
        'subtext': f'{year} - En toneladas',
        'x':'left',
        'textStyle': {
            'color': '#fff',
            'fontSize': 20,
        },
        'subtextStyle': {
            'color': '#eee',
            'fontSize': 14,
        }
    },
    'tooltip': {
        'trigger': 'axis',
        'axisPointer': {'type': 'shadow'}
    },
    'legend': {
        'data': categories,
        'textStyle': {'color': '#ccc'},
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

st_echarts(options=options, height='400px')