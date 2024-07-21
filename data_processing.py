import pandas as pd
import random

# Parámetros del algoritmo genético
probabilidad_mutacion = 0.1
tamano_poblacion = 50
num_generaciones = 200

# Diccionario de productos
productos_dict = {
    "Pozol": {"costo": 7, "venta": 15, "preferencia": 0.56},
    "Coca-Cola": {"costo": 18, "venta": 25, "preferencia": 0.44},
    "Quesadilla": {"costo": 12, "venta": 22, "preferencia": 0.3},
    "Gordita": {"costo": 10, "venta": 18, "preferencia": 0.3},
    "Taco": {"costo": 9, "venta": 14, "preferencia": 0.16},
    "Empanada": {"costo": 8, "venta": 15, "preferencia": 0.24},
    "Turrón": {"costo": 4, "venta": 10, "preferencia": 0.48},
    "Nuegado": {"costo": 5, "venta": 12, "preferencia": 0.52}
}
productos_df = pd.DataFrame.from_dict(productos_dict, orient='index')
productos_df.reset_index(inplace=True)
productos_df.rename(columns={'index': 'nombre'}, inplace=True)

# Simulación de historial de ventas (puedes reemplazar esto con datos reales)
historial_ventas = {
    "Pozol": 150,
    "Coca-Cola": 200,
    "Quesadilla": 100,
    "Gordita": 100,
    "Taco": 80,
    "Empanada": 90,
    "Turrón": 110,
    "Nuegado": 130
}
historial_df = pd.DataFrame.from_dict(historial_ventas, orient='index', columns=['ventas'])

# Crear un combo aleatorio
def crear_combo():
    bebida = random.choice(productos_df[productos_df['nombre'].isin(["Pozol", "Coca-Cola"])]["nombre"].tolist())
    comida = random.choice(productos_df[productos_df['nombre'].isin(["Quesadilla", "Gordita", "Taco", "Empanada"])]["nombre"].tolist())
    postre = random.choice(productos_df[productos_df['nombre'].isin(["Turrón", "Nuegado"])]["nombre"].tolist())
    return [bebida, comida, postre]

# Calcular el descuento dinámico basado en el historial de ventas
def calcular_descuento(combo):
    total_ventas = sum(historial_df.loc[combo]["ventas"])
    promedio_ventas = total_ventas / len(combo)
    max_ventas = historial_df["ventas"].max()
    factor_descuento = 1 - (promedio_ventas / max_ventas) * 0.3  # El descuento varía hasta un 30% según las ventas
    return factor_descuento

# Calcular el fitness de un combo
def calcular_fitness(combo):
    venta_individual_total = sum(productos_df[productos_df['nombre'].isin(combo)]["venta"])
    costo_total = sum(productos_df[productos_df['nombre'].isin(combo)]["costo"])
    factor_descuento = calcular_descuento(combo)
    venta_combo = venta_individual_total * factor_descuento
    satisfaccion = sum(productos_df[productos_df['nombre'].isin(combo)]["preferencia"])
    rentabilidad = venta_combo - costo_total
    fitness = rentabilidad * 0.6 + satisfaccion * 0.4
    return fitness, venta_combo, costo_total

# Seleccionar padres usando el método de ruleta
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

# Aplicar cruce para generar nuevos hijos
def cruce(padre1, padre2):
    punto_cruce = random.randint(1, len(padre1) - 1)
    hijo1 = padre1[:punto_cruce] + padre2[punto_cruce:]
    hijo2 = padre2[:punto_cruce] + padre1[punto_cruce:]
    return hijo1, hijo2

# Aplicar mutación a un combo
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

# Inicializar población
poblacion = [(crear_combo(), 0, 0, 0) for _ in range(tamano_poblacion)]

# Evaluar población inicial
poblacion = [(combo, *calcular_fitness(combo)) for combo, _, _, _ in poblacion]

# Iterar a través de las generaciones
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

# Encontrar el mejor combo
mejor_combo = max(poblacion, key=lambda x: x[1])
print(f"Mejor combo: {mejor_combo[0]}")
print(f"Fitness: {mejor_combo[1]}")
print(f"Precio de venta: {mejor_combo[2]}")
print(f"Precio de producción: {mejor_combo[3]}")
