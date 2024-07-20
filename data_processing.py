import pandas as pd
import random


probabilidad_mutacion = 0.1
tamano_poblacion = 10
num_generaciones = 100

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

def crear_combo():
    bebida = random.choice(productos_df[productos_df['nombre'].isin(["Pozol", "Coca-Cola"])]["nombre"].tolist())
    comida = random.choice(productos_df[productos_df['nombre'].isin(["Quesadilla", "Gordita", "Taco", "Empanada"])]["nombre"].tolist())
    postre = random.choice(productos_df[productos_df['nombre'].isin(["Turrón", "Nuegado"])]["nombre"].tolist())
    return [bebida, comida, postre]

def calcular_fitness(combo):
    rentabilidad = sum(productos_df[productos_df['nombre'].isin(combo)]["venta"]) - sum(productos_df[productos_df['nombre'].isin(combo)]["costo"])
    satisfaccion = sum(productos_df[productos_df['nombre'].isin(combo)]["preferencia"])
    print(f"Combo: {combo}, Rentabilidad: {rentabilidad}, Satisfacción: {satisfaccion}")
    return rentabilidad * 0.6 + satisfaccion * 0.4

def seleccionar_padres(poblacion):
    fitness_total = sum(fitness for combo, fitness in poblacion)
    seleccionados = []
    for _ in range(2):
        pick = random.uniform(0, fitness_total)
        current = 0
        for combo, fitness in poblacion:
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

poblacion = [(crear_combo(), 0) for _ in range(tamano_poblacion)]

poblacion = [(combo, calcular_fitness(combo)) for combo, _ in poblacion]

for generacion in range(num_generaciones):
    nueva_poblacion = []
    for _ in range(tamano_poblacion // 2):
        padre1, padre2 = seleccionar_padres(poblacion)
        hijo1, hijo2 = cruce(padre1, padre2)
        hijo1 = mutar(hijo1)
        hijo2 = mutar(hijo2)
        nueva_poblacion.append((hijo1, calcular_fitness(hijo1)))
        nueva_poblacion.append((hijo2, calcular_fitness(hijo2)))
    poblacion = nueva_poblacion

mejor_combo = max(poblacion, key=lambda x: x[1])
print(f"Mejor combo: {mejor_combo[0]}, Fitness: {mejor_combo[1]}")
