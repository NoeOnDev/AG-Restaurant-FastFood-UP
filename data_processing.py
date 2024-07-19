import pandas as pd

df_ventas = pd.read_csv('market analysis/datasets/historial_ventas_comida_rapida.csv')
df_encuestas = pd.read_csv('market analysis/datasets/encuestas_clientes.csv')
df_popularidad = pd.read_csv('market analysis/datasets/popularidad_preferencias_final.csv')

ventas_totales = df_ventas.groupby('Nombre del Producto').sum()['Cantidad']
print("Ventas Totales por Producto:")
print(ventas_totales)

preferencias_encuestas = df_encuestas.groupby(['Bebida Favorita', 'Comida Favorita', 'Postre Favorito']).size().reset_index(name='Conteo')
print("Preferencias de Encuestas:")
print(preferencias_encuestas)

popularidad = df_popularidad.set_index('Producto')['Porcentaje de Preferencia']
print("Popularidad por Producto:")
print(popularidad)

precios_venta = df_ventas.groupby('Nombre del Producto').first()['Precio de Venta por Unidad (MXN)']
costos_produccion = {
    'Pozol': 13.60, 'Coca-Cola': 8.50, 'Gordita': 17.00,
    'Empanada': 20.40, 'Taco': 12.75, 'Nuegado': 8.50, 'Turrón': 11.90
}
rentabilidad = df_ventas.groupby('Nombre del Producto').sum()['Cantidad'] * (precios_venta - pd.Series(costos_produccion))
print("Rentabilidad por Producto:")
print(rentabilidad)

datos_combinados = pd.DataFrame({
    'Popularidad': popularidad,
    'Rentabilidad': rentabilidad
})
print("Datos Combinados para el Algoritmo Genético:")
print(datos_combinados)

def calcular_rentabilidad(combo, rentabilidades):
    return sum(rentabilidades[producto] for producto in combo)

def calcular_popularidad(combo, popularidades):
    return sum(popularidades[producto] for producto in combo) / len(combo)

def calcular_costo_produccion(combo, costos_produccion):
    return sum(costos_produccion[producto] for producto in combo)

def calcular_precio_venta(combo, precios_venta):
    return sum(precios_venta[producto] for producto in combo)

def funcion_aptitud(combo, rentabilidades, popularidades, costos_produccion, precios_venta):
    rentabilidad = calcular_rentabilidad(combo, rentabilidades)
    popularidad = calcular_popularidad(combo, popularidades)
    costo_produccion = calcular_costo_produccion(combo, costos_produccion)
    precio_venta_individual = calcular_precio_venta(combo, precios_venta)
    
    precio_venta_combo = max(costo_produccion * 1.2, precio_venta_individual * 0.8)

    aptitud = rentabilidad * popularidad / precio_venta_combo
    return aptitud, precio_venta_combo, costo_produccion
