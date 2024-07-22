import pandas as pd

productos_dict = {
    "Pozol": {"costo": 7, "venta": 15},
    "Coca-Cola": {"costo": 18, "venta": 25},
    "Tascalate": {"costo": 8, "venta": 14},
    "Agua de chía": {"costo": 11, "venta": 25},
    "Agua de horchata": {"costo": 10, "venta": 20},
    "Agua de jamaica": {"costo": 9, "venta": 18},
    "Quesadilla": {"costo": 12, "venta": 22},
    "Gordita": {"costo": 10, "venta": 18},
    "Taco": {"costo": 9, "venta": 14},
    "Empanada": {"costo": 8, "venta": 15},
    "Tamal": {"costo": 10, "venta": 20},
    "Tostada": {"costo": 7, "venta": 12},
    "Turrón": {"costo": 4, "venta": 10},
    "Nuegado": {"costo": 5, "venta": 12},
    "Turulete": {"costo": 3, "venta": 10},
    "Cocada": {"costo": 4, "venta": 8},
    "Plátano Asado": {"costo": 4, "venta": 9},
    "Bunuelo": {"costo": 5, "venta": 10},
}

productos_df = pd.DataFrame.from_dict(productos_dict, orient='index')

productos_df.to_csv('market analysis/datasets/precios_productos.csv')