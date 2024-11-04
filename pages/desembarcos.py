import base64
import pandas as pd
import streamlit as st
from streamlit_echarts import st_echarts
from utils.utils import get_data
from utils.layouts import page_config, nav_layout


page_config() # Config
nav_layout('desembarcos') # Nav


st.header("Capturas Marítimas por Puerto y Especie (2014 -2024)", anchor=False)


def render_svg(svg, container):
    """Renders the given svg string."""
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    container.write(html, unsafe_allow_html=True)
    container.write(f"{perc.round(2)} %")


# Data
SVGS = get_data('SVGS')
PUERTOS_REF = get_data('Puertos')
full_data = pd.read_csv('data/desembarques_2014_2024.csv')


# Group
idx_cols = ['año', 'provincia', 'puerto', 'especie_tipo', 'toneladas']
gr_cols = ['provincia', 'puerto', 'especie_tipo', 'año']
ton_especie = full_data[idx_cols].groupby(gr_cols).sum()


# Filtros
filters, chart, percentages = st.columns([0.20, 0.75, 0.05])

# Año
years = [str(y) for y in range(2014,2025,1)]
start_year, end_year = filters.select_slider(
    "Año",
    options=years,
    value=('2014', '2024'),
)

# Provincia
provincias = tuple(PUERTOS_REF.keys())
provincia = filters.selectbox('Provincia', provincias)

# Puerto
puerto = filters.selectbox('Puerto', PUERTOS_REF.get(provincia, []))

# Especie
available_species = set(k[0] for k in list(ton_especie['toneladas'][provincia][puerto].to_dict().keys()))
especies = filters.multiselect('Especie', available_species)

# Totales por especie
total_especie_puerto = {}
for especie in especies:
    total_puerto = ton_especie['toneladas'][provincia][puerto].sum()
    total_especie_puerto[f'{especie}'] = ton_especie['toneladas'][provincia][puerto][especie].sum().round(2)


# Plots
series = []
for especie in especies:
    yearly = ton_especie['toneladas'][provincia][puerto][especie].to_dict()
    meta_data = {
        'name': especie,
        'type': 'line',
        'areaStyle': {},
        'emphasis': {'focus': 'series'},
        'data': [round(v,2) for v in list(yearly.values())],
    }
    series.append(meta_data)

options = {
    'title': {
        'text': 'Capturas Marítimas por Especie (Tn)',
        'subtext': f'{puerto.capitalize()}',
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
        'axisPointer': {'type': 'cross', 'label': {'backgroundColor': '#6a7985'}},
        },
    'legend': { 
        'data': list(available_species),
        'textStyle': {'color': '#ccc'},
        'left': 'center'
    },
    'toolbox': { 'feature': {'saveAsImage': {}} },
    'grid': {
        'top': '20%',
        'left': '3%',
        'right': '4%',
        'bottom': '2%',
        'containLabel': True
    },
    'xAxis': {
        'type': 'category',
        'data': [y for y in range(int(start_year), int(end_year)+1,1)],
    },
    'yAxis': {'type': 'value', 'name':'Tn'},
    'series': series
}


chart_container = chart.container(border=True)

with chart_container:
    st_echarts(options=options, height='500px')

container = percentages.container(border=False)
container.write("% Total \n Especie")
for k,v in total_especie_puerto.items():
    perc = (v * 100) / total_puerto
    svg = SVGS[k]
    render_svg(open(svg).read(), container)