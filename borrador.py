import sqlite3

conexion = sqlite3.connect('stock.db')
cursor = conexion.cursor()
nombre_producto_ingresado= input("Ingresar nombre del producto:\n>")

resultado = cursor.execute("SELECT * FROM productos WHERE name_producto='{}'".format(nombre_producto_ingresado)).fetchall()
print(resultado)


conexion.close()