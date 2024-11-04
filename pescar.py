import streamlit as st
from utils.layouts import page_config, nav_home_layout

page_config() # Config

# Gap
# gap_ = st.html("<div style='margin-top:12rem; border-bottom:1px #0E1117 solid';></div>")

title = st.html("""
<h3 style='margin-top:10rem; color:gray; padding-bottom:0;'>Visualización</h3>
""")
intro, sections = st.columns([0.6, 0.4])
intro.html("""
<h1 style='margin-top:0; padding-top:0; font-size: 4rem;'>Industria pesquera argentina</h1>
<p style='font-size:1.4rem; color:gray; '>Un acercamiento a la industria pesquera argentina en la última década. Esta herramienta permite explorar, a través de gráficos interactivos y desgloses estacionales de datos, información relacionada con la captura marítima según tipos de flota, puerto y provincia, con el objetivo de comprender la dinámica de las actividades pesqueras en distintas regiones del país.</p>
""")

nav_home = sections.container(border=False)

with nav_home:
    nav_home_layout()

questions = st.html("""
<ul style='margin-top:2rem; font-size:1.4rem; list-style-type: none;'>
<li>¿Qué provincias y puertos tienen el mayor movimiento de la industria pesquera nacional?</li>
<li>¿Cómo fluctúa el tonelaje de diferentes especies a través de los años y los tipos de flotas?</li>
<li>¿Cuáles son las principales especies capturadas por las distintas flotas en diferentes provincias y con que estacionalidad?</li>
</ul>
""")

