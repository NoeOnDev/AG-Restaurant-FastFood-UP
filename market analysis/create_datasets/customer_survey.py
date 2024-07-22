import pandas as pd
import random

bebidas = ["Pozol", "Coca-Cola", "Tascalate", "Agua de chía", "Agua de horchata", "Agua de jamaica"]
comidas = ["Gordita", "Empanada", "Taco", "Quesadilla", "Tamal", "Tostada"]
postres = ["Nuegado", "Turrón", "Turulete", "Cocada", "Plátano Asado", "Bunuelo"]

frecuencia_consumo = ["Diario", "Semanal", "Mensual", "Rara vez"]

num_encuestas = 1000

encuestas = []
for i in range(1, num_encuestas + 1):
    bebida = random.choice(bebidas)
    comida = random.choice(comidas)
    postre = random.choice(postres)
    frecuencia = random.choice(frecuencia_consumo)
    
    encuestas.append([
        i,
        bebida,
        comida,
        postre,
        frecuencia
    ])

df_encuestas = pd.DataFrame(encuestas, columns=[
    "Número de Encuesta",
    "Bebida Favorita",
    "Comida Favorita",
    "Postre Favorito",
    "Frecuencia de Consumo"
])

df_encuestas.to_csv('market analysis/datasets/encuestas_clientes.csv', index=False)