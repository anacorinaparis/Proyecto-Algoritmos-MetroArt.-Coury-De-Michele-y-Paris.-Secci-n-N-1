import requests
import time
from Departamento import Departamento
from Obra import Obra

class Museo:
    def __init__(self):
        self.departamentos = []

    def start(self):
        self.cargar_departamentos()

        while True:
            menu = input("""\nBienvenido al Museo MetroArt.
--- MENÚ PRINCIPAL ---
1- Ver lista de obras por departamento
2- Ver lista de obras por nacionalidad del autor
3- Ver lista de obras por nombre del autor
4- Salir 
---> """)
            if menu == "1":
                self.mostrar_departamentos()
            elif menu == "2":
                None
            elif menu == "3":
                None
            elif menu == "4":
                print("Gracias por visitar el Museo MetroArt.")
                break
            else:
                print("Opción invalida, intentelo de nuevo.")

    def cargar_departamentos(self):
        url = "https://collectionapi.metmuseum.org/public/collection/v1/departments"
        response = requests.get(url)
        if response.status_code == 200:
            datos = response.json()
            for depto in datos["departments"]:
                self.departamentos.append(Departamento(depto["departmentId"], depto["displayName"]))
        else:
            print(f"Error al cargar departamentos. Código de estado: {response.status_code}")

    def mostrar_departamentos(self):
        print("\n--- Departamentos del Museo ---")
        for departamento in self.departamentos:
            departamento.show()
        
        while True:
            id_depto = input("\nIngrese el ID de un departemento para ver sus obras o '0' para volver al menú principal: ")
                
            if id_depto == "0":
                break

            if not id_depto.isdigit() or not any(depto.department_id == int(id_depto) for depto in self.departamentos):
                print("ID invalido. Ingrese uno. de los IDs mostrados")
                continue

            obras = self.obtener_obras_por_departamento(id_depto)
            if obras is None:
                return
            elif obras:
                print(f"\n--- OBRAS DEL DEPARTAMENTO {id_depto} ---")
                for obra in obras:
                    obra.show()
            else:
                print("No se encontraron obras para este departamento.")
