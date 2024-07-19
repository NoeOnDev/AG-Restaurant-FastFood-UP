import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

productos = [
    {"nombre": "Pozol", "precio_produccion": 13.60, "precio_venta": 34.00},
    {"nombre": "Coca-Cola", "precio_produccion": 8.50, "precio_venta": 25.50},
    {"nombre": "Gordita", "precio_produccion": 17.00, "precio_venta": 42.50},
    {"nombre": "Empanada", "precio_produccion": 20.40, "precio_venta": 51.00},
    {"nombre": "Taco", "precio_produccion": 12.75, "precio_venta": 34.00},
    {"nombre": "Nuegado", "precio_produccion": 8.50, "precio_venta": 25.50},
    {"nombre": "Turrón", "precio_produccion": 11.90, "precio_venta": 34.00},
]

num_filas = 200
fecha_inicio = datetime(2023, 1, 1)
ventas_por_dia = random.randint(5, 100)

fechas_venta = []
for i in range(num_filas // ventas_por_dia + 1):
    for j in range(ventas_por_dia):
        fecha_venta = fecha_inicio + timedelta(days=i, hours=random.randint(0, 23), minutes=random.randint(0, 59))
        fechas_venta.append(fecha_venta.strftime('%Y-%m-%d %H:%M:%S'))

fechas_venta = fechas_venta[:num_filas]

dataset = []
for i in range(num_filas):
    id_transaccion = i + 1
    producto = random.choice(productos)
    cantidad = random.randint(1, 10)
    precio_venta_unidad = producto["precio_venta"]
    precio_total_venta = precio_venta_unidad * cantidad
    
    dataset.append([
        fechas_venta[i],
        id_transaccion,
        producto["nombre"],
        cantidad,
        precio_venta_unidad,
        precio_total_venta
    ])

df = pd.DataFrame(dataset, columns=[
    "Fecha y Hora de la Venta",
    "ID de la Transacción",
    "Nombre del Producto",
    "Cantidad",
    "Precio de Venta por Unidad (MXN)",
    "Precio Total de la Venta (MXN)"
])

df.to_csv('historial_ventas_comida_rapida.csv', index=False)

df.head()
