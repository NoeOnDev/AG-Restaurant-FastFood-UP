import pandas as pd
import random
import matplotlib.pyplot as plt

precios_productos_df = pd.read_csv('market analysis/datasets/precios_productos.csv')
encuestas_clientes_df = pd.read_csv('market analysis/datasets/encuestas_clientes.csv')
historial_ventas_df = pd.read_csv('market analysis/datasets/historial_ventas_comida_rapida.csv')

def calcular_preferencias(df, columna):
    total_votos = df[columna].value_counts().sum()
    return (df[columna].value_counts() / total_votos * 100).to_dict()

preferencia_bebidas_dict = calcular_preferencias(encuestas_clientes_df, 'Bebida Favorita')
preferencia_comidas_dict = calcular_preferencias(encuestas_clientes_df, 'Comida Favorita')
preferencia_postres_dict = calcular_preferencias(encuestas_clientes_df, 'Postre Favorito')

def crear_productos_dict(precios_df, *preferencias_dicts):
    productos = {}
    for _, row in precios_df.iterrows():
        producto = row['producto']
        preferencia = sum(pref_dict.get(producto, 0) for pref_dict in preferencias_dicts)
        productos[producto] = {
            "costo": row['costo'],
            "venta": row['venta'],
            "preferencia": preferencia / len(preferencias_dicts)
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

BEBIDAS = ["Pozol", "Coca-Cola", "Tascalate", "Agua de chía", "Agua de horchata", "Agua de jamaica"]
COMIDAS = ["Gordita", "Empanada", "Taco", "Quesadilla", "Tamal", "Tostada"]
POSTRES = ["Nuegado", "Turrón", "Turulete", "Cocada", "Plátano Asado", "Bunuelo"]

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
    venta_individual_total = sum(productos_dict[producto]['venta'] for producto in combo)
    costo_total = sum(productos_dict[producto]['costo'] for producto in combo)
    factor_descuento = calcular_descuento(combo)
    venta_combo = venta_individual_total * factor_descuento
    satisfaccion = sum(productos_dict[producto]['preferencia'] for producto in combo)
    rentabilidad = venta_combo - costo_total
    fitness = (rentabilidad * 0.5) + (satisfaccion * 0.5)
    return fitness, venta_combo, costo_total, venta_individual_total

def transformar_fitness(poblacion):
    min_fitness = min(fitness for _, fitness, _, _, _ in poblacion)
    if min_fitness < 0:
        return [(combo, fitness - min_fitness, venta, costo, venta_individual_total) for combo, fitness, venta, costo, venta_individual_total in poblacion]
    else:
        return poblacion

def seleccionar_padres(poblacion):
    poblacion = transformar_fitness(poblacion)
    fitness_total = sum(fitness for _, fitness, _, _, _ in poblacion)
    seleccionados = []
    for _ in range(2):
        pick = random.uniform(0, fitness_total)
        current = 0
        for combo, fitness, _, _, _ in poblacion:
            current += fitness
            if current > pick:
                seleccionados.append(combo)
                break
    return seleccionados

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

def mutar(combo, probabilidad_mutacion, probabilidad_mutacion_gen):
    if random.random() < probabilidad_mutacion:
        for i in range(len(combo)):
            if random.random() < probabilidad_mutacion_gen:
                if i == 0:
                    combo[i] = random.choice(BEBIDAS)
                elif i == 1:
                    combo[i] = random.choice(COMIDAS)
                elif i == 2:
                    combo[i] = random.choice(POSTRES)
    return combo

def poda(poblacion, tamano_maximo_poblacion):
    poblacion.sort(key=lambda x: x[1], reverse=True)
    mejor_individuo = poblacion[0]
    while len(poblacion) > tamano_maximo_poblacion:
        indice_eliminar = random.randint(1, len(poblacion) - 1)
        poblacion.pop(indice_eliminar)
    if mejor_individuo not in poblacion:
        poblacion.append(mejor_individuo)
    return poblacion

def algoritmo_genetico(tamano_poblacion, num_generaciones, tamano_maximo_poblacion, probabilidad_mutacion, probabilidad_mutacion_gen):
    poblacion = [(crear_combo(), 0, 0, 0, 0) for _ in range(tamano_poblacion)]
    poblacion = [(combo, *calcular_fitness(combo)) for combo, _, _, _, _ in poblacion]
    
    combos_unicos = {tuple(combo) for combo, _, _, _, _ in poblacion}
    
    fitness_max = []
    fitness_avg = []
    fitness_min = []
    generaciones = []

    mejores_individuos = []

    for gen in range(num_generaciones):
        nueva_poblacion = []
        while len(nueva_poblacion) < tamano_poblacion:
            padre1, padre2 = seleccionar_padres(poblacion)
            hijo1, hijo2 = cruce(padre1, padre2)
            hijo1 = mutar(hijo1, probabilidad_mutacion, probabilidad_mutacion_gen)
            hijo2 = mutar(hijo2, probabilidad_mutacion, probabilidad_mutacion_gen)
            
            if tuple(hijo1) not in combos_unicos:
                nueva_poblacion.append((hijo1, *calcular_fitness(hijo1)))
                combos_unicos.add(tuple(hijo1))
            
            if tuple(hijo2) not in combos_unicos:
                nueva_poblacion.append((hijo2, *calcular_fitness(hijo2)))
                combos_unicos.add(tuple(hijo2))
        
        poblacion.extend(nueva_poblacion)
        poblacion = poda(poblacion, tamano_maximo_poblacion)
        
        combos_unicos = {tuple(combo) for combo, _, _, _, _ in poblacion}
        
        fitness_vals = [fitness for _, fitness, _, _, _ in poblacion]
        fitness_max.append(max(fitness_vals))
        fitness_avg.append(sum(fitness_vals) / len(fitness_vals))
        fitness_min.append(min(fitness_vals))

        mejor_combo = max(poblacion, key=lambda x: x[1])
        generaciones.append(mejor_combo)

        print(f"Generación {gen + 1}: Combo = {mejor_combo[0]}, Precio de venta individual total = {mejor_combo[4]}")

        if gen == num_generaciones - 1:
            mejores_individuos = sorted(poblacion, key=lambda x: x[1], reverse=True)[:3]

    mejor_combo = max(poblacion, key=lambda x: x[1])
    return mejor_combo, fitness_max, fitness_avg, fitness_min, generaciones, mejores_individuos

def graficar_resultados(fitness_max, fitness_avg, fitness_min):
    plt.plot(fitness_max, label='Max Fitness')
    plt.plot(fitness_avg, label='Avg Fitness')
    plt.plot(fitness_min, label='Min Fitness')
    plt.xlabel('Generación')
    plt.ylabel('Fitness')
    plt.legend()
    plt.show()
