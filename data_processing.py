import pandas as pd
import random

precios_productos_df = pd.read_csv('market analysis/datasets/precios_productos.csv')
encuestas_clientes_df = pd.read_csv('market analysis/datasets/encuestas_clientes.csv')
historial_ventas_df = pd.read_csv('market analysis/datasets/historial_ventas_comida_rapida.csv')

def calcular_preferencias(df, columna):
    return (df[columna].value_counts(normalize=True) * 100).to_dict()

preferencia_bebidas_dict = calcular_preferencias(encuestas_clientes_df, 'Bebida Favorita')
preferencia_comidas_dict = calcular_preferencias(encuestas_clientes_df, 'Comida Favorita')
preferencia_postres_dict = calcular_preferencias(encuestas_clientes_df, 'Postre Favorito')

def crear_productos_dict(precios_df, *preferencias_dicts):
    productos = {}
    for _, row in precios_df.iterrows():
        producto = row['producto']
        preferencia = 0
        for pref_dict in preferencias_dicts:
            preferencia = pref_dict.get(producto, preferencia)
        productos[producto] = {
            "costo": row['costo'],
            "venta": row['venta'],
            "preferencia": preferencia / 100
        }
    return productos

productos_dict = crear_productos_dict(precios_productos_df, preferencia_bebidas_dict, preferencia_comidas_dict, preferencia_postres_dict)

def calcular_total_ventas(historial_df):
    ventas_por_producto = {}
    for _, row in historial_df.iterrows():
        producto = row['Nombre del Producto']
        precio_total_venta = row['Precio Total de la Venta (MXN)']
        ventas_por_producto[producto] = ventas_por_producto.get(producto, 0) + precio_total_venta
    return ventas_por_producto

total_ventas_por_producto = calcular_total_ventas(historial_ventas_df)

productos_df = pd.DataFrame.from_dict(productos_dict, orient='index').reset_index().rename(columns={'index': 'nombre'})
historial_df = pd.DataFrame.from_dict(total_ventas_por_producto, orient='index', columns=['ventas'])

TAMANO_POBLACION = 10
PROBABILIDAD_MUTACION = 0.7
NUM_GENERACIONES = 200
BEBIDAS = ["Pozol", "Coca-Cola"]
COMIDAS = ["Quesadilla", "Gordita", "Taco", "Empanada"]
POSTRES = ["Turrón", "Nuegado"]

def crear_combo():
    bebida = random.choice(BEBIDAS)
    comida = random.choice(COMIDAS)
    postre = random.choice(POSTRES)
    return [bebida, comida, postre]

def calcular_descuento(combo):
    total_ventas = sum(historial_df.loc[combo]["ventas"])
    promedio_ventas = total_ventas / len(combo)
    max_ventas = historial_df["ventas"].max()
    factor_descuento = 1 - (promedio_ventas / max_ventas) * 0.3
    return factor_descuento

def calcular_fitness(combo):
    venta_individual_total = sum(productos_df[productos_df['nombre'].isin(combo)]["venta"])
    costo_total = sum(productos_df[productos_df['nombre'].isin(combo)]["costo"])
    factor_descuento = calcular_descuento(combo)
    venta_combo = venta_individual_total * factor_descuento
    satisfaccion = sum(productos_df[productos_df['nombre'].isin(combo)]["preferencia"])
    rentabilidad = venta_combo - costo_total
    fitness = rentabilidad * 0.6 + satisfaccion * 0.4
    return fitness, venta_combo, costo_total

def seleccionar_padres(poblacion):
    fitness_total = sum(fitness for _, fitness, _, _ in poblacion)
    seleccionados = []
    for _ in range(2):
        pick = random.uniform(0, fitness_total)
        current = 0
        for combo, fitness, _, _ in poblacion:
            current += fitness
            if current > pick:
                seleccionados.append(combo)
                break
    return seleccionados

def cruce(padre1, padre2):
    punto_cruce = random.randint(1, len(padre1) - 1)
    hijo1 = padre1[:punto_cruce] + padre2[punto_cruce:]
    hijo2 = padre2[:punto_cruce] + padre1[punto_cruce:]
    return hijo1, hijo2

def mutar(combo):
    if random.random() < PROBABILIDAD_MUTACION:
        indice = random.randint(0, len(combo) - 1)
        if indice == 0:
            combo[indice] = random.choice(BEBIDAS)
        elif indice == 1:
            combo[indice] = random.choice(COMIDAS)
        elif indice == 2:
            combo[indice] = random.choice(POSTRES)
    return combo

# Algoritmo genético
def algoritmo_genetico(tamano_poblacion, num_generaciones):
    poblacion = [(crear_combo(), 0, 0, 0) for _ in range(tamano_poblacion)]
    poblacion = [(combo, *calcular_fitness(combo)) for combo, _, _, _ in poblacion]

    for _ in range(num_generaciones):
        nueva_poblacion = []
        for _ in range(tamano_poblacion // 2):
            padre1, padre2 = seleccionar_padres(poblacion)
            hijo1, hijo2 = cruce(padre1, padre2)
            hijo1 = mutar(hijo1)
            hijo2 = mutar(hijo2)
            nueva_poblacion.append((hijo1, *calcular_fitness(hijo1)))
            nueva_poblacion.append((hijo2, *calcular_fitness(hijo2)))
        poblacion = nueva_poblacion

    mejor_combo = max(poblacion, key=lambda x: x[1])
    return mejor_combo

# Ejecutar el algoritmo
mejor_combo = algoritmo_genetico(TAMANO_POBLACION, NUM_GENERACIONES)
print(f"Mejor combo: {mejor_combo[0]}")
print(f"Fitness: {mejor_combo[1]}")
print(f"Precio de venta: {mejor_combo[2]}")
print(f"Precio de producción: {mejor_combo[3]}")
