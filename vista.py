from tkinter import Tk
from tkinter import Entry
from tkinter import Button
from tkinter import Menu
from tkinter import Label
from tkinter import StringVar
from tkinter import messagebox
from tkinter.constants import E, W
from tkinter.ttk import Treeview
from modelo import Modelo
import re


class Ventanita(Tk):
    def __init__(self):
        super().__init__()
        self.modelo = Modelo()
        self.modelo.crear_tabla()

        self.crear_ventana()
        self.crear_menu()
        self.crear_entrada_datos()
        self.crear_buttons()
        self.crear_treeview()
        self.configure_grid()
        self.cargar_treeview()

        self.mainloop()

    def configure_grid(self):
        for i in range(1, 12, 2):
            self.grid_rowconfigure(i, weight=1, minsize=5)

        for i in range(7):
            self.grid_columnconfigure(i, weight=1, minsize=5 if i % 2 == 0 else 113)

    def crear_ventana(self):
        self.title("MIS CONTRASEÑAS")
        self.geometry("370x400")
        self.configure(bg="#F6CCFF")

    def crear_menu(self):
        menubar = Menu(self)
        menu_archivo = Menu(menubar, tearoff=0)
        menu_archivo.add_command(label="Editar", command=self.vista_editar)
        menu_archivo.add_command(label="Borrar", command=self.vista_borrar)

        menu_archivo.add_separator()

        menu_archivo.add_command(label="Salir", command=self.salir)
        menubar.add_cascade(label="Archivo", menu=menu_archivo)
        menu_edicion = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Editar", menu=menu_edicion)
        submenu = Menu(menu_edicion, tearoff=0)
        submenu.add_command(label="Tema 1", command=self.tema_1)
        submenu.add_command(label="Tema 2", command=self.tema_2)
        submenu.add_command(label="Tema 3", command=self.tema_3)
        menu_edicion.add_cascade(label="Temas", menu=submenu)
        self.config(menu=menubar)

    def crear_entrada_datos(self):
        self.titulo = Label(
            self, text="Completa los siguientes datos", bg="#9D49EB", fg="#E3E2E0"
        )
        self.titulo.grid(row=0, column=0, columnspan=7, sticky=W + E)

        self.app = Label(self, text="Aplicación: ", bg="#F6CCFF", fg="#075659")
        self.app.grid(row=2, column=1, sticky=E)

        self.var_app = StringVar()
        self.entrada1 = Entry(self, textvariable=self.var_app)
        self.entrada1.grid(row=2, column=2, columnspan=4, sticky=W + E)

        self.var_usuario = Label(self, text="Tu Usuario: ", bg="#F6CCFF", fg="#075659")
        self.var_usuario.grid(row=4, column=1, sticky=E)

        self.var_usuario = StringVar()
        self.entrada2 = Entry(self, textvariable=self.var_usuario)
        self.entrada2.grid(row=4, column=2, columnspan=4, sticky=W + E)

        self.var_contrasena = Label(
            self, text="Contraseña: ", bg="#F6CCFF", fg="#075659"
        )
        self.var_contrasena.grid(row=6, column=1, sticky=E)

        self.var_contrasena = StringVar()
        self.entrada3 = Entry(self, textvariable=self.var_contrasena)
        self.entrada3.grid(row=6, column=2, columnspan=4, sticky=W + E)

    def crear_buttons(self):
        self.boton_guardar = Button(
            self,
            text="Guardar",
            bg="#E23AEB",
            fg="#E3E2E0",
            padx=15,
            command=self.vista_alta,
        )
        self.boton_guardar.grid(row=8, column=1)

        self.boton_borrar = Button(
            self,
            text="Borrar",
            bg="#E23AEB",
            fg="#E3E2E0",
            padx=15,
            command=self.vista_borrar,
        )
        self.boton_borrar.grid(row=8, column=3)

        self.boton_editar = Button(
            self,
            text="Editar",
            bg="#E23AEB",
            fg="#E3E2E0",
            padx=15,
            command=self.vista_editar,
        )
        self.boton_editar.grid(row=8, column=5)

    def crear_treeview(self):
        self.tree = Treeview(self)
        self.tree["columns"] = ("col1", "col2", "col3")
        self.tree.column("#0", width=40)
        self.tree.column("col1", width=100)
        self.tree.column("col2", width=100)
        self.tree.column("col3", width=100)
        self.tree.heading("#0", text="ID")
        self.tree.heading("col1", text="Aplicación")
        self.tree.heading("col2", text="Usuario")
        self.tree.heading("col3", text="Contraseña")
        self.tree.grid(row=10, column=1, columnspan=5)

        self.tree.bind(
            "<Button-1>",
            lambda event: self.seleccionar_usando_clic(event),
        )

    def cargar_treeview(self):
        records = self.tree.get_children()

        for element in records:
            self.tree.delete(element)

        resultado = self.modelo.extraer_registros()

        for fila in resultado:
            self.tree.insert("", 0, text=fila[0], values=(fila[1], fila[2], fila[3]))

    def seleccionar_usando_clic(self, event):
        item = self.tree.identify("item", event.x, event.y)
        self.var_app.set(self.tree.item(item, "values")[0])
        self.var_usuario.set(self.tree.item(item, "values")[1])
        self.var_contrasena.set(self.tree.item(item, "values")[2])

    def vista_alta(self):
        cadena_1 = self.var_app.get()
        cadena_2 = self.var_usuario.get()
        cadena_3 = self.var_contrasena.get()
        patron = "^[A-Za-zÁÉÍÓÚáéíóúñÑ\s]*$"

        if (
            re.match(patron, cadena_1)
            and re.match(patron, cadena_2)
            and re.match(patron, cadena_3)
        ):
            data = (
                self.var_app.get(),
                self.var_usuario.get(),
                self.var_contrasena.get(),
            )
            if not all(data):
                messagebox.showwarning("¡ATENCION!", "Error en carga de datos")
                return
            self.modelo.alta(data)

            self.limpiar_campos()
            self.cargar_treeview()

            messagebox.showinfo("¡ATENCION!", "Carga realizada correctamente")
        else:
            messagebox.showwarning("¡ATENCION!", "Error en carga de datos")

    def vista_editar(self):
        valor = self.tree.selection()
        item = self.tree.item(valor)
        mi_id = item["text"]
        data = mi_id
        cadena_1 = self.var_app.get()
        cadena_2 = self.var_usuario.get()
        cadena_3 = self.var_contrasena.get()
        patron = "^[A-Za-zÁÉÍÓÚáéíóúñÑ\s]*$"
        if (
            re.match(patron, cadena_1)
            and re.match(patron, cadena_2)
            and re.match(patron, cadena_3)
        ):
            datos = (
                self.var_app.get(),
                self.var_usuario.get(),
                self.var_contrasena.get(),
                data,
            )
            if not all(datos):
                messagebox.showwarning("¡ATENCION!", "Error en carga de datos")
                return
            self.modelo.editar(datos)

            self.limpiar_campos()
            self.cargar_treeview()

            messagebox.showinfo("¡ATENCION!", "Carga realizada correctamente")
        else:
            messagebox.showwarning("¡ATENCION!", "Error en carga de datos")

    def vista_borrar(self):
        valor = self.tree.selection()
        item = self.tree.item(valor)
        mi_id = item["text"]
        data = (mi_id,)
        # self.tree.delete(data)

        self.modelo.borrar(data)
        self.limpiar_campos()
        self.cargar_treeview()

    def tema_1(self):
        self.configure(bg="#AF6CCFF")
        self.titulo.configure(bg="#075659", fg="#E3E2E0")
        self.var_app.configure(bg="#AF6CCFF", fg="#075659")
        self.var_usuario.configure(bg="#AF6CCFF", fg="#075659")
        self.var_contrasena.configure(bg="#AF6CCFF", fg="#075659")
        self.boton_guardar.configure(bg="#075659", fg="#E3E2E0")
        self.boton_borrar.configure(bg="#075659", fg="#E3E2E0")
        self.boton_editar.configure(bg="#075659", fg="#E3E2E0")

    def tema_2(self):
        self.configure(bg="#8C7954")
        self.titulo.configure(bg="#59492C", fg="#BFB7A8")
        self.app.configure(bg="#8C7954", fg="#000000")
        self.usuario.configure(bg="#8C7954", fg="#000000")
        self.contrasena.configure(bg="#8C7954", fg="#000000")
        self.boton_guardar.configure(bg="#59492C", fg="#BFB7A8")
        self.boton_borrar.configure(bg="#59492C", fg="#BFB7A8")
        self.boton_editar.configure(bg="#59492C", fg="#BFB7A8")

    def tema_3(self):
        self.configure(bg="#9DA65D")
        self.titulo.configure(bg="#6C733D", fg="#FFFFFF")
        self.app.configure(bg="#9DA65D", fg="#000000")
        self.usuario.configure(bg="#9DA65D", fg="#000000")
        self.contrasena.configure(bg="#9DA65D", fg="#000000")
        self.boton_guardar.configure(bg="#6C733D", fg="#FFFFFF")
        self.boton_borrar.configure(bg="#6C733D", fg="#FFFFFF")
        self.boton_editar.configure(bg="#6C733D", fg="#FFFFFF")

    def limpiar_campos(self):
        self.var_app.set("")
        self.var_usuario.set("")
        self.var_contrasena.set("")

    def salir(self):
        valor = messagebox.askquestion("Salir", "¿Está seguro que desea salir?")
        if valor == "yes":
            self.destroy()
