import pandas as pd

precios_productos = pd.read_csv('market analysis/datasets/precios_productos.csv')
encuestas_clientes = pd.read_csv('market analysis/datasets/encuestas_clientes.csv')

preferencia_bebidas = encuestas_clientes['Bebida Favorita'].value_counts(normalize=True) * 100
preferencia_comidas = encuestas_clientes['Comida Favorita'].value_counts(normalize=True) * 100
preferencia_postres = encuestas_clientes['Postre Favorito'].value_counts(normalize=True) * 100

preferencia_bebidas_dict = (preferencia_bebidas / 100).to_dict()
preferencia_comidas_dict = (preferencia_comidas / 100).to_dict()
preferencia_postres_dict = (preferencia_postres / 100).to_dict()

productos_dict = {}

for index, row in precios_productos.iterrows():
    producto = row['producto']
    costo = row['costo']
    venta = row['venta']
    
    preferencia = preferencia_bebidas_dict.get(producto, 
                    preferencia_comidas_dict.get(producto, 
                    preferencia_postres_dict.get(producto, 0)))
    
    productos_dict[producto] = {"costo": costo, "venta": venta, "preferencia": preferencia}


