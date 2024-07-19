import pandas as pd
import matplotlib.pyplot as plt
import os

df_encuestas = pd.read_csv('market analysis/datasets/encuestas_clientes.csv')

output_dir = 'market analysis/images'
os.makedirs(output_dir, exist_ok=True)

for archivo in os.listdir(output_dir):
    ruta_archivo = os.path.join(output_dir, archivo)
    if os.path.isfile(ruta_archivo):
        os.remove(ruta_archivo)

def guardar_grafica(df, columna, titulo, nombre_archivo):
    plt.figure(figsize=(10, 6))
    counts = df[columna].value_counts(normalize=True) * 100
    counts.plot(kind='bar', color='skyblue')
    plt.title(titulo)
    plt.xlabel(columna)
    plt.ylabel('Porcentaje')
    plt.xticks(rotation=45)
    for i, v in enumerate(counts):
        plt.text(i, v + 0.5, f"{v:.2f}%", ha='center', va='bottom')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, nombre_archivo))
    plt.close()

guardar_grafica(df_encuestas, 'Bebida Favorita', 'Preferencias de Bebida (%)', 'preferencias_bebida.png')
guardar_grafica(df_encuestas, 'Comida Favorita', 'Preferencias de Comida (%)', 'preferencias_comida.png')
guardar_grafica(df_encuestas, 'Postre Favorito', 'Preferencias de Postre (%)', 'preferencias_postre.png')
guardar_grafica(df_encuestas, 'Frecuencia de Consumo', 'Frecuencia de Consumo (%)', 'frecuencia_consumo.png')
