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

st.subheader("Tolvas (stock real)")

tolvas = {}

for i in range(1, 11):
    st.markdown(f"**Tolva {i}**")

    tipo_tolva = st.selectbox(
        f"Tipo Tolva {i}",
        ["Vacía"] + list(TIPOS.keys()),
        key=f"tipo_{i}"
    )

    capacidad = 23000 if i in [1, 2] else 20000

    kg_tolva = st.number_input(
        f"Kg en Tolva {i} (max {capacidad})",
        min_value=0,
        max_value=capacidad,
        key=f"kg_{i}"
    )

    if tipo_tolva != "Vacía":
        tolvas.setdefault(tipo_tolva, 0)
        tolvas[tipo_tolva] += kg_tolva

# ------------------- PEDIDOS -------------------

st.subheader("Pedidos")

for i, p in enumerate(st.session_state.pedidos):
    st.write(f"{i+1}. {p[0]} → {p[1]} kg")

if st.button("Borrar pedidos"):
    st.session_state.pedidos = []

# ------------------- CALCULO -------------------

def calcular(pedidos, tolvas):

    agrupado = {}

    for tipo, kg in pedidos:
        agrupado[tipo] = agrupado.get(tipo, 0) + kg

    resultado = []

    for tipo, kg in agrupado.items():

        stock = tolvas.get(tipo, 0)
        kg_necesario = max(0, kg - stock)

        porcentaje = TIPOS[tipo]

        kg_base = kg_necesario / (1 + porcentaje) if kg_necesario > 0 else 0
        fichas = ceil(kg_base / 3000) if kg_necesario > 0 else 0

        resultado.append({
            "tipo": tipo,
            "pedido": int(kg),
            "stock": int(stock),
            "fabricar": int(kg_necesario),
            "fichas": fichas,
            "dosificacion": int(kg_base)
        })

    return resultado

# ------------------- ORDEN INTELIGENTE -------------------

def ordenar(fabricacion):

    orden = []

    inicios = []
    migas = []
    crecimientos = []
    fines = []
    camperos = []

    for f in fabricacion:
        t = f["tipo"].lower()

        if "inicio" in t:
            inicios.append(f)
        elif "migas" in t:
            migas.append(f)
        elif "crecimiento" in t:
            crecimientos.append(f)
        elif "fin" in t:
            fines.append(f)
        elif "campero" in t:
            camperos.append(f)

    orden.extend(inicios)
    orden.extend(migas)
    orden.extend(crecimientos)
    orden.extend(fines)

    # 🔥 Regla camperos
    for c in camperos:
        if not any("fin vegetal" in f["tipo"].lower() for f in orden):
            orden.append({
                "tipo": "Fin vegetal (limpieza)",
                "pedido": 0,
                "stock": 0,
                "fabricar": 3000,
                "fichas": 1,
                "dosificacion": 2600
            })

        orden.append(c)

    return orden

# ------------------- VALIDACION -------------------

def validar(orden):

    avisos = []

    for i in range(len(orden)-1):
        actual = orden[i]["tipo"]
        siguiente = orden[i+1]["tipo"]

        if ("inicio" in actual.lower() or "migas" in actual.lower()) and "fin" in siguiente.lower():
            avisos.append(f"⚠️ No permitido: {actual} → {siguiente}")

    return avisos

# ------------------- RESULTADO -------------------

if st.button("Generar fabricación"):

    fabricacion = calcular(st.session_state.pedidos, tolvas)
    fabricacion = ordenar(fabricacion)
    avisos = validar(fabricacion)

    st.subheader("Fabricación optimizada")

    for f in fabricacion:
        st.write(
            f"{f['tipo']} → Pedido: {f['pedido']} | "
            f"Stock: {f['stock']} | "
            f"Fabricar: {f['fabricar']} | "
            f"{f['fichas']} fichas | "
            f"{f['dosificacion']} kg dosificación"
        )

    if avisos:
        st.subheader("Avisos")
        for a in avisos:
            st.warning(a)
