import pandas as pd

df_encuestas = pd.read_csv('market analysis/datasets/encuestas_clientes.csv')

productos = [
    "Pozol", "Coca-Cola", "Tascalate", "Agua de chía", "Agua de horchata", "Agua de jamaica",
    "Quesadilla", "Gordita", "Taco", "Empanada", "Tamal", "Tostada",
    "Turrón", "Nuegado", "Turulete", "Cocada", "Plátano Asado", "Bunuelo"
]

num_votos_bebida = df_encuestas['Bebida Favorita'].value_counts()
num_votos_comida = df_encuestas['Comida Favorita'].value_counts()
num_votos_postre = df_encuestas['Postre Favorito'].value_counts()

num_votos = pd.concat([num_votos_bebida, num_votos_comida, num_votos_postre]).reindex(productos).fillna(0).astype(int)

porcentaje_preferencia = num_votos / len(df_encuestas)

df_popularidad = pd.DataFrame({
    'Producto': productos,
    'Número de Votos': num_votos.values,
    'Porcentaje de Preferencia': porcentaje_preferencia.values
})

df_popularidad['Porcentaje de Preferencia'] = df_popularidad['Porcentaje de Preferencia'].map('{:.6f}'.format)

df_popularidad.to_csv('market analysis/datasets/popularidad_preferencias_final.csv', index=False)
