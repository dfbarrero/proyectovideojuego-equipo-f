

class Entrenador:
    """
    Clase entrenador usada para el propio jugador y los entrenadores enemigos. Los enemigos solo usarán las listas fakemon
    """


    def __init__(self, nombre):
        """
        Constructor de la clase Entrenador
        :param nombre: nombre del entrenador o jugador
        """
        # String
        self.nombre = nombre
        # Int
        self.dinero = 200
        # Diccionario String-->Int
        self.inventario = {'Pocion':1,'Cuerda Huida':1}
        # Lista de objetos Pokemon
        self.lista_equipo = []
        self.lista_muertos = []
        self.no_derrotado = True # Variable usada unicamente en entrenadores enemigos para comprobar si han sido derrotados


    def restar_dinero(self, cantidad):
        """
        Resta dinero del jugador al realizar una compra
        :param cantidad: cantidad de dinero a retirar
        """
        self.dinero -= cantidad
        if self.dinero <= 0: self.dinero = 0 # Evita tener dinero negativo
