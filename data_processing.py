import pandas as pd
import random

# Cargar datos
df_ventas = pd.read_csv('market analysis/datasets/historial_ventas_comida_rapida.csv')
df_encuestas = pd.read_csv('market analysis/datasets/encuestas_clientes.csv')
df_popularidad = pd.read_csv('market analysis/datasets/popularidad_preferencias_final.csv')

# Preparar datos
ventas_totales = df_ventas.groupby('Nombre del Producto').sum()['Cantidad']
preferencias_encuestas = df_encuestas.groupby(['Bebida Favorita', 'Comida Favorita', 'Postre Favorito']).size().reset_index(name='Conteo')
popularidad = df_popularidad.set_index('Producto')['Porcentaje de Preferencia']
precios_venta = df_ventas.groupby('Nombre del Producto').first()['Precio de Venta por Unidad (MXN)']
costos_produccion = {'Pozol': 13.60, 'Coca-Cola': 8.50, 'Gordita': 17.00, 'Empanada': 20.40, 'Taco': 12.75, 'Nuegado': 8.50, 'Turrón': 11.90}
rentabilidad = df_ventas.groupby('Nombre del Producto').sum()['Cantidad'] * (precios_venta - pd.Series(costos_produccion))
datos_combinados = pd.DataFrame({'Popularidad': popularidad, 'Rentabilidad': rentabilidad})

# Funciones auxiliares
def calcular_rentabilidad(combo, rentabilidades):
    return sum(rentabilidades[producto] for producto in combo)

def calcular_popularidad(combo, popularidades):
    return sum(popularidades[producto] for producto in combo) / len(combo)

def calcular_costo_produccion(combo, costos_produccion):
    return sum(costos_produccion[producto] for producto in combo)

def calcular_precio_venta(combo, precios_venta):
    return sum(precios_venta[producto] for producto in combo)

def funcion_aptitud(combo, rentabilidades, popularidades, costos_produccion, precios_venta):
    try:
        rentabilidad = calcular_rentabilidad(combo, rentabilidades)
        popularidad = calcular_popularidad(combo, popularidades)
        costo_produccion = calcular_costo_produccion(combo, costos_produccion)
        precio_venta_individual = calcular_precio_venta(combo, precios_venta)
        precio_venta_combo = max(costo_produccion * 1.2, precio_venta_individual * 0.8)
        aptitud = rentabilidad * popularidad / precio_venta_combo

        print(f"Combo: {combo}")
        print(f"Rentabilidad: {rentabilidad}")
        print(f"Popularidad: {popularidad}")
        print(f"Costo Producción: {costo_produccion}")
        print(f"Precio Venta Individual: {precio_venta_individual}")
        print(f"Precio Venta Combo: {precio_venta_combo}")
        print(f"Aptitud: {aptitud}")
        return aptitud, precio_venta_combo, costo_produccion
    except KeyError as e:
        print(f"Error: {e}. Combo: {combo}")
        return 0, 0, 0

# Inicialización
def crear_poblacion_inicial(tamano_poblacion, productos, tamano_combo):
    return [random.sample(productos, tamano_combo) for _ in range(tamano_poblacion)]

# Selección
def seleccion(poblacion, rentabilidades, popularidades, costos_produccion, precios_venta):
    puntuaciones = [(funcion_aptitud(combo, rentabilidades, popularidades, costos_produccion, precios_venta), combo) for combo in poblacion]
    puntuaciones = [p for p in puntuaciones if p[0][0] > 0]  # Filtrar puntuaciones no válidas
    if not puntuaciones:
        print("No se encontraron combinaciones válidas en la población inicial. Verifique los datos y condiciones de aptitud.")
        raise ValueError("No se encontraron combinaciones válidas en la población.")
    puntuaciones.sort(reverse=True, key=lambda x: x[0][0])
    seleccionados = [combo for _, combo in puntuaciones[:len(poblacion)//2]]
    return seleccionados, puntuaciones[0]

# Cruza
def cruzar(padre1, padre2):
    punto_cruce = random.randint(1, len(padre1) - 2)
    hijo = padre1[:punto_cruce] + padre2[punto_cruce:]
    return hijo

# Mutación
def mutar(combo, productos, prob_mut_indiv, prob_mut_gen):
    if random.random() < prob_mut_indiv:
        combo = [gen if random.random() >= prob_mut_gen else random.choice(productos) for gen in combo]
    return combo

# Poda
def podar(poblacion, max_poblacion):
    nueva_poblacion = []
    [nueva_poblacion.append(indiv) for indiv in poblacion if indiv not in nueva_poblacion]
    while len(nueva_poblacion) > max_poblacion:
        nueva_poblacion.remove(random.choice(nueva_poblacion[1:]))
    return nueva_poblacion

# Evolución
def evolucionar_poblacion(poblacion, rentabilidades, popularidades, costos_produccion, precios_venta, generaciones, tamano_poblacion, max_poblacion, prob_mut_indiv, prob_mut_gen):
    estadisticas = []
    for _ in range(generaciones):
        seleccionados, mejor_individuo = seleccion(poblacion, rentabilidades, popularidades, costos_produccion, precios_venta)
        nueva_poblacion = seleccionados[:]
        while len(nueva_poblacion) < tamano_poblacion:
            if len(seleccionados) < 2:
                break
            padre1, padre2 = random.sample(seleccionados, 2)
            hijo = cruzar(padre1, padre2)
            hijo = mutar(hijo, productos, prob_mut_indiv, prob_mut_gen)
            nueva_poblacion.append(hijo)
        poblacion = podar(nueva_poblacion, max_poblacion)
        estadisticas.append(mejor_individuo)
    return mejor_individuo, estadisticas

# Parámetros del algoritmo
tamano_poblacion = 50
tamano_combo = 3
generaciones = 100
max_poblacion = 100
prob_mut_indiv = 0.1
prob_mut_gen = 0.1

# Crear la población inicial
productos = datos_combinados.index.tolist()
poblacion_inicial = crear_poblacion_inicial(tamano_poblacion, productos, tamano_combo)

# Evolucionar la población
try:
    mejor_combo, estadisticas = evolucionar_poblacion(
        poblacion_inicial,
        datos_combinados['Rentabilidad'],
        datos_combinados['Popularidad'],
        costos_produccion,
        precios_venta,
        generaciones,
        tamano_poblacion,
        max_poblacion,
        prob_mut_indiv,
        prob_mut_gen
    )

    # Resultados
    print("Mejor Combo:", mejor_combo[1])
    print("Aptitud del Mejor Combo:", mejor_combo[0][0])
    print("Precio de Venta del Combo:", mejor_combo[0][1])
    print("Costo de Producción del Combo:", mejor_combo[0][2])
except ValueError as e:
    print(e)
