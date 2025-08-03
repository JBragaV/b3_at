import streamlit as st

from home import home
from help import help


pg = st.navigation([
    st.Page(home, title="Ações", icon=":material/trending_up:"),
    st.Page(help, title="Indices -- Em Breve", icon="🔥"),
])

pg.run()
