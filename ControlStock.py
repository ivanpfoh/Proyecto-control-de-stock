import sqlite3
from tkinter import *



#Configuracion de la ventana
root = Tk()
frame = Frame(root)
frame.pack(fill="both", expand=1)
root.geometry("800x800")
root.resizable(False, True)
frame.config(bg="lightgrey")
root.config( relief="sunken", bd=9)

#Label 0 , Titulo
label = Label(frame, text="Control de Stock", font=("Verdana", 15))
label.grid(row=0, column=0, padx=10, pady=10)

#Variables para ejecutar las tareas de guardado 
nombre_producto = StringVar()
marca_producto = StringVar()
precio_producto = StringVar()
cantidad_producto = StringVar()
tabla_productos = StringVar()
nombre_producto_ingresado = StringVar()
nombre_producto_borrar = StringVar()

def borrar_por_nombre():
    
    conexion = sqlite3.connect('stock.db')
    cursor = conexion.cursor()
    try:
        nombre_producto_borrar = Entrada_Nombre_borrar.get()
        cursor.execute("DELETE FROM productos WHERE name_producto=?",(nombre_producto_borrar,))
        Entrada_Nombre_borrar.delete(0, END)
        

    except:
        SalidaDeDatos2.config(text="No se encontro el producto O se ingreso un nombre no valido.")
        Entrada_Nombre_borrar.delete(0, END)
    conexion.commit()
    conexion.close()
    
    
    
    
def buscar_por_nombre():
    conexion = sqlite3.connect('stock.db')
    cursor = conexion.cursor()
    try:
        nombre_producto_ingresado = entrada_datos_busqueda1.get()
        cursor.execute("SELECT * FROM productos WHERE name_producto=?",(nombre_producto_ingresado,))
        resultado = cursor.fetchone()
        entrada_datos_busqueda1.delete(0, END)
        SalidaDeDatos1.config(text=resultado)
        

    except:
        SalidaDeDatos1.config(text="No se encontro el producto O se ingreso un nombre no valido.")
        print("No se encontro el producto O se ingreso un nombre no valido.")
        entrada_datos_busqueda1.delete(0, END)
    
    conexion.close()


def datos_a_texto(n):
    """
    Returns:
        Retorna el texto SQL ordenado
    """
    texto = ""
    for i in n:
        texto += "\t".join(map(str, i)) + "\n"
    return texto


def resultados():
    """
        Ejecuta la consulta de los valores actuales en los registros de la base de datos
    """
    conexion = sqlite3.connect('stock.db')
    cursor = conexion.cursor()
    
    tabla_productos = ""
    tabla = cursor.execute("SELECT * FROM productos").fetchall()
    tabla_productos = datos_a_texto(tabla)
    SalidaDeDatos.config(text=tabla_productos)
    conexion.close()

    

    
def guardar():
    """
        Almacena los valores ingresados por el usuario en la base de datos
    """
    conexion = sqlite3.connect('stock.db')
    cursor = conexion.cursor()
    nombre_producto = entrada_nombre.get()
    marca_producto = entrada_marca.get()
    precio_producto = entrada_precio.get()
    cantidad_producto = entrada_cantidad.get()
    
    cursor.execute("INSERT INTO productos (nombre_producto, marca_producto, precio_producto, cantidad_producto) VALUES (?, ?, ?, ?)",
    (nombre_producto, marca_producto, precio_producto, cantidad_producto))
    
    entrada_nombre.delete(0, END)
    entrada_marca.delete(0, END)
    entrada_precio.delete(0, END)
    entrada_cantidad.delete(0, END)
    conexion.commit()
    conexion.close()
    
    
    
#label y Entry 1 

label1 = Label(frame, text="Nombre del producto: ")
label1.grid(row=1, column=0,  padx=3, pady=3)
entrada_nombre = Entry(frame, textvariable=nombre_producto)
entrada_nombre.grid(row=1, column=1)


#label y Entry 2

label2 = Label(frame, text="Marca del producto: ")
label2.grid(row=2, column=0, padx=3, pady=3)
entrada_marca = Entry(frame, textvariable=marca_producto)
entrada_marca.grid(row=2, column=1)


#label y Entry 3

label3 = Label(frame, text="Precio del producto: ")
label3.grid(row=3, column=0, padx=3, pady=3)
entrada_precio = Entry(frame, textvariable=precio_producto)
entrada_precio.grid(row=3, column=1)


#label y Entry 4

label4 = Label(frame, text="Cantidad en Stock del producto: ")
label4.grid(row=4, column=0,  padx=3, pady=3)
entrada_cantidad = Entry(frame, textvariable=cantidad_producto)
entrada_cantidad.grid(row=4, column=1)

#Boton para almacenar los datos

Button(frame, text="Guardar", command=guardar).grid(row=5, column=1)

#Otro label para Explicar que valor ingresar
SalidaDeDatos2 = Label(frame, text="Ingrese el nombre del producto:")
SalidaDeDatos2.grid(row=6, column=0)



#Boton para buscar un datos especifico por nombre

Button(frame, text="Buscar", command=buscar_por_nombre).grid(row=7, column=1, pady=10)

entrada_datos_busqueda1 = Entry(frame, textvariable=nombre_producto_ingresado)
entrada_datos_busqueda1.grid(row=7, column=0 )



SalidaDeDatos1 = Label(frame, text="")
SalidaDeDatos1.grid(row=8, column=0)


#Boton para eliminar datos especificos de la DB


Button(frame, text="Borrar", command=borrar_por_nombre).grid(row=9, column=1, pady=10)


Entrada_Nombre_borrar = Entry(frame, textvariable=nombre_producto_borrar)
Entrada_Nombre_borrar.grid(row=9, column=0)

SalidaDeDatos2 = Label(frame, text="")
SalidaDeDatos2.grid(row=10, column=0)



#Boton para ver datos actuales en la base de datos
Button(frame, text="Ver los datos actuales", command=resultados).grid(row=13,column=0, pady=10) 

#Breve explicacion de cada columna
label5 = Label(frame, text="\tid\tNombre  |marca  |precio  |cantidad", justify=CENTER)
label5.grid(row=14,column=0)

#Respuesta de datos en la DB
SalidaDeDatos = Label(frame, text="")
SalidaDeDatos.grid(row=15)


root.mainloop()