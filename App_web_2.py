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

# ------------------- CALCULO -------------------

def calcular(pedidos, stock):

    agrupado = {}

    for tipo, kg in pedidos:
        agrupado[tipo] = agrupado.get(tipo, 0) + kg

    resultado = []

    for tipo, kg in agrupado.items():

        stock_tipo = stock.get(tipo, 0)
        kg_necesario = max(0, kg - stock_tipo)

        porcentaje = TIPOS[tipo]

        kg_base = kg_necesario / (1 + porcentaje) if kg_necesario > 0 else 0
        fichas = ceil(kg_base / 3000) if kg_necesario > 0 else 0

        resultado.append({
            "tipo": tipo,
            "fabricar": int(kg_necesario),
            "fichas": fichas,
            "dosificacion": int(kg_base)
        })

    return resultado

# ------------------- ORDEN SIN CONTAMINACIÓN -------------------

def ordenar(fabricacion):

    orden = []

    for f in fabricacion:

        if orden:
            anterior = orden[-1]["tipo"].lower()
            actual = f["tipo"].lower()

            # 🔥 BLOQUEO CONTAMINACIÓN
            if ("inicio" in anterior or "migas" in anterior) and "fin" in actual:

                orden.append({
                    "tipo": "Fin vegetal (limpieza)",
                    "fabricar": 3000,
                    "fichas": 1,
                    "dosificacion": 2600,
                    "limpieza": True
                })

        # 🔥 REGLA CAMPEROS
        if "campero" in f["tipo"].lower():
            if not orden or "fin vegetal" not in orden[-1]["tipo"].lower():
                orden.append({
                    "tipo": "Fin vegetal (limpieza)",
                    "fabricar": 3000,
                    "fichas": 1,
                    "dosificacion": 2600,
                    "limpieza": True
                })

        f["limpieza"] = False
        orden.append(f)

    return orden

# ------------------- RESULTADO -------------------

if st.button("Generar fabricación"):

    fabricacion = calcular(st.session_state.pedidos, stock_por_tipo)
    fabricacion = ordenar(fabricacion)

    st.subheader("Fabricación optimizada")

    for f in fabricacion:

        if f.get("limpieza"):
            st.warning(
                f"🔧 LIMPIEZA → {f['fichas']} ficha → {f['dosificacion']} kg"
            )
        else:
            st.write(
                f"{f['tipo']} → "
                f"{f['fabricar']} kg | "
                f"{f['fichas']} fichas | "
                f"{f['dosificacion']} kg dosificación"
            )
