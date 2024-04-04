class Categoria:
    def __init__(self,cat_nom, cat_description):
        self.cat_nom = cat_nom
        self.cat_description = cat_description


    def __str__(self):
        return f"Nombre Categoria: {self.cat_nom}, Descripcion: {self.cat_description}"