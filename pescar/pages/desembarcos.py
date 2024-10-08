import streamlit as st
from streamlit_echarts import st_echarts
import pandas as pd
import numpy as np
import base64



PUERTOS_REF = {
    'Buenos Aires': [
        'BAHIA BLANCA',
        'GRAL.LAVALLE',
        'MAR DEL PLATA',
        'NECOCHEA/QUEQUEN',
        'RIO SALADO',
        'ROSALES',
        'SAN CLEMENTE DEL TUYÚ',
        'Otros puertos Bs. As.'
    ],
    'Rio Negro': [
        'SAN ANTONIO ESTE',
        'SAN ANTONIO OESTE'
    ],
    'Chubut': [
        'CALETA CORDOVA',
        'CAMARONES',
        'COMODORO RIVADAVIA',
        'PUERTO MADRYN',
        'RAWSON'
    ],
    'Santa Cruz': [
        'CALETA OLIVIA/PAULA',
        'PTO. DESEADO',
        'SAN JULIAN'
    ],
    'Tierra del Fuego': [
        'ALMANZA',
        'USHUAIA'
    ],
    'Otros puertos': [
        'Otros puertos'
    ]
}

SVGS = {
    "Crustáceos": "data/crab.svg",
    "Moluscos": "data/squid.svg",
    "Peces": "data/fish.svg",
}

def render_svg(svg, percentage, value, container):
    """Renders the given svg string."""
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    # svg_, perc = container.columns(1)
    container.write(html, unsafe_allow_html=True)
    container.write(f"{perc.round(2)} %")


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
## Capturas Marítimas por Puerto y Especie (2014 -2024)
"""
)


full_data = pd.read_csv('data/desembarques_2014_2024.csv')
ton_especie = full_data[['año', 'provincia', 'puerto', 'especie_tipo', 'toneladas']].groupby(['provincia', 'puerto', 'especie_tipo', 'año']).sum()


# Filtros
filters, chart, percentages = st.columns([0.20, 0.75, 0.05])

# Año
start_year, end_year = filters.select_slider(
    "Año",
    options=['2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024'],
    value=('2014', '2024'),
)

# Provincia
provincia = filters.selectbox(
    'Provincia',
    ('Buenos Aires', 'Rio Negro', 'Chubut', 'Santa Cruz', 'Tierra del Fuego', 'Otros puertos'),
)

# Puerto
puerto = filters.selectbox(
    'Puerto',
    PUERTOS_REF.get(provincia, [])
)

# Especie
available_species = set(k[0] for k in list(ton_especie['toneladas'][provincia][puerto].to_dict().keys()))
especies = filters.multiselect(
    'Especie',
    available_species
)

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
        # 'stack': '总量',
        'areaStyle': {},
        'emphasis': {'focus': 'series'},
        'data': [round(v,2) for v in list(yearly.values())],
    }
    series.append(meta_data)

options = {
    'title': {'text': 'Capturas Marítimas por Especie (Tn)', 'subtext': f'{puerto}', 'x':'left'},
    'tooltip': {
        'trigger': 'axis',
        'axisPointer': {'type': 'cross', 'label': {'backgroundColor': '#6a7985'}},
        },
    'legend': {'data': list(available_species)},
    'toolbox': {'feature': {'saveAsImage': {}}},
    'grid': {'top':'20%', 'left': '3%', 'right': '4%', 'bottom': '3%', 'containLabel': True},
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
    render_svg(open(svg).read(), perc, v, container)