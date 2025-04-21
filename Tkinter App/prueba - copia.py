from tkinter import Canvas,Frame

import customtkinter as ctk
from customtkinter import CTk, CTkLabel, CTkButton, CTkEntry, CTkComboBox, CTkTextbox, CTkToplevel, CTkScrollbar,CTkFrame
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Clase Storage
class Storage:
    def __init__(self, name: str):
        self.name = name
        self.stock = []

    def add_liquor(self, liquor):
        self.stock.append(liquor)
        liquor.status = f"EN {self.name.upper()}"
        print(f"{liquor.name} ahora está almacenado en {self.name.upper()}.")

    def search_liquor(self, name: str):
        for liquor in self.stock:
            if liquor.name.lower() == name.lower():
                return liquor
        return None

    def remove_liquor(self, name: str, amount: int):
        liquor = self.search_liquor(name)
        if liquor:
            if 0 < amount <= liquor.amount:
                liquor.amount -= amount
                if liquor.amount == 0:
                    self.stock.remove(liquor)
                return liquor
            else:
                print(f"No se pueden eliminar {amount} unidad(es). Solo hay {liquor.amount} disponible(s).")
        else:
            print(f"No se encontró ningún licor con el nombre '{name}'.")
        return None

    def move_liquor(self, name: str, amount: int, target_storage):
        liquor_to_move = self.remove_liquor(name, amount)
        if liquor_to_move:
            moved_liquor = Liquor(liquor_to_move.name, liquor_to_move.type, amount)
            target_storage.add_liquor(moved_liquor)
            print(f"{amount} unidad(es) de {liquor_to_move.name} movida(s) de {self.name.upper()} a {target_storage.name.upper()}.")

    def get_inventory(self):
        return [f"{liquor.name} ({liquor.type}): {liquor.amount} unidad(es)" for liquor in self.stock]


# Clase Liquor
class Liquor:
    def __init__(self, name: str, type: str, amount: int):
        self.name = name
        self.type = type
        self.amount = amount
        self.status = "EN BODEGA"


