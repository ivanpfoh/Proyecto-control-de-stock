import sqlite3

conexion = sqlite3.connect("stock.db")
cursor = conexion.cursor()
cursor.execute("PRAGMA table_info(productos)")
for columna in cursor.fetchall():
    print(columna)
conexion.close()