class Obra:
    def __init__(self, obra_id, title, artist, nacionalidad, creacion, nacimiento, muerte, tipo, imagen):
        self.obra_id = obra_id
        self.title = title
        self.artist = artist
        self.nacionalidad = nacionalidad
        self.creacion = creacion
        self.nacimiento = nacimiento
        self.muerte = muerte
        self.tipo = tipo
        self.imagen = imagen

    def show_resumen(self):
        print(f"\nID: {self.obra_id}")
        print(f"Titulo: {self.title}")
        print(f"Artista: {self.artist}")
    
    def show_completo(self):
        print("--- DETALLES COMPLETOS DE LA OBRA ---")
        print(f"Título: {self.title}")
        print(f"Artista: {self.artist}")
        print(f"Nacionalidad del artista: {self.nacionalidad}")
        print(f"Fecha nacimiento artista: {self.nacimiento}")
        print(f"Fecha muerte artista: {self.muerte}")
        print(f"Tipo (clasificación): {self.tipo}")
        print(f"Año de creación: {self.creacion}")
