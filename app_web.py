import streamlit as st
from math import ceil

st.title("Planificador de Fabricación")

TIPOS = {
    "Inicio": 0.05,
    "Inicio campero": 0.05,
    "Migas vegetales": 0.10,
    "Migas blanco": 0.10,
    "Crecimiento campero": 0.10,
    "Crecimiento blanco": 0.10,
    "Crecimiento vegetal": 0.10,
    "Fin campero": 0.15,
    "Fin blanco": 0.15,
    "Fin vegetal": 0.15
}

if "pedidos" not in st.session_state:
    st.session_state.pedidos = []

st.subheader("Añadir pedido")

tipo = st.selectbox("Tipo", list(TIPOS.keys()))
kg = st.number_input("Kg pedido (final)", min_value=0)

if st.button("Añadir"):
    st.session_state.pedidos.append((tipo, kg))

st.subheader("Pedidos")

for i, p in enumerate(st.session_state.pedidos):
    st.write(f"{i+1}. {p[0]} → {p[1]} kg")

if st.button("Borrar todo"):
    st.session_state.pedidos = []

if st.button("Generar fabricación"):

    agrupado = {}

    for tipo, kg in st.session_state.pedidos:
        agrupado[tipo] = agrupado.get(tipo, 0) + kg

    st.subheader("Fabricación")

    for tipo, kg in agrupado.items():
        porcentaje = TIPOS[tipo]

        kg_base = kg / (1 + porcentaje)
        fichas = ceil(kg_base / 3000)

        st.write(
            f"{fichas} fichas de {tipo} → {int(kg)} kg final → {int(kg_base)} kg dosificación"
        )