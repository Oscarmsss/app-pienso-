import streamlit as st
from math import ceil

st.title("Planificador de Fabricación Inteligente")

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

st.subheader("Tolvas (stock real)")

stock_por_tipo = {}

for i in range(1, 11):

    col1, col2 = st.columns(2)

    with col1:
        tipo_tolva = st.selectbox(
            f"Tolva {i} - Tipo",
            ["Vacía"] + list(TIPOS.keys()),
            key=f"tipo_{i}"
        )

    capacidad = 23000 if i in [1, 2] else 20000

    with col2:
        kg_tolva = st.number_input(
            f"Tolva {i} - Kg (max {capacidad})",
            min_value=0,
            max_value=capacidad,
            key=f"kg_{i}"
        )

    if tipo_tolva != "Vacía":
        stock_por_tipo[tipo_tolva] = stock_por_tipo.get(tipo_tolva, 0) + kg_tolva

# ------------------- MOSTRAR PEDIDOS -------------------

st.subheader("Pedidos")

for i, p in enumerate(st.session_state.pedidos):
    st.write(f"{i+1}. {p[0]} → {p[1]} kg")

if st.button("Borrar pedidos"):
    st.session_state.pedidos = []

# ------------------- OPTIMIZACIÓN REAL -------------------

def generar_bloques(pedidos, stock):

    bloques = []

    for tipo, kg in pedidos:

        stock_tipo = stock.get(tipo, 0)
        kg_necesario = max(0, kg - stock_tipo)

        if kg_necesario == 0:
            continue

        porcentaje = TIPOS[tipo]
        kg_base = kg_necesario / (1 + porcentaje)

        fichas = ceil(kg_base / 3000)

        for _ in range(fichas):
            bloques.append(tipo)

    return bloques


def es_compatible(anterior, siguiente):

    if anterior is None:
        return True

    anterior = anterior.lower()
    siguiente = siguiente.lower()

    # 🔥 regla contaminación
    if ("inicio" in anterior or "migas" in anterior) and "fin" in siguiente:
        return False

    return True


def optimizar(bloques):

    resultado = []
    ultimo = None

    while bloques:

        colocado = False

        for i, tipo in enumerate(bloques):

            if es_compatible(ultimo, tipo):
                resultado.append(tipo)
                ultimo = tipo
                bloques.pop(i)
                colocado = True
                break

        # 🔥 si no hay compatible, forzar el menos malo
        if not colocado:
            tipo = bloques.pop(0)
            resultado.append(tipo)
            ultimo = tipo

    return resultado

# ------------------- RESULTADO -------------------

if st.button("Generar fabricación"):

    bloques = generar_bloques(st.session_state.pedidos, stock_por_tipo)
    orden = optimizar(bloques)

    st.subheader("Fabricación optimizada")

    conteo = {}

    for tipo in orden:
        conteo[tipo] = conteo.get(tipo, 0) + 1

    for tipo, fichas in conteo.items():

        porcentaje = TIPOS[tipo]
        kg_base = fichas * 3000
        kg_final = int(kg_base * (1 + porcentaje))

        st.write(
            f"{tipo} → {fichas} fichas | "
            f"{kg_final} kg final | "
            f"{kg_base} kg dosificación"
        )

    st.subheader("Orden de fabricación")

    for i, tipo in enumerate(orden):
        st.write(f"{i+1}. {tipo}")
