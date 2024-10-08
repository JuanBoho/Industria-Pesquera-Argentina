import streamlit as st

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

st.markdown("""

___
### **Introducción**
#### Esta aplicación ofrece una visión de la industria pesquera Argentina entre los años 2014 y 2024. Centrándose en la captura marítima por tipos de flota, puerto y provincia. Con gráficos interactivos y desglose de los datos, esta herramienta permite explorar la información en busca de comprender la dinámica de las actividades pesqueras en diferentes provincias del país en la última década.

#### - ¿Qué provincias y puertos tienen el mayor movimiento de la industria pesquera nacional?
#### - ¿Cómo fluctúa el tonelaje de diferentes especies a través de los años y los tipos de flotas?
#### - ¿Cuáles son las principales especies capturadas por las distintas flotas en diferentes provincias y con que estacionalidad?
"""
)