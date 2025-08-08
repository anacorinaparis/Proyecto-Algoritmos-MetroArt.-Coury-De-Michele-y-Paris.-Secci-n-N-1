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
                print(f"\n--- Obras del Departamento {id_depto} ---")
                for obra in obras:
                    obra.show_resumen()
            else:
                print("\nNo se encontraron obras para este departamento.")

    def obtener_obras_por_departamento(self, department_id):
        url = f"https://collectionapi.metmuseum.org/public/collection/v1/search?departmentId={department_id}&q=*"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            object_ids = response.json().get("objectIDs", [])
            
            obras = []
            batch_size = 20
            continue_loading = True

            for i, obj_id in enumerate(object_ids, 1):
                if not continue_loading:
                    return None
                    
                obra_url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{obj_id}"
                obra_response = requests.get(obra_url, timeout=5)

                if obra_response.status_code == 200:
                    obra_data = obra_response.json()
                    obras.append(Obra(
                        obj_id,
                        obra_data.get("title", "Sin título"),
                        obra_data.get("artistDisplayName", "Artista desconocido"),
                        obra_data.get("artistNationality", "Desconocida"),
                        obra_data.get("objectDate", "Fecha desconocida"),
                        obra_data.get("artistBeginDate", "Fecha desconocida"),
                        obra_data.get("artistEndDate", "Fecha desconocida"),
                        obra_data.get("classification", "Desconocido"),
                        obra_data.get("primaryImage", ""),
                    ))
                
                if i % batch_size == 0:
                    print(f"\n--- Mostrando obras {i-batch_size+1} a {i} ---")
                    for obra in obras[-batch_size:]:
                        obra.show_resumen()

                    opcion = input("""\nSeleccione una opción:
1- Ver más obras
2- Buscar una obra por ID
3- Volver al menú principal
---> """)
                    if opcion == "1":
                        continue_loading = True
                        continue
                    elif opcion == "2":
                        obra_id = input("\nIngrese el ID de la obra que desea ver en detalle: ")
                        self.mostrar_detalle_obra(obra_id)
                        
                        while True:
                            respuesta = input("\n¿Desea continuar viendo más obras? (s/n): ").lower()
                            if respuesta == "n":
                                self.mostrar_departamentos()
                                continue_loading = False
                                break
                            elif respuesta == "s":
                                continue_loading = True
                                break
                            else:
                                print("\nOpción no válida.")
                    elif opcion == "3":
                        continue_loading = False
                        continue
                    else:
                        print("\nOpción inválida, continuando con más obras...")
            return obras
        
        else:
            print(f"\nError al obtener obras. Código: {response.status_code}")
            return []
        
    def mostrar_detalle_obra(self, obra_id):
        obra_url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{obra_id}"
        response = requests.get(obra_url, timeout=5)
    
        if response.status_code == 200:
            obra_data = response.json()
            obra = Obra(0,
                obra_data.get("title", "Sin título"),
                obra_data.get("artistDisplayName", "Artista desconocido"),
                obra_data.get("artistNationality", "Desconocida"),
                obra_data.get("objectDate", "Fecha desconocida"),
                obra_data.get("artistBeginDate", "Fecha desconocida"),
                obra_data.get("artistEndDate", "Fecha desconocida"),
                obra_data.get("classification", "Desconocido"),
                obra_data.get("primaryImage", ""),
            )
            obra.show_completo()
            imagen_url = obra_data.get("primaryImage", "") or obra_data.get("primaryImageSmall", "")
            if imagen_url:
                print(f"\nImagen disponible en: {imagen_url}")
            else:
                print("\nNo hay imagen disponible para esta obra.")
        else:
            print(f"\nError al obtener detalles de la obra. Código: {response.status_code}")
