import sqlite3
from tkinter import *
from tkinter import ttk, messagebox


# FUNCIONES DE BASE DE DATOS

def crear_tabla():
    with sqlite3.connect('stock.db') as conexion:
        cursor = conexion.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_producto TEXT NOT NULL,
                marca_producto TEXT NOT NULL,
                precio_producto REAL NOT NULL,
                cantidad_producto INTEGER NOT NULL
            )
        ''')
        conexion.commit()

def agregar_producto(nombre, marca, precio, cantidad):
    try:
        with sqlite3.connect('stock.db') as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO productos (nombre_producto, marca_producto, precio_producto, cantidad_producto) VALUES (?, ?, ?, ?)",
                (nombre, marca, precio, cantidad)
            )
            conexion.commit()
        return True
    except sqlite3.Error as e:
        print("Error al agregar producto:", e)
        return False

def borrar_producto(nombre):
    with sqlite3.connect('stock.db') as conexion:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM productos WHERE nombre_producto=?", (nombre,))
        conexion.commit()
        return cursor.rowcount  # devuelve la cantidad de filas eliminadas

def buscar_producto(nombre):
    with sqlite3.connect('stock.db') as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos WHERE nombre_producto=?", (nombre,))
        return cursor.fetchone()

def obtener_todos_productos():
    with sqlite3.connect('stock.db') as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos")
        return cursor.fetchall()

# =========================
# FUNCIONES DE LA INTERFAZ
# =========================
def validar_y_guardar():
    nombre = entrada_nombre.get().strip()
    marca = entrada_marca.get().strip()
    try:
        precio = float(entrada_precio.get())
        cantidad = int(entrada_cantidad.get())
    except ValueError:
        messagebox.showerror("Error", "Precio o cantidad no válidos")
        return

    if not nombre or not marca:
        messagebox.showerror("Error", "Nombre y marca no pueden estar vacíos")
        return

    if agregar_producto(nombre, marca, precio, cantidad):
        messagebox.showinfo("Éxito", "Producto agregado correctamente")
        limpiar_entradas()
        mostrar_productos()
    else:
        messagebox.showerror("Error", "No se pudo agregar el producto")

def limpiar_entradas():
    entrada_nombre.delete(0, END)
    entrada_marca.delete(0, END)
    entrada_precio.delete(0, END)
    entrada_cantidad.delete(0, END)

def eliminar_producto():
    nombre = entrada_borrar.get().strip()
    if not nombre:
        messagebox.showwarning("Aviso", "Ingrese el nombre del producto a eliminar")
        return
    cantidad_eliminada = borrar_producto(nombre)
    if cantidad_eliminada:
        messagebox.showinfo("Éxito", f"Producto '{nombre}' eliminado")
        entrada_borrar.delete(0, END)
        mostrar_productos()
    else:
        messagebox.showerror("Error", f"No se encontró el producto '{nombre}'")

def buscar_y_mostrar():
    nombre = entrada_buscar.get().strip()
    if not nombre:
        messagebox.showwarning("Aviso", "Ingrese el nombre del producto a buscar")
        return
    resultado = buscar_producto(nombre)
    if resultado:
        treeview.selection_remove(treeview.selection())
        treeview.delete(*treeview.get_children())
        treeview.insert("", END, values=resultado)
    else:
        messagebox.showinfo("Resultado", "No se encontró el producto")
    entrada_buscar.delete(0, END)

def mostrar_productos():
    treeview.delete(*treeview.get_children())
    for producto in obtener_todos_productos():
        treeview.insert("", END, values=producto)


# CONFIGURACION DE LA VENTANA

root = Tk()
root.title("Control de Stock")
root.geometry("850x600")
root.resizable(False, False)
root.config(bg="#f0f0f0")

# Titulo
Label(root, text="Control de Stock", font=("Verdana", 18, "bold"), bg="#f0f0f0").pack(pady=10)

# Frame para entradas
frame_entradas = Frame(root, bg="#d9d9d9", bd=2, relief="groove")
frame_entradas.pack(pady=10, padx=10, fill="x")

# Entradas para agregar producto
Label(frame_entradas, text="Nombre:", bg="#d9d9d9").grid(row=0, column=0, padx=5, pady=5, sticky=W)
entrada_nombre = Entry(frame_entradas, width=20)
entrada_nombre.grid(row=0, column=1, padx=5, pady=5)

Label(frame_entradas, text="Marca:", bg="#d9d9d9").grid(row=0, column=2, padx=5, pady=5, sticky=W)
entrada_marca = Entry(frame_entradas, width=20)
entrada_marca.grid(row=0, column=3, padx=5, pady=5)

Label(frame_entradas, text="Precio:", bg="#d9d9d9").grid(row=1, column=0, padx=5, pady=5, sticky=W)
entrada_precio = Entry(frame_entradas, width=20)
entrada_precio.grid(row=1, column=1, padx=5, pady=5)

Label(frame_entradas, text="Cantidad:", bg="#d9d9d9").grid(row=1, column=2, padx=5, pady=5, sticky=W)
entrada_cantidad = Entry(frame_entradas, width=20)
entrada_cantidad.grid(row=1, column=3, padx=5, pady=5)

Button(frame_entradas, text="Agregar Producto", command=validar_y_guardar, bg="#4caf50", fg="white").grid(row=2, column=0, columnspan=4, pady=10)

# Frame para buscar y borrar
frame_buscar_borrar = Frame(root, bg="#d9d9d9", bd=2, relief="groove")
frame_buscar_borrar.pack(pady=10, padx=10, fill="x")

# Buscar
Label(frame_buscar_borrar, text="Buscar producto por nombre:", bg="#d9d9d9").grid(row=0, column=0, padx=5, pady=5, sticky=W)
entrada_buscar = Entry(frame_buscar_borrar, width=30)
entrada_buscar.grid(row=0, column=1, padx=5, pady=5)
Button(frame_buscar_borrar, text="Buscar", command=buscar_y_mostrar, bg="#2196f3", fg="white").grid(row=0, column=2, padx=5, pady=5)

# Borrar
Label(frame_buscar_borrar, text="Eliminar producto por nombre:", bg="#d9d9d9").grid(row=1, column=0, padx=5, pady=5, sticky=W)
entrada_borrar = Entry(frame_buscar_borrar, width=30)
entrada_borrar.grid(row=1, column=1, padx=5, pady=5)
Button(frame_buscar_borrar, text="Eliminar", command=eliminar_producto, bg="#f44336", fg="white").grid(row=1, column=2, padx=5, pady=5)

# Frame para tabla de productos
frame_tabla = Frame(root)
frame_tabla.pack(pady=10, padx=10, fill="both", expand=True)

# Scrollbar
scrollbar = Scrollbar(frame_tabla)
scrollbar.pack(side=RIGHT, fill=Y)

# Treeview para mostrar productos
treeview = ttk.Treeview(frame_tabla, columns=("ID","Nombre","Marca","Precio","Cantidad"), show="headings", yscrollcommand=scrollbar.set)
treeview.heading("ID", text="ID")
treeview.heading("Nombre", text="Nombre")
treeview.heading("Marca", text="Marca")
treeview.heading("Precio", text="Precio")
treeview.heading("Cantidad", text="Cantidad")
treeview.column("ID", width=50, anchor=CENTER)
treeview.column("Nombre", width=150)
treeview.column("Marca", width=150)
treeview.column("Precio", width=100, anchor=CENTER)
treeview.column("Cantidad", width=100, anchor=CENTER)
treeview.pack(fill="both", expand=True)
scrollbar.config(command=treeview.yview)

# Crear tabla y mostrar productos iniciales
crear_tabla()
mostrar_productos()

root.mainloop()