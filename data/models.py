class Libro():
    def __init__(self,id, titulo, autor, genero, disponible: bool = True):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.genero = genero
        self.disponible = disponible