import tkinter as tk
from tkinter import ttk
from math import ceil

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

pedidos = []
fabricacion = []

# ------------------- PEDIDOS -------------------

def añadir():
    try:
        tipo = combo.get()
        kg = float(entry.get())

        pedidos.append((tipo, kg))
        actualizar_pedidos()

        entry.delete(0, tk.END)
    except:
        pass

def actualizar_pedidos():
    lista_pedidos.delete(0, tk.END)
    for i, p in enumerate(pedidos):
        lista_pedidos.insert(tk.END, f"{i+1}. {p[0]} → {int(p[1])} kg")

def subir_pedido():
    i = lista_pedidos.curselection()
    if i:
        i = i[0]
        if i > 0:
            pedidos[i], pedidos[i-1] = pedidos[i-1], pedidos[i]
            actualizar_pedidos()
            lista_pedidos.select_set(i-1)

def bajar_pedido():
    i = lista_pedidos.curselection()
    if i:
        i = i[0]
        if i < len(pedidos)-1:
            pedidos[i], pedidos[i+1] = pedidos[i+1], pedidos[i]
            actualizar_pedidos()
            lista_pedidos.select_set(i+1)

def borrar_pedido():
    i = lista_pedidos.curselection()
    if i:
        pedidos.pop(i[0])
        actualizar_pedidos()

# ------------------- CALCULO -------------------

def calcular():
    global fabricacion
    agrupado = {}

    # Agrupar pedidos
    for tipo, kg in pedidos:
        if tipo not in agrupado:
            agrupado[tipo] = 0
        agrupado[tipo] += kg

    fabricacion = []

    for tipo, kg in agrupado.items():
        porcentaje = TIPOS[tipo]

        # 🔥 cálculo correcto
        kg_base = kg / (1 + porcentaje)
        fichas = ceil(kg_base / 3000)

        kg_final = int(kg)  # no se pasa del pedido
        kg_dosificacion = int(kg_base)

        fabricacion.append((tipo, fichas, kg_final, kg_dosificacion))

    actualizar_fabricacion()

def actualizar_fabricacion():
    resultado.delete(0, tk.END)
    for i, r in enumerate(fabricacion):
        texto = (
            f"{i+1}. {r[1]} fichas de {r[0]} → "
            f"{r[2]} kg final → {r[3]} kg dosificación"
        )
        resultado.insert(tk.END, texto)

# ------------------- FABRICACION -------------------

def subir_fab():
    i = resultado.curselection()
    if i:
        i = i[0]
        if i > 0:
            fabricacion[i], fabricacion[i-1] = fabricacion[i-1], fabricacion[i]
            actualizar_fabricacion()
            resultado.select_set(i-1)

def bajar_fab():
    i = resultado.curselection()
    if i:
        i = i[0]
        if i < len(fabricacion)-1:
            fabricacion[i], fabricacion[i+1] = fabricacion[i+1], fabricacion[i]
            actualizar_fabricacion()
            resultado.select_set(i+1)

def borrar_fab():
    i = resultado.curselection()
    if i:
        fabricacion.pop(i[0])
        actualizar_fabricacion()

# ------------------- VENTANA -------------------

root = tk.Tk()
root.title("Planificador de Fabricación")

# Entrada
combo = ttk.Combobox(root, values=list(TIPOS.keys()), width=30)
combo.pack(pady=5)

entry = tk.Entry(root)
entry.pack(pady=5)

tk.Button(root, text="Añadir pedido", command=añadir).pack(pady=5)

# Lista pedidos
lista_pedidos = tk.Listbox(root, width=60)
lista_pedidos.pack(pady=5)

tk.Button(root, text="🔼 Subir pedido", command=subir_pedido).pack()
tk.Button(root, text="🔽 Bajar pedido", command=bajar_pedido).pack()
tk.Button(root, text="❌ Borrar pedido", command=borrar_pedido).pack()

# Calcular
tk.Button(root, text="Generar fabricación", command=calcular).pack(pady=10)

# Resultado
resultado = tk.Listbox(root, width=80)
resultado.pack(pady=5)

tk.Button(root, text="🔼 Subir fabricación", command=subir_fab).pack()
tk.Button(root, text="🔽 Bajar fabricación", command=bajar_fab).pack()
tk.Button(root, text="❌ Borrar fabricación", command=borrar_fab).pack()

root.mainloop()