import pandas as pd
import random

precios_productos_df = pd.read_csv('market analysis/datasets/precios_productos.csv')
encuestas_clientes_df = pd.read_csv('market analysis/datasets/encuestas_clientes.csv')
historial_ventas_df = pd.read_csv('market analysis/datasets/historial_ventas_comida_rapida.csv')

preferencia_bebidas = encuestas_clientes_df['Bebida Favorita'].value_counts(normalize=True) * 100
preferencia_comidas = encuestas_clientes_df['Comida Favorita'].value_counts(normalize=True) * 100
preferencia_postres = encuestas_clientes_df['Postre Favorito'].value_counts(normalize=True) * 100

preferencia_bebidas_dict = (preferencia_bebidas / 100).to_dict()
preferencia_comidas_dict = (preferencia_comidas / 100).to_dict()
preferencia_postres_dict = (preferencia_postres / 100).to_dict()

productos_dict = {}

for index, row in precios_productos_df.iterrows():
    producto = row['producto']
    costo = row['costo']
    venta = row['venta']
    
    preferencia = preferencia_bebidas_dict.get(producto, 
                    preferencia_comidas_dict.get(producto, 
                    preferencia_postres_dict.get(producto, 0)))
    
    productos_dict[producto] = {"costo": costo, "venta": venta, "preferencia": preferencia}

total_ventas_por_producto = {}

for index, row in historial_ventas_df.iterrows():
    producto = row['Nombre del Producto']
    precio_total_venta = row['Precio Total de la Venta (MXN)']
    
    if producto in total_ventas_por_producto:
        total_ventas_por_producto[producto] += precio_total_venta
    else:
        total_ventas_por_producto[producto] = precio_total_venta

productos_df = pd.DataFrame.from_dict(productos_dict, orient='index')
productos_df.reset_index(inplace=True)
productos_df.rename(columns={'index': 'nombre'}, inplace=True)

historial_df = pd.DataFrame.from_dict(total_ventas_por_producto, orient='index', columns=['ventas'])

tamano_poblacion = 10
probabilidad_mutacion = 0.7
num_generaciones = 200

def crear_combo():
    bebida = random.choice(productos_df[productos_df['nombre'].isin(["Pozol", "Coca-Cola"])]["nombre"].tolist())
    comida = random.choice(productos_df[productos_df['nombre'].isin(["Quesadilla", "Gordita", "Taco", "Empanada"])]["nombre"].tolist())
    postre = random.choice(productos_df[productos_df['nombre'].isin(["Turrón", "Nuegado"])]["nombre"].tolist())
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
    fitness_total = sum(fitness for combo, fitness, _, _ in poblacion)
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
    if random.random() < probabilidad_mutacion:
        indice = random.randint(0, len(combo) - 1)
        if indice == 0:
            combo[indice] = random.choice(["Pozol", "Coca-Cola"])
        elif indice == 1:
            combo[indice] = random.choice(["Quesadilla", "Gordita", "Taco", "Empanada"])
        elif indice == 2:
            combo[indice] = random.choice(["Turrón", "Nuegado"])
    return combo

poblacion = [(crear_combo(), 0, 0, 0) for _ in range(tamano_poblacion)]

poblacion = [(combo, *calcular_fitness(combo)) for combo, _, _, _ in poblacion]

for generacion in range(num_generaciones):
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
print(f"Mejor combo: {mejor_combo[0]}")
print(f"Fitness: {mejor_combo[1]}")
print(f"Precio de venta: {mejor_combo[2]}")
print(f"Precio de producción: {mejor_combo[3]}")