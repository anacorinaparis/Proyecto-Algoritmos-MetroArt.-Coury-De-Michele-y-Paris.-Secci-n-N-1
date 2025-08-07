class Obra:
    def __init__(self, obra_id, title, artist):
        self.obra_id = obra_id
        self.title = title
        self.artist = artist

    def show_resumen(self):
        print(f"\nID: {self.obra_id}")
        print(f"Titulo: {self.title}")
        print(f"Artista: {self.artist}")
