import tkinter as tk


class Liquor:
    def __init__(self, name: str, type: str, amount: int):
        self.name = name
        self.type = type
        self.amount = amount
        self.status = "EN BODEGA"

    def sell(self, n_sell: int):
        if 0 < n_sell <= self.amount:
            self.amount -= n_sell
            print(f"VENDIDO(S): {n_sell} BOTELLA(S) DE: {self.type}, {self.name}. ---- RESTANTES: {self.amount}")
        elif n_sell > self.amount:
            print(f"NO DISPONIBLE: {n_sell} BOTELLA(S) DE {self.type}, {self.name}. SOLO HAY: {self.amount}")
        else:
            print("CANTIDAD INVÁLIDA. INTENTE DE NUEVO.")

class Storage:
    def __init__(self, name: str):
        self.name = name
        self.stock = []

    def add_liquor(self, liquor: Liquor):
        if isinstance(liquor, Liquor):
            self.stock.append(liquor)
            liquor.status = f"EN {self.name.upper()}"
            print(f"{liquor.name} ahora está almacenado en {self.name.upper()}.")
        else:
            print("ERROR: Sólo se pueden añadir objetos de la clase Liquor.")

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
                print(f"{amount} unidad(es) de {liquor.name} procesada(s). Restantes: {liquor.amount}")
                if liquor.amount == 0:
                    self.stock.remove(liquor)
                    print(f"{liquor.name} eliminado completamente del inventario de {self.name.upper()}.")
                return liquor
            elif amount > liquor.amount:
                print(f"NO SE PUEDEN PROCESAR {amount} unidad(es). SÓLO HAY {liquor.amount} DISPONIBLE(S).")
            else:
                print("La cantidad debe ser positiva. Intente de nuevo.")
        else:
            print(f"No se encontró ningún licor con el nombre '{name}'.")
        return None

    def move_liquor(self, name: str, amount: int, target_storage):
        liquor_to_move = self.remove_liquor(name, amount)
        if liquor_to_move:
            moved_liquor = Liquor(liquor_to_move.name, liquor_to_move.type, amount)
            target_storage.add_liquor(moved_liquor)
            print(f"{amount} unidad(es) de {liquor_to_move.name} movida(s) de {self.name.upper()} a {target_storage.name.upper()}.")

    def show_stock(self):
        print(f"\nLicores en {self.name.upper()}:")
        if not self.stock:
            print("No hay licores almacenados aquí.")
        else:
            for liquor in self.stock:
                print(f"- {liquor.name} ({liquor.type}): {liquor.amount} unidad(es). Estado: {liquor.status}")

# Crear inventarios
inventario = Storage("Inventario")
caba_salon = Storage("Caba salón")

# Menú principal
def show_menu():
    print("\n---------------------------------")
    print("  SISTEMA DE INVENTARIO DE LICORES")
    print("---------------------------------")
    print("1. Añadir Licor")
    print("2. Mostrar Inventario")
    print("3. Mover Licor")
    print("4. Vender/Eliminar Licor")
    print("0. Salir")
    print("---------------------------------")

def add_liquor():
    name = input("Nombre del ítem: ")
    type = input("Categoría: ")
    try:
        amount = int(input("Cantidad: "))
        item = Liquor(name, type, amount)
        inventario.add_liquor(item)
        print(f"{name} ({type}): {amount} unidad(es) añadida(s) con éxito.")
    except ValueError:
        print("Error: La cantidad debe ser un número válido.")

def move_liquor():
    name = input("Nombre del ítem a mover: ")
    try:
        amount = int(input("Cantidad por mover: "))
        inventario.move_liquor(name, amount, caba_salon)
    except ValueError:
        print("Error: La cantidad debe ser un número válido.")

def sell_or_remove_liquor():
    print("\n1. Vender Licor\n2. Eliminar Licor")
    try:
        option = int(input("Seleccione una opción: "))
        name = input("Nombre del ítem: ")
        amount = int(input(f"Cantidad de {name}: "))
        if option == 1:  # Vender
            liquor = inventario.search_liquor(name)
            if liquor:
                liquor.sell(amount)
        elif option == 2:  # Eliminar
            inventario.remove_liquor(name, amount)
        else:
            print("Opción inválida.")
    except ValueError:
        print("Error: La cantidad debe ser un número válido.")

# Bucle principal
while True:
    show_menu()
    try:
        user_option = int(input("Seleccione una opción: "))
        if user_option == 1:
            add_liquor()
        elif user_option == 2:
            inventario.show_stock()
            caba_salon.show_stock()
        elif user_option == 3:
            move_liquor()
        elif user_option == 4:
            sell_or_remove_liquor()
        elif user_option == 0:
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")
    except ValueError:
        print("Por favor, ingrese un número válido.")
