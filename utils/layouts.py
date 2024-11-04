import streamlit as st


def page_config():
    title = f'Industria Pesquera Argentina'
    st.set_page_config(page_title=title, layout='wide')


def nav_layout(pg=''):

    btn_1 = 'primary' if pg == 'desembarcos' else 'secondary'
    btn_2 = 'primary' if pg == 'especies' else 'secondary'
    btn_3 = 'primary' if pg == 'flota' else 'secondary'

    
    st.title("Visualización de la Industria Pesquera Argentina", anchor=False)
    home, desembarcos, especies, flota= st.columns(4)
    if home.button("Inicio", use_container_width=True):
        st.switch_page("pescar.py")
    if desembarcos.button("Desembarcos", use_container_width=True, type=btn_1):
        st.switch_page("pages/desembarcos.py")
    if especies.button("Especies", use_container_width=True, type=btn_2):
        st.switch_page("pages/especies.py")
    if flota.button("Flota", use_container_width=True, type=btn_3):
        st.switch_page("pages/flota.py")


def nav_home_layout():

    gap_l, content, gap_r = st.columns([0.2, 0.6, 0.2])
    st.markdown(
    """<style>
        .element-container button {
            margin-top: 0.5rem;
            height: 4rem;
        }
        .element-container button div p {
            font-size: 1.4rem;
        }
        </style>""",
        unsafe_allow_html=True,
    )


    # content.header("Explorar", anchor=False)
    if content.button("Desembarcos", use_container_width=True):
        st.switch_page("pages/desembarcos.py")
    if content.button("Especies", use_container_width=True):
        st.switch_page("pages/especies.py")
    if content.button("Flota", use_container_width=True):
        st.switch_page("pages/flota.py")