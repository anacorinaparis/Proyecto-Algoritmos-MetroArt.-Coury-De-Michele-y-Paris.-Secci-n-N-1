import requests
import time
from Departamento import Departamento
from Obra import Obra
import pandas as pandas

class Museo:
    def __init__(self):
        self.departamentos = []

    def start(self):
        self.cargar_departamentos()

        while True:
            menu = input("""\n¡Bienvenido al Museo MetroArt! Ingrese una opción:
            
--- MENÚ PRINCIPAL ---
1- Ver lista de obras por departamento
2- Ver lista de obras por nacionalidad del autor
3- Ver lista de obras por nombre del autor
4- Salir 

---> """)
            
            if menu == "1":
                self.mostrar_departamentos()
            elif menu == "2":
                print()
                self.mostrar_nacionalidades()
                print()
            elif menu == "3":
                self.buscar_obras_por_artista()
            elif menu == "4":
                print()
                print("¡Gracias por visitar el Museo MetroArt!")
                break
            else:
                print()
                print("Opción invalida, inténtelo de nuevo.")

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
        print("\n--- DEPARTAMENTOS DEL MUSEO ---")
        print()
        for departamento in self.departamentos:
            departamento.show()
        
        while True:
            id_depto = input("\nIngrese el ID de un departemento para ver sus obras o '0' para volver al menú principal: ")
                
            if id_depto == "0":
                break

            if not id_depto.isdigit() or not any(depto.department_id == int(id_depto) for depto in self.departamentos):
                print("ID inválido. Ingrese uno de los IDs mostrados")
                continue

            obras = self.obtener_obras_por_departamento(id_depto)
            if obras is None:
                return
            elif obras:
                print(f"\n--- ORRAS DEL DEPARTAMENTO {id_depto} ---")
                for obra in obras:
                    obra.show_resumen()
            else:
                print("\nNo se encontraron obras para este departamento.")

    def obtener_obras_por_departamento(self, department_id):
        url = f"https://collectionapi.metmuseum.org/public/collection/v1/search?departmentId={department_id}&q=*"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            id_obras = response.json().get("objectIDs", [])
            obras = []
            lote = 20
            cargando = True

            for i, id_obra in enumerate(id_obras, 1):
                if not cargando:
                    return None
                    
                obra_url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{id_obra}"
                obra_response = requests.get(obra_url, timeout=5)

                if obra_response.status_code == 200:
                    info_obra = obra_response.json()
                    obras.append(Obra(
                        id_obra,
                        info_obra.get("title", "Sin título"),
                        info_obra.get("artistDisplayName", "Artista desconocido"),
                        info_obra.get("artistNationality", "Desconocida"),
                        info_obra.get("objectDate", "Fecha desconocida"),
                        info_obra.get("artistBeginDate", "Fecha desconocida"),
                        info_obra.get("artistEndDate", "Fecha desconocida"),
                        info_obra.get("classification", "Desconocido"),
                        info_obra.get("primaryImage", ""),
                    ))
                
                if i % lote == 0:
                    print(f"\n--- Mostrando obras {i-lote+1} a {i} ---")
                    for obra in obras[-lote:]:
                        obra.show_resumen()

                    
                    while True:
                        opcion = input("""\nSeleccione una opción:
    1- Ver más obras
    2- Buscar una obra por ID
    3- Volver al menú principal
    ---> """)
                        
                        if opcion == "1":
                            break
                            
                        elif opcion == "2":
                            obra_id = input("\nIngrese el ID de la obra que desea ver en detalle: ")
                            self.mostrar_detalle_obra(obra_id)
                            respuesta = input("\n¿Desea continuar viendo más obras? (s/n): ").lower()
                            
                            if respuesta == "n":
                                self.mostrar_departamentos()
                                cargando = False
                                break
                            elif respuesta == "s":
                                break
                            else:
                                print("\nOpción inválida.")
                                    
                        elif opcion == "3":
                            cargando = False
                            break
                            
                        else:
                            print("\nOpción inválida. Intente de nuevo")
                            print()
                            continue
            return obras
        
        else:
            print(f"\nError al obtener obras. Código: {response.status_code}")
            return []
        
    def mostrar_detalle_obra(self, obra_id):
        obra_url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{obra_id}"
        response = requests.get(obra_url, timeout=5)
    
        if response.status_code == 200:
            obra_data = response.json()
            obra = Obra(
                obra_id,
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

    def mostrar_nacionalidades(self):
        nacionalidades_archivo = pandas.read_csv("CH_Nationality_List_20171130_v1.csv")
        self.nacionalidades = []
        print("--- LISTA DE NACIONALIDADES DE AUTORES ---")
        print()

        for nacionalidad in nacionalidades_archivo["Nationality"]:
            self.nacionalidades.append(nacionalidad)
   
        for indice,nacionalidad in enumerate(self.nacionalidades, 1):
            print(f"{indice}- {nacionalidad}")

        while True:

            seleccion_nacionalidad = input("\nIngrese el núsmero de la nacionalidad de la cual desea ver obras, o '0' para volver al menú principal: ")
            nacionalidad_escogida = None

            if seleccion_nacionalidad == "0":
                break
            
            if not seleccion_nacionalidad.isnumeric():
                print("Ingreso inválido, intente de nuevo.")
                continue
            
            posicion = int(seleccion_nacionalidad) - 1
            if posicion < 0 or posicion >= len(self.nacionalidades):
                print("\nNúmero inválido, intente de nuevo.")
                continue
            else:  
                nacionalidad_escogida = self.nacionalidades[posicion]
                print(f"\nBuscando obras de artistas de nacionalidad '{nacionalidad_escogida}'...")

            obras_nac = self.obtener_obras_por_nacionalidad(nacionalidad_escogida)
            if obras_nac is None:
                return
            elif obras_nac:
                for obra in obras_nac:
                    obra.show_resumen()
            else:
                print("No se encontraron obras")


    def obtener_obras_por_nacionalidad(self, artist_nationality):
        url = f"https://collectionapi.metmuseum.org/public/collection/v1/search?artistNationality={artist_nationality}&q=*"
        response = requests.get(url, timeout=15)

        if response.status_code == 200:
            id_obras = response.json().get("objectIDs", [])
            
            obras = []
            lote = 20
            cargando = True

            for i, id_obra in enumerate(id_obras, 1):
                if not cargando:
                    return None
                    
                obra_url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{id_obra}"
                obra_response = requests.get(obra_url, timeout=5)

                if obra_response.status_code == 200:
                    info_obra = obra_response.json()
                    obras.append(Obra(
                        id_obra,
                        info_obra.get("title", "Sin título"),
                        info_obra.get("artistDisplayName", "Artista desconocido"),
                        info_obra.get("artistNationality", "Desconocida"),
                        info_obra.get("objectDate", "Fecha desconocida"),
                        info_obra.get("artistBeginDate", "Fecha desconocida"),
                        info_obra.get("artistEndDate", "Fecha desconocida"),
                        info_obra.get("classification", "Desconocido"),
                        info_obra.get("primaryImage", ""),
                    ))
                
                if i % lote == 0:
                    print(f"\n--- Mostrando obras {i-lote+1} a {i} ---")
                    for obra in obras[-lote:]:
                        obra.show_resumen()

                    while True:
                        opcion = input("""\nSeleccione una opción:
    1- Ver más obras
    2- Buscar una obra por ID
    3- Volver al menú principal
    ---> """)
                        
                        if opcion == "1":
                            break
                            
                        elif opcion == "2":
                            obra_id = input("\nIngrese el ID de la obra que desea ver en detalle: ")
                            self.mostrar_detalle_obra(obra_id)
                            respuesta = input("\n¿Desea continuar viendo más obras? (s/n): ").lower()
                            
                            if respuesta == "n":
                                cargando = False
                                break
                            elif respuesta == "s":
                                break
                            else:
                                print("\nOpción inválida.")
                                    
                        elif opcion == "3":
                            cargando = False
                            break
                            
                        else:
                            print("\nOpción inválida. Intente de nuevo")
                            print()
                            continue
            return obras
        
        else:
            print(f"\nError al obtener obras. Código: {response.status_code}")
            return []


    def buscar_obras_por_artista(self):
        artista = input("\nIngrese el nombre del artista: ").strip()

        if not artista:
            print("Nombre de artista inválido")
            return

        obras = self.obtener_obras_por_artista(artista)
        if obras is None:
            return
        elif obras:
            print(f"\n--- OBRAS DE {artista.upper()} ---")
            self.mostrar_obras_por_lotes(obras)
        else:
            print(f"No se encontraron obras para el artista '{artista}'")



    def obtener_obras_por_artista(self, artista):
        url = f"https://collectionapi.metmuseum.org/public/collection/v1/search?artistOrCulture=true&q={artista}"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            id_obras = data.get("objectIDs", []) or []
            obras = []
            lote = 20
            cargando = True
            if not id_obras: 
                return []

            for i, id_obra in enumerate(id_obras, 1):
                if not cargando:
                    return None
                
                obra_url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{id_obra}"
                obra_response = requests.get(obra_url, timeout=5)

                if obra_response.status_code == 200:
                    info_obra = obra_response.json()
                    artist_name = info_obra.get("artistDisplayName", "").lower()
                    if artist_name and artista.lower() in artist_name:
                        obras.append(Obra(
                        id_obra,
                        info_obra.get("title", "Sin título"),
                        info_obra.get("artistDisplayName", "Artista desconocido"),
                        info_obra.get("artistNationality", "Desconocida"),
                        info_obra.get("objectDate", "Fecha desconocida"),
                        info_obra.get("artistBeginDate", "Fecha desconocida"),
                        info_obra.get("artistEndDate", "Fecha desconocida"),
                        info_obra.get("classification", "Desconocido"),
                        info_obra.get("primaryImage", ""),
                    ))


                if i % lote == 0:
                    print(f"\n--- Mostrando obras {i-lote+1} a {i} ---")
                    for obra in obras[-lote:]:
                        obra.show_resumen()

                    while True:
                        opcion = input("""\nSeleccione una opción:
    1- Ver más obras
    2- Buscar una obra por ID
    3- Volver al menú principal
    ---> """)
                        
                        if opcion == "1":
                            break
                        
                        elif opcion == "2":
                            obra_id = input("\nIngrese el ID de la obra que desea ver en detalle: ")
                            self.mostrar_detalle_obra(obra_id)
                            respuesta = input("\n¿Desea continuar viendo más obras? (s/n): ").lower()

                            if respuesta == "n":
                                cargando = False
                                break
                            elif respuesta == "s":
                                break
                            else:
                                print("\nOpción no válida.")

                        elif opcion == "3":
                            cargando = False
                            break
                        else:
                            print("\nOpción inválida. Intente de nuevo.")
                            print()
                            continue
            return obras
        
        else:
            print(f"\nError al obtener obras. Código: {response.status_code}")
            return []
