import pandas as pd

productos_dict = {
    "Pozol": {"costo": 7, "venta": 15, "preferencia": 0.56},
    "Coca-Cola": {"costo": 18, "venta": 25, "preferencia": 0.44},
    "Quesadilla": {"costo": 12, "venta": 22, "preferencia": 0.3},
    "Gordita": {"costo": 10, "venta": 18, "preferencia": 0.3},
    "Taco": {"costo": 9, "venta": 14, "preferencia": 0.16},
    "Empanada": {"costo": 8, "venta": 15, "preferencia": 0.24},
    "Turrón": {"costo": 4, "venta": 10, "preferencia": 0.48},
    "Nuegado": {"costo": 5, "venta": 12, "preferencia": 0.52}
}

for producto in productos_dict.values():
    del producto['preferencia']

productos_df = pd.DataFrame.from_dict(productos_dict, orient='index')

productos_df.to_csv('precios_productos.csv')