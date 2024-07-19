import pandas as pd

# Cargar los datasets desde las rutas especificadas
df_ventas = pd.read_csv('market analysis/datasets/historial_ventas_comida_rapida.csv')
df_encuestas = pd.read_csv('market analysis/datasets/encuestas_clientes.csv')
df_popularidad = pd.read_csv('market analysis/datasets/popularidad_preferencias_final.csv')

# Resumen de ventas totales por producto
ventas_totales = df_ventas.groupby('Nombre del Producto').sum()['Cantidad']
print("Ventas Totales por Producto:")
print(ventas_totales)   

# Resumen de preferencias de encuestas
preferencias_encuestas = df_encuestas.groupby(['Bebida Favorita', 'Comida Favorita', 'Postre Favorito']).size().reset_index(name='Conteo')
print("Preferencias de Encuestas:")
print(preferencias_encuestas)

# Resumen de popularidad de productos
popularidad = df_popularidad.set_index('Producto')['Porcentaje de Preferencia']
print("Popularidad por Producto:")
print(popularidad)

# Calcular la rentabilidad de cada producto
precios_venta = df_ventas.groupby('Nombre del Producto').first()['Precio de Venta por Unidad (MXN)']
costos_produccion = {
    'Pozol': 20.0, 'Coca-Cola': 15.0, 'Gordita': 30.0,
    'Empanada': 35.0, 'Taco': 22.0, 'Nuegado': 15.0, 'Turrón': 20.0
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
