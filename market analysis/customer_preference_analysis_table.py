import pandas as pd

df_encuestas = pd.read_csv('market analysis/datasets/encuestas_clientes.csv')

preferencias_bebida = df_encuestas['Bebida Favorita'].value_counts(normalize=True)
preferencias_comida = df_encuestas['Comida Favorita'].value_counts(normalize=True)
preferencias_postre = df_encuestas['Postre Favorito'].value_counts(normalize=True)

df_popularidad = pd.DataFrame({
    'Bebida': preferencias_bebida,
    'Comida': preferencias_comida,
    'Postre': preferencias_postre
}).fillna(0)

orden_filas = ['Pozol', 'Coca-Cola', 'Gordita', 'Empanada', 'Taco', 'Nuegado', 'Turrón']
df_popularidad = df_popularidad.loc[orden_filas]

df_popularidad.to_csv('market analysis/datasets/popularidad_preferencias.csv', index=True)

print("Tabla de popularidad generada y guardada en 'market analysis/datasets/popularidad_preferencias.csv'")
print(df_popularidad)