# Clase principal con la interfaz gráfica
class InventoryApp:
    def __init__(self, window):
        self.window = window
        self.window.geometry("800x600")
        self.window.title("Gestión de Inventario")
        

        # Inventarios
        self.inventario = Storage("Inventario")
        self.caba_salon = Storage("Caba salón")
        self.bodega = Storage("Bodega")

        # Título principal
        title = CTkLabel(master=window, text="Gestión de Inventario", font=("Arial", 20))
        title.place(relx=0.5, rely=0.03, anchor="n")

        # Crear el Canvas
        self.canvas = tk.Canvas(window, width=800, height=400, bg="gray", highlightthickness=0)
        self.canvas.place(x=100, y=100)  # Posicionar el Canvas

        # Crear Scrollbar vertical conectada al Canvas
        self.scrollbar = ttk.Scrollbar(window, orient="vertical", command=self.canvas.yview)
        self.scrollbar.place(x=900, y=100, height=400)  # Posicionar la Scrollbar al lado del Canvas

        # Configurar el Canvas para que use la Scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Crear el Frame dentro del Canvas
        self.frame = tk.Frame(self.canvas, bg="gray")
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        # Crear encabezados de la tabla
        headers = ["NOMBRE", "TIPO", "CANTIDAD", "ESTADO"]
        for col_index, header in enumerate(headers):
            label = ctk.CTkLabel(master=self.window, text=header, anchor="center", width=150, height=30, corner_radius=5, fg_color="gray")
            label.grid(row=0, column=col_index, padx=5, pady=5)

        # Mostrar los datos del inventario en filas
        for row_index, licor in Storage:
            values = [licor.nombre, licor.tipo, licor.cantidad, licor.estado]
            for col_index, value in enumerate(values):
                cell = ctk.CTkLabel(master=self.frame, text=value, anchor="w", width=150, height=30, corner_radius=5)
                cell.grid(row=row_index, column=col_index, padx=5, pady=5)

        # Actualizar la región desplazable del Canvas según el tamaño del Frame
        self.frame.bind("<Configure>", self.update_scrollregion)

    def update_scrollregion(self, event):
        """Actualizar la región desplazable del Canvas según el tamaño del Frame."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))        





        # Botones para las funcionalidades
        add_button = CTkButton(master=window, text="Añadir Licor", corner_radius=12, command=self.windowadd_liquor)
        add_button.place(relx=0.05, rely=0.95, anchor="sw")

        sell_remove_button = CTkButton(master=window, text="Vender/Remover", corner_radius=12, command=self.window_sell_or_remove)
        sell_remove_button.place(relx=0.35, rely=0.95, anchor="s")

        move_button = CTkButton(master=window, text="Mover Licor", corner_radius=12, command=self.window_move_liquor)
        move_button.place(relx=0.55, rely=0.95, anchor="s")

        update_button = CTkButton(master=window, text="Actualizar Inventario", corner_radius=12, command=self.update_inventory_display)
        update_button.place(relx=0.95, rely=0.95, anchor="se")

    # Ventana para añadir licor
    def windowadd_liquor(self):
        addwindow = CTkToplevel(self.window)
        addwindow.geometry("600x400")
        addwindow.title("Añadir Licor")

        addtitle = CTkLabel(master=addwindow, text="Añadir al Inventario:", font=("Arial", 18))
        addtitle.place(relx=0.5, rely=0.03, anchor="n")

        liquorname = CTkEntry(master=addwindow, placeholder_text="Escriba Nombre del Ítem...")
        liquorname.place(relx=0.5, rely=0.2, anchor="center")

        category_button = CTkComboBox(master=addwindow, values=["Vino", "Whiskey", "Ron", "Aguardiente"])
        category_button.place(relx=0.5, rely=0.3, anchor="center")

        liquoramount = CTkEntry(master=addwindow, placeholder_text="Escriba Cantidad...")
        liquoramount.place(relx=0.5, rely=0.4, anchor="center")

        def add():
            try:
                name = liquorname.get()
                category = category_button.get()
                amount = int(liquoramount.get())
                if name and category and amount > 0:
                    liquor = Liquor(name, category, amount)
                    self.inventario.add_liquor(liquor)
                    messagebox.showinfo("Éxito", f"{name} añadido al inventario.")
                    addwindow.destroy()
                else:
                    messagebox.showwarning("Error", "Por favor complete todos los campos correctamente.")
            except ValueError:
                messagebox.showwarning("Error", "La cantidad debe ser un número válido.")

        add_button2 = CTkButton(master=addwindow, text="Añadir", command=add)
        add_button2.place(relx=0.5, rely=0.5, anchor="center")

    # Ventana para vender/remover ítem
    def window_sell_or_remove(self):
        # Similar a lo que ya tienes implementado...
        pass

    # Ventana para mover ítem entre inventarios
    def window_move_liquor(self):
        move_window = CTkToplevel(self.window)
        move_window.geometry("600x400")
        move_window.title("Mover Licor Entre Inventarios")

        title = CTkLabel(master=move_window, text="Mover Licor", font=("Arial", 18))
        title.place(relx=0.5, rely=0.03, anchor="n")

        liquorname = CTkEntry(master=move_window, placeholder_text="Nombre del Ítem...")
        liquorname.place(relx=0.5, rely=0.2, anchor="center")

        amount_entry = CTkEntry(master=move_window, placeholder_text="Cantidad...")
        amount_entry.place(relx=0.5, rely=0.3, anchor="center")

        destination_combo = CTkComboBox(master=move_window, values=["Caba salón", "Bodega"])
        destination_combo.place(relx=0.5, rely=0.4, anchor="center")

        def move():
            try:
                name = liquorname.get()
                amount = int(amount_entry.get())
                destination = destination_combo.get()
                target_storage = None
                if destination == "Caba salón":
                    target_storage = self.caba_salon
                elif destination == "Bodega":
                    target_storage = self.bodega

                if target_storage:
                    self.inventario.move_liquor(name, amount, target_storage)
                    messagebox.showinfo("Éxito", f"{amount} unidad(es) de {name} movida(s) a {destination}.")
                    self.update_inventory_display()
                    move_window.destroy()
                else:
                    messagebox.showwarning("Error", "Inventario de destino no válido.")
            except ValueError:
                messagebox.showwarning("Error", "La cantidad debe ser un número válido.")

        move_button = CTkButton(master=move_window, text="Mover", command=move)
        move_button.place(relx=0.5, rely=0.5, anchor="center")

    # Actualizar la visualización del inventario
    def update_inventory_display(self):
        # Encabezados de la tabla
        headers = f"{'NOMBRE':<20} {'TIPO':<15} {'CANTIDAD':<15} {'UBICACIÓN':<15}"
        separator = "-" * 60

        # Combinar los inventarios en un solo listado
        inventory_list = [
            f"{liquor.name:<20} {liquor.type:<20} {liquor.amount:<20} {liquor.status:<20}"
            for storage in [self.inventario, self.caba_salon, self.bodega]
            for liquor in storage.stock
        ]

        # Combinar encabezados, separador y cuerpo en un texto final
        table_text = f"{headers}\n{separator}\n" + "\n".join(inventory_list)

        # Actualizar el CTkTextbox con la tabla completa
        self.inventory_display.configure(state="normal")  # Permitir edición temporal
        self.inventory_display.delete("0.0", "end")  # Limpiar contenido actual
        if inventory_list:
            self.inventory_display.insert("0.0", table_text)  # Insertar la tabla formateada
        else:
            self.inventory_display.insert("0.0", "El inventario está vacío.\n")  # Mensaje si no hay ítems
        self.inventory_display.configure(state="disabled")  # Volver a modo de solo lectura



# Ejecutar la aplicación
window = CTk()
app = InventoryApp(window)
window.mainloop()