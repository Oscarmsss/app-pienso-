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

# ------------------- PEDIDOS -------------------

if "pedidos" not in st.session_state:
    st.session_state.pedidos = []

st.subheader("Añadir pedido")

tipo = st.selectbox("Tipo", list(TIPOS.keys()))
kg = st.number_input("Kg pedido", min_value=0)

if st.button("Añadir pedido"):
    st.session_state.pedidos.append((tipo, kg))

# ------------------- TOLVAS -------------------

st.subheader("Tolvas")

capacidades = {
    "Tolva 1": 23000,
    "Tolva 2": 23000,
    "Tolva 3": 20000,
    "Tolva 4": 20000,
    "Tolva 5": 20000,
    "Tolva 6": 20000,
    "Tolva 7": 20000,
    "Tolva 8": 20000,
    "Tolva 9": 20000,
    "Tolva 10": 20000
}

stock_tolvas = {}

for tolva, capacidad in capacidades.items():
    stock_tolvas[tolva] = st.number_input(
        f"{tolva} (capacidad {capacidad} kg)",
        min_value=0,
        max_value=capacidad,
        key=tolva
    )

# ------------------- PEDIDOS -------------------

st.subheader("Pedidos")

for i, p in enumerate(st.session_state.pedidos):
    st.write(f"{i+1}. {p[0]} → {p[1]} kg")

if st.button("Borrar pedidos"):
    st.session_state.pedidos = []

# ------------------- CALCULO -------------------

def calcular(pedidos, stock_tolvas):

    agrupado = {}

    for tipo, kg in pedidos:
        agrupado[tipo] = agrupado.get(tipo, 0) + kg

    total_stock = sum(stock_tolvas.values())

    resultado = []

    for tipo, kg in agrupado.items():

        # 🔥 stock total disponible
        kg_necesario = max(0, kg - total_stock)

        porcentaje = TIPOS[tipo]

        kg_base = kg_necesario / (1 + porcentaje) if kg_necesario > 0 else 0
        fichas = ceil(kg_base / 3000) if kg_necesario > 0 else 0

        resultado.append({
            "tipo": tipo,
            "pedido": int(kg),
            "stock_total": int(total_stock),
            "fabricar": int(kg_necesario),
            "fichas": fichas,
            "dosificacion": int(kg_base)
        })

    return resultado

# ------------------- RESULTADO -------------------

if st.button("Generar fabricación"):

    resultado = calcular(st.session_state.pedidos, stock_tolvas)

    st.subheader("Fabricación")

    for r in resultado:

        st.write(
            f"{r['tipo']} → Pedido: {r['pedido']} kg | "
            f"Stock total: {r['stock_total']} kg | "
            f"Fabricar: {r['fabricar']} kg | "
            f"{r['fichas']} fichas | "
            f"{r['dosificacion']} kg dosificación"
        )