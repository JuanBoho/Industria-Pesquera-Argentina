import streamlit as st
from streamlit_echarts import st_echarts
import pandas as pd
import numpy as np
import base64



ESPECIES_REF = {
    "Peces": [
        "Abadejo",
        "Anchoa de banco",
        "Anchoíta",
        "Atunes nep",
        "Bacalao austral",
        "Bagre",
        "Bathyraja",
        "Besugo",
        "Bonito",
        "Brótola",
        "Burriqueta",
        "Caballa",
        "Cabrilla",
        "Castañeta",
        "Cazón",
        "Chernia",
        "Chucho",
        "Chanchito",
        "Cojinova",
        "Congrio",
        "Congrio de profundidad",
        "Cornalito",
        "Corvina blanca",
        "Corvina negra",
        "Gatuzo",
        "Granadero",
        "Jurel",
        "Lenguados nep",
        "Lisa",
        "Merluza austral",
        "Merluza de cola",
        "Merluza hubbsi",
        "Merluza negra",
        "Mero",
        "Morena",
        "Notothenia",
        "Palometa",
        "Pampanito",
        "Papafigo",
        "Pargo",
        "Pejerrey",
        "Pescadilla",
        "Pescadilla real",
        "Pez ángel",
        "Pez espada",
        "Pez gallo",
        "Pez limón",
        "Pez palo",
        "Pez sable",
        "Pez sierra",
        "Polaca",
        "Raya cola corta",
        "Raya de círculos",
        "Raya hocicuda / picuda",
        "Raya lisa",
        "Raya marmolada",
        "Raya pintada",
        "Rayas nep",
        "Raya marrón oscuro",
        "Raya platana",
        "Raya espinosa",
        "Tiburón gris      ",
        "Tiburón sardinero",
        "Róbalo",
        "Rubio",
        "Salmón de mar",
        "Salmonete",
        "Saraca",
        "Sargo",
        "Savorín",
        "Tiburón bacota",
        "Tiburón espinoso",
        "Tiburón gris",
        "Tiburón martillo",
        "Tiburón moteado",
        "Tiburón pintaroja",
        "Tiburones nep",
        "Testolín",
        "Otras especies de peces",
        "Otros peces"
    ],
    "Crustáceos": [
        "Camarón",
        "Cangrejo",
        "Cangrejo rojo",
        "Centolla",
        "Langostino",
        "Centollón",
        "Otros crustáceos"
    ],
    "Moluscos": [
        "Almejas nep",
        "Calamar Illex",
        "Calamar Loligo",
        "Calamar Martialia",
        "Calamar patagónico",
        "Caracol",
        "Caracol negro",
        "Mejillón",
        "Pulpitos",
        "Pulpos nep",
        "Vieira",
        "Cholga",
        "Panopea",
        "Navaja",
        "Otros moluscos"
    ]
}




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
## Capturas Marítimas por Animal (2014 -2024)
"""
)

full_data = pd.read_csv('data/desembarques_2014_2024.csv')



# Filtros
top_container = st.container(border=True)
filters, gap, totals = top_container.columns([0.45, 0.1, 0.45])


filt_esp, filt_animal = filters.columns([0.5, 0.5])

# Especie tipo
especie_tipo = filt_esp.selectbox(
    'Especie',
    ('Peces', 'Crustáceos', 'Moluscos'),
)

# Animal
animal = filt_animal.selectbox(
    'Animal',
    ESPECIES_REF.get(especie_tipo, [])
)



# Totales
total_cap, mean_anual = totals.columns([0.5, 0.5])
# Total periodo
ton_especie = full_data[['año','especie_tipo', 'especie', 'toneladas']].groupby(['especie_tipo', 'especie', 'año']).sum()
total_ton_especie = ton_especie['toneladas'][especie_tipo][animal].sum()
total_cap.markdown('##### Total Captura')
total_cap.header(f'{total_ton_especie} Tn.')

# Media anual
media_anual_especie = ton_especie['toneladas'][especie_tipo][animal].mean()

mean_anual.markdown('##### Media Anual')
mean_anual.header(f'{round(media_anual_especie,2)} Tn.')


chart, percentages = st.columns([0.50, 0.50])
chart_container = chart.container(border=True)


#   ESTACIONALIDAD: MEDIA MENSUAL

# Vals
ton_especie_mean = full_data[['mes', 'especie_tipo', 'especie', 'toneladas']].groupby(['especie_tipo', 'especie', 'mes']).mean()
values = ton_especie_mean['toneladas'][especie_tipo][animal].to_dict().values()

# Plot
options = {
    'title': {'text': 'Media Mensual', 'subtext': f'{animal}', 'x':'left'},
    "xAxis": {
        "type": "category",
        'splitLine': {
            'show': True,
            'interval': 2,
            'lineStyle': {'opacity':0.1, 'color': '#fff'}
        },
        "data": ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"],
    },
    "yAxis": {
        "type": "value",
        'show':False
    },
    "series": [{"data": [round(v,2) for v in list(values)], "type": "line", 'smooth': True, 'showSymbol': False }],
}

with chart_container:
    st_echarts(options=options, height='400px')



#   TOTAL POR PUERTO

# Vals
ton_especie_puerto = full_data[['puerto','especie_tipo', 'especie', 'toneladas']].groupby(['especie_tipo', 'especie', 'puerto']).sum()
especie_puerto = ton_especie_puerto['toneladas'][especie_tipo][animal].to_dict()
especie_puerto_ = [{"value": round((especie_puerto[p] * 100 ) / total_ton_especie, 2), "name": p} for p in especie_puerto]

# Container
chart_2_container = percentages.container(border=True)

# Plot
options = {
    'title': {'text': 'Capturas por Puerto', 'subtext': f'{animal}', 'x':'left'},
    "tooltip": {"trigger": "item"},
    "legend": {"top": "5%", "left": "right", "orient": "vertical"},
    "series": [
        {
            "name": "Capturas en Tn.",
            "type": "pie",
            "radius": ["50%", "90%"],
            "avoidLabelOverlap": False,
            "itemStyle": {
                "borderRadius": 10,
                "borderColor": "#333",
                "borderWidth": 1,
            },
            "label": {"show": True, "position": "center"},
            "emphasis": {
                "label": {"show": True, "fontSize": "22", "fontWeight": "bold"}
            },
            "labelLine": {"show": True},
            "data": especie_puerto_,
            'center': ['30%' if len(especie_puerto_) > 15 else '50%', '50%']
        }
    ],
}

with chart_2_container:
    st_echarts(options=options, height='400px')

