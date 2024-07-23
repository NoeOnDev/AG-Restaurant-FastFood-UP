import pandas as pd

productos_dict = {
    "Pozol": {"costo": 7, "venta": 16},
    "Coca-Cola": {"costo": 18, "venta": 26},
    "Tascalate": {"costo": 8, "venta": 15},
    "Agua de chía": {"costo": 11, "venta": 24},
    "Agua de horchata": {"costo": 10, "venta": 21},
    "Agua de jamaica": {"costo": 9, "venta": 19},
    "Quesadilla": {"costo": 12, "venta": 23},
    "Gordita": {"costo": 10, "venta": 19},
    "Taco": {"costo": 9, "venta": 15},
    "Empanada": {"costo": 8, "venta": 16},
    "Tamal": {"costo": 10, "venta": 21},
    "Tostada": {"costo": 7, "venta": 13},
    "Turrón": {"costo": 4, "venta": 11},
    "Nuegado": {"costo": 5, "venta": 13},
    "Turulete": {"costo": 3, "venta": 9},
    "Cocada": {"costo": 4, "venta": 9},
    "Plátano Asado": {"costo": 4, "venta": 10},
    "Bunuelo": {"costo": 5, "venta": 11},
}

productos_df = pd.DataFrame.from_dict(productos_dict, orient='index')

productos_df['producto'] = productos_df.index

productos_df = productos_df[['producto', 'costo', 'venta']]

productos_df = productos_df.reset_index(drop=True)

productos_df.to_csv('market analysis/datasets/precios_productos.csv', index=False)
