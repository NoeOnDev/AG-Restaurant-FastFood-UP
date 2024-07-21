import pandas as pd
import random

# Cargar los datos
precios_productos_df = pd.read_csv('market analysis/datasets/precios_productos.csv')
encuestas_clientes_df = pd.read_csv('market analysis/datasets/encuestas_clientes.csv')
historial_ventas_df = pd.read_csv('market analysis/datasets/historial_ventas_comida_rapida.csv')

# Calcular las preferencias de los clientes
def calcular_preferencias(df, columna):
    return (df[columna].value_counts(normalize=True) * 100).to_dict()

preferencia_bebidas_dict = calcular_preferencias(encuestas_clientes_df, 'Bebida Favorita')
preferencia_comidas_dict = calcular_preferencias(encuestas_clientes_df, 'Comida Favorita')
preferencia_postres_dict = calcular_preferencias(encuestas_clientes_df, 'Postre Favorito')

# Crear un diccionario de productos con sus preferencias y precios
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

# Calcular las ventas totales por producto
def calcular_total_ventas(historial_df):
    ventas_por_producto = {}
    for _, row in historial_df.iterrows():
        producto = row['Nombre del Producto']
        precio_total_venta = row['Precio Total de la Venta (MXN)']
        ventas_por_producto[producto] = ventas_por_producto.get(producto, 0) + precio_total_venta
    return ventas_por_producto

total_ventas_por_producto = calcular_total_ventas(historial_ventas_df)

# Convertir los diccionarios en DataFrames para facilitar el acceso a los datos
productos_df = pd.DataFrame.from_dict(productos_dict, orient='index').reset_index().rename(columns={'index': 'nombre'})
historial_df = pd.DataFrame.from_dict(total_ventas_por_producto, orient='index', columns=['ventas'])

# Parámetros del algoritmo genético
TAMANO_POBLACION = 10
TAMANO_MAXIMO_POBLACION = 30
PROBABILIDAD_MUTACION = 0.7
PROBABILIDAD_MUTACION_GEN = 0.01
NUM_GENERACIONES = 50
BEBIDAS = ["Pozol", "Coca-Cola", "Tascalate", "Agua de chía"]
COMIDAS = ["Quesadilla", "Gordita", "Taco", "Empanada"]
POSTRES = ["Nuegado", "Turrón", "Turulete", "Cocada"]

# Crear un combo aleatorio
def crear_combo():
    bebida = random.choice(BEBIDAS)
    comida = random.choice(COMIDAS)
    postre = random.choice(POSTRES)
    return [bebida, comida, postre]

# Calcular el descuento basado en el historial de ventas
def calcular_descuento(combo):
    total_ventas = sum(historial_df.loc[combo]["ventas"])
    promedio_ventas = total_ventas / len(combo)
    max_ventas = historial_df["ventas"].max()
    factor_descuento = 1 - (promedio_ventas / max_ventas) * 0.3
    return factor_descuento

# Calcular el fitness de un combo
def calcular_fitness(combo):
    venta_individual_total = sum(productos_df[productos_df['nombre'].isin(combo)]["venta"])
    costo_total = sum(productos_df[productos_df['nombre'].isin(combo)]["costo"])
    factor_descuento = calcular_descuento(combo)
    venta_combo = venta_individual_total * factor_descuento
    satisfaccion = sum(productos_df[productos_df['nombre'].isin(combo)]["preferencia"])
    rentabilidad = venta_combo - costo_total
    fitness = rentabilidad * 0.5 + satisfaccion * 0.5
    return fitness, venta_combo, costo_total

# Seleccionar padres basados en el fitness
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

# Cruce de dos padres para generar hijos con múltiples puntos de cruza
def cruce(padre1, padre2):
    num_puntos_cruce = random.randint(1, len(padre1) - 1)
    puntos_cruce = sorted(random.sample(range(1, len(padre1)), num_puntos_cruce))
    
    hijo1, hijo2 = [], []
    origen = 0
    for i, punto in enumerate(puntos_cruce):
        if i % 2 == 0:
            hijo1.extend(padre1[origen:punto])
            hijo2.extend(padre2[origen:punto])
        else:
            hijo1.extend(padre2[origen:punto])
            hijo2.extend(padre1[origen:punto])
        origen = punto
    
    if len(puntos_cruce) % 2 == 0:
        hijo1.extend(padre1[origen:])
        hijo2.extend(padre2[origen:])
    else:
        hijo1.extend(padre2[origen:])
        hijo2.extend(padre1[origen:])
        
    return hijo1, hijo2

# Mutar un combo con una probabilidad de mutación global y por gen
def mutar(combo):
    if random.random() < PROBABILIDAD_MUTACION:
        for i in range(len(combo)):
            if random.random() < PROBABILIDAD_MUTACION_GEN:
                if i == 0:
                    combo[i] = random.choice(BEBIDAS)
                elif i == 1:
                    combo[i] = random.choice(COMIDAS)
                elif i == 2:
                    combo[i] = random.choice(POSTRES)
    return combo

# Podar la población para mantener el tamaño máximo
def poda(poblacion, tamano_maximo_poblacion):
    poblacion.sort(key=lambda x: x[1], reverse=True)
    mejor_individuo = poblacion[0]
    while len(poblacion) > tamano_maximo_poblacion:
        indice_eliminar = random.randint(1, len(poblacion) - 1)
        poblacion.pop(indice_eliminar)
    poblacion.append(mejor_individuo)
    return poblacion

# Implementar el algoritmo genético
def algoritmo_genetico(tamano_poblacion, num_generaciones, tamano_maximo_poblacion):
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
        poblacion += nueva_poblacion
        poblacion = poda(poblacion, tamano_maximo_poblacion)

    mejor_combo = max(poblacion, key=lambda x: x[1])
    return mejor_combo

# Ejecutar el algoritmo genético
mejor_combo = algoritmo_genetico(TAMANO_POBLACION, NUM_GENERACIONES, TAMANO_MAXIMO_POBLACION)
print(f"Mejor combo: {mejor_combo[0]}")
print(f"Fitness: {mejor_combo[1]}")
print(f"Precio de venta: {mejor_combo[2]}")
print(f"Precio de producción: {mejor_combo[3]}")
