import pandas as pd
from datetime import datetime, timedelta
import random

productos = [
    {"nombre": "Pozol", "precio_produccion": 7, "precio_venta": 16},
    {"nombre": "Coca-Cola", "precio_produccion": 18, "precio_venta": 26},
    {"nombre": "Tascalate", "precio_produccion": 8, "precio_venta": 15},
    {"nombre": "Agua de chía", "precio_produccion": 11, "precio_venta": 24},
    {"nombre": "Agua de horchata", "precio_produccion": 10, "precio_venta": 21},
    {"nombre": "Agua de jamaica", "precio_produccion": 9, "precio_venta": 19},
    {"nombre": "Quesadilla", "precio_produccion": 12, "precio_venta": 23},
    {"nombre": "Gordita", "precio_produccion": 10, "precio_venta": 19},
    {"nombre": "Taco", "precio_produccion": 9, "precio_venta": 15},
    {"nombre": "Empanada", "precio_produccion": 8, "precio_venta": 16},
    {"nombre": "Tamal", "precio_produccion": 10, "precio_venta": 21},
    {"nombre": "Tostada", "precio_produccion": 7, "precio_venta": 13},
    {"nombre": "Turrón", "precio_produccion": 4, "precio_venta": 11},
    {"nombre": "Nuegado", "precio_produccion": 5, "precio_venta": 13},
    {"nombre": "Turulete", "precio_produccion": 3, "precio_venta": 9},
    {"nombre": "Cocada", "precio_produccion": 4, "precio_venta": 9},
    {"nombre": "Plátano Asado", "precio_produccion": 4, "precio_venta": 10},
    {"nombre": "Bunuelo", "precio_produccion": 5, "precio_venta": 11},
]

num_filas = 9998

fecha_inicio = datetime(2024, 1, 1)

fechas_venta = []

for i in range(num_filas // 10 + 1):
    for j in range(random.randint(10, 100)):
        if len(fechas_venta) >= num_filas:
            break
        fecha_venta = fecha_inicio + timedelta(days=i, hours=7, minutes=random.randint(0, 600))
        fechas_venta.append(fecha_venta)

fechas_venta = sorted(fechas_venta)[:num_filas]

dataset = []
for i, fecha_venta in enumerate(fechas_venta):
    id_transaccion = i + 1
    producto = random.choice(productos)
    cantidad = random.randint(1, 10)
    precio_venta_unidad = producto["precio_venta"]
    precio_total_venta = precio_venta_unidad * cantidad
    
    dataset.append([
        fecha_venta.strftime('%Y-%m-%d %H:%M:%S'),
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

df.to_csv('market analysis/datasets/historial_ventas_comida_rapida.csv', index=False)
df.head()