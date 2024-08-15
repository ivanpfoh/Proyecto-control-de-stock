import sqlite3
from tkinter import *



#Configuracion de la ventana
root = Tk()
frame = Frame(root)
frame.pack(fill="both", expand=1)
root.geometry("400x400")
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


def datos_a_texto(n):
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
    
    cursor.execute("INSERT INTO productos VALUES"
    "(NULL ,'{}','{}','{}', {})".format(nombre_producto,marca_producto,precio_producto,cantidad_producto))
    entrada_nombre.delete()
    entrada_marca.delete()
    entrada_precio.delete()
    entrada_cantidad.delete()
    conexion.commit()
    conexion.close()
    
    
    
#label 1

label1 = Label(frame, text="Nombre del producto: ")
label1.grid(row=1, column=0,  padx=3, pady=3)
entrada_nombre = Entry(frame, textvariable=nombre_producto)
entrada_nombre.grid(row=1, column=1)


#label 2

label2 = Label(frame, text="Marca del producto: ")
label2.grid(row=2, column=0, padx=3, pady=3)
entrada_marca = Entry(frame, textvariable=marca_producto)
entrada_marca.grid(row=2, column=1)


#label 3

label3 = Label(frame, text="Precio del producto: ")
label3.grid(row=3, column=0, padx=3, pady=3)
entrada_precio = Entry(frame, textvariable=precio_producto)
entrada_precio.grid(row=3, column=1)


#label 4

label4 = Label(frame, text="Cantidad en Stock del producto: ")
label4.grid(row=4, column=0,  padx=3, pady=3)
entrada_cantidad = Entry(frame, textvariable=cantidad_producto)
entrada_cantidad.grid(row=4, column=1)


#Boton para enviar

Button(frame, text="Guardar", command=guardar).grid(row=5, column=1) 

#Separador


#Espacio para ver datos actuales en la base de datos

Button(frame, text="Ver los datos actuales", command=resultados).grid(row=7,column=0, pady=10) 

label5 = Label(frame, text="\tid\tNombre  |marca  |precio  |cantidad", justify=CENTER)
label5.grid(row=8,column=0)


SalidaDeDatos = Label(frame, text="")
SalidaDeDatos.grid(row=9)


root.mainloop()