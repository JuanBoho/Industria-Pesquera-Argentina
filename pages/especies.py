import json
import pandas as pd
import streamlit as st
from streamlit_echarts import st_echarts
from utils.utils import get_data
from utils.layouts import page_config, nav_layout

page_config() # Config
nav_layout('especies') # Nav


st.header('Capturas Marítimas por Animal (2014 -2024)', anchor=False)

# Data
ESPECIES_REF = get_data('Especies')
full_data = pd.read_csv('data/desembarques_2014_2024.csv')


# Filtros
top_container = st.container(border=True)
filters, gap, totals = top_container.columns([0.45, 0.1, 0.45])

filt_esp, filt_animal = filters.columns([0.5, 0.5])

# Especie tipo
esp_tipos = ('Peces', 'Crustáceos', 'Moluscos')
especie_tipo = filt_esp.selectbox('Especie', esp_tipos)

# Animal
esp_ = ESPECIES_REF.get(especie_tipo, [])
animal = filt_animal.selectbox('Animal', esp_)


# TOTALES
_, total_cap, mean_anual = totals.columns([0.2, 0.4, 0.4])

# Total periodo
idx_cols = ['año','especie_tipo', 'especie', 'toneladas']
gr_cols = ['especie_tipo', 'especie', 'año']
ton_especie = full_data[idx_cols].groupby(gr_cols).sum()
total_ton_especie = ton_especie['toneladas'][especie_tipo][animal].sum()

total_cap.write('Total Captura')
total_cap.subheader(f'{round(total_ton_especie,2)} Tn.', anchor=False)


# Media anual
media_anual_especie = ton_especie['toneladas'][especie_tipo][animal].mean()

mean_anual.write('Media Anual')
mean_anual.subheader(f'{round(media_anual_especie,2)} Tn.', anchor=False)


chart, percentages = st.columns([0.5, 0.5])
chart_container = chart.container(border=True)


# ESTACIONALIDAD: MEDIA MENSUAL

# Vals
idx_cols_vals = ['mes', 'especie_tipo', 'especie', 'toneladas']
gr_cols_vals = ['especie_tipo', 'especie', 'mes']
ton_especie_mean = full_data[idx_cols_vals].groupby(gr_cols_vals).mean()
values = ton_especie_mean['toneladas'][especie_tipo][animal].to_dict().values()

months = get_data('Meses')
months_formatted = [m[:3] for m in months]

# Plot
options = {
    'title': {
        'text': 'Media Mensual',
        'subtext': f'{animal}',
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
    'xAxis': {
        'type': 'category',
        'splitLine': {
            'show': True,
            'interval': 2,
            'lineStyle': {
                'opacity':0.1,
                'color': '#fff'
            }
        },
        'data': months_formatted,
    },
    'yAxis': {
        'type': 'value',
        'show':False,
    },
    'series': [{
        'data': [round(v,2) for v in list(values)],
        'type': 'line',
        'smooth': True,
        'showSymbol': False
    }],
}

# Plot
with chart_container:
    st_echarts(options=options, height='400px')


# TOTAL POR PUERTO

# Vals
idx_cols_pto = ['puerto','especie_tipo', 'especie', 'toneladas']
gr_cols_pto = ['especie_tipo', 'especie', 'puerto']
ton_especie_puerto = full_data[idx_cols_pto].groupby(gr_cols_pto).sum()
especie_puerto = ton_especie_puerto['toneladas'][especie_tipo][animal].to_dict()
especie_puerto_ = [
    {
    'value': round((especie_puerto[p] * 100 ) / total_ton_especie, 2),
    'name': p
    } for p in especie_puerto]

# Container
chart_2_container = percentages.container(border=True)

# Plot
options = {
    'title': {
        'text': 'Capturas por Puerto',
        'subtext': f'{animal}',
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
    'tooltip': {'trigger': 'item'},
    'legend': {
        'top': '5%',
        'left': 'right',
        'orient': 'vertical',
        'textStyle': {'color': '#fff'},
    },
    'series': [
        {
            'name': 'Capturas en Tn.',
            'type': 'pie',
            'radius': ['50%', '90%'],
            'avoidLabelOverlap': True,
            'itemStyle': {
                'borderRadius': 10,
                'borderColor': '#333',
                'borderWidth': 1,
            },
            'label': {
                'show': False,
                'position': 'center'
            },
            'emphasis': {
                'label': {
                    'show': True,
                    'color': '#fff'
                }
            },
            'labelLine': {'show': False},
            'data': especie_puerto_,
            'center': ['35%' if len(especie_puerto_) > 15 else '50%', '50%'],
            'top': '5%'
        }
    ],
}

with chart_2_container:
    st_echarts(options=options, height='400px')

