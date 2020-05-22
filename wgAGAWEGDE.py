import os
import arcade
import Objeto_Entrenador
import Objeto_Pokemon
from tests import Combate
from tests.Cambiar_Pokemon import cambiar_pokemon

WIDTH = 800
HEIGHT = 600
SPRITE_SCALING = 0.6
SPRITE_NATIVE_SIZE = 128
SPRITE_SIZE = int(SPRITE_NATIVE_SIZE * SPRITE_SCALING)

VIEWPORT_MARGIN_TOP = 60
VIEWPORT_MARGIN_BOTTOM = 60
VIEWPORT_RIGHT_MARGIN = 270
VIEWPORT_LEFT_MARGIN = 270

MOVEMENT_SPEED = 3


# La clase room es aquella clase que crea los escenarios donde se desplaza el jugador
class Room:
    """
    Esta clase crea y caga las distintas habitaciones del juego
    """

    def __init__(self):
        self.wall_list = None
        self.textura = None


def setup_pueblo():
    """
    Crea la habitación del pueblo
    """
    room = Room()

    # Lista de Sprites
    room.wall_list = arcade.SpriteList()
    room.textura = arcade.SpriteList()

    map = arcade.tilemap.read_tmx("resources" + os.path.sep + "maps" + os.path.sep + "nivel0.tmx")

    carga = arcade.process_layer(map, "Nivel", 1)
    wall = arcade.process_layer(map, "Muros Invisibles", 1)

    room.textura = carga
    room.wall_list = wall

    return room


def setup_room_1():
    """
    Crea la habitacion 1.
    """
    room = Room()

    # Lista de Sprites
    room.wall_list = arcade.SpriteList()
    room.textura = arcade.SpriteList()

    map = arcade.tilemap.read_tmx("resources" + os.path.sep + "maps" + os.path.sep + "nivel1.tmx")

    carga = arcade.process_layer(map, "Nivel", 1)
    wall = arcade.process_layer(map, "Muros Invisibles", 1)

    room.textura = carga
    room.wall_list = wall

    return room


def setup_combate():
    """
    Create la habitación donde ocurriran los combates
    """
    room = Room()

    # Lista de Sprites
    room.wall_list = arcade.SpriteList()
    room.textura = arcade.SpriteList()

    map = arcade.tilemap.read_tmx("resources" + os.path.sep + "maps" + os.path.sep + "combate.tmx")

    carga = arcade.process_layer(map, "Nivel", 1)
    wall = arcade.process_layer(map, "Muros Invisibles", 1)

    room.textura = carga
    room.wall_list = wall

    return room


# Juego
class MyGame(arcade.Window):
    def __init__(self):
        """
        Constructor
        """
        super().__init__(WIDTH, HEIGHT, "Juego", fullscreen=True)

        self.set_mouse_visible(False)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        width, height = self.get_size()

        self.set_viewport(0, width, 0, height)

        self.current_room = 0
        self.rooms = None

        self.textura = None
        self.wall_list = None
        self.player_sprite = None
        self.player_list = None

        self.view_left = 0
        self.view_bottom = 0
        self.physics_engine = None

        # Variables globales para los principales procesos del juego
        self.tienda = False
        self.cambio = False
        self.is_salvaje = False
        self.cuerda_huida = False


    def setup(self):
        """ Set up the game and initialize the variables. """
        # Set up the player
        self.player_list = arcade.SpriteList()
        self.player_sprite = arcade.AnimatedWalkingSprite()

        self.player_sprite.stand_right_textures = []
        self.player_sprite.stand_right_textures.append(arcade.load_texture(
            "resources" + os.path.sep + "sprites" + os.path.sep + "player" + os.path.sep + "Derecha" + os.path.sep + "Der0.png"))

        self.player_sprite.stand_left_textures = []
        self.player_sprite.stand_left_textures.append(
            arcade.load_texture("resources/sprites/player/Izquierda/Izq0.png"))

        # Cargamos las texturas para el movimiento derecho
        self.player_sprite.walk_right_textures = []
        self.player_sprite.walk_right_textures.append(arcade.load_texture(
            "resources" + os.path.sep + "sprites" + os.path.sep + "player" + os.path.sep + "Derecha" + os.path.sep + "Der1.png"))
        self.player_sprite.walk_right_textures.append(arcade.load_texture(
            "resources" + os.path.sep + "sprites" + os.path.sep + "player" + os.path.sep + "Derecha" + os.path.sep + "Der2.png"))
        self.player_sprite.walk_right_textures.append(arcade.load_texture(
            "resources" + os.path.sep + "sprites" + os.path.sep + "player" + os.path.sep + "Derecha" + os.path.sep + "Der3.png"))
        self.player_sprite.walk_right_textures.append(arcade.load_texture(
            "resources" + os.path.sep + "sprites" + os.path.sep + "player" + os.path.sep + "Derecha" + os.path.sep + "Der4.png"))
        self.player_sprite.walk_right_textures.append(arcade.load_texture(
            "resources" + os.path.sep + "sprites" + os.path.sep + "player" + os.path.sep + "Derecha" + os.path.sep + "Der5.png"))
        self.player_sprite.walk_right_textures.append(arcade.load_texture(
            "resources" + os.path.sep + "sprites" + os.path.sep + "player" + os.path.sep + "Derecha" + os.path.sep + "Der6.png"))
        self.player_sprite.walk_right_textures.append(arcade.load_texture(
            "resources" + os.path.sep + "sprites" + os.path.sep + "player" + os.path.sep + "Derecha" + os.path.sep + "Der7.png"))
        self.player_sprite.walk_right_textures.append(arcade.load_texture(
            "resources" + os.path.sep + "sprites" + os.path.sep + "player" + os.path.sep + "Derecha" + os.path.sep + "Der8.png"))

        # Cargamos las texturas para el movimiento  izquierdo
        self.player_sprite.walk_left_textures = []
        self.player_sprite.walk_left_textures.append(arcade.load_texture(
            "resources" + os.path.sep + "sprites" + os.path.sep + "player" + os.path.sep + "Izquierda" + os.path.sep + "Izq1.png"))
        self.player_sprite.walk_left_textures.append(arcade.load_texture(
            "resources" + os.path.sep + "sprites" + os.path.sep + "player" + os.path.sep + "Izquierda" + os.path.sep + "Izq2.png"))
        self.player_sprite.walk_left_textures.append(arcade.load_texture(
            "resources" + os.path.sep + "sprites" + os.path.sep + "player" + os.path.sep + "Izquierda" + os.path.sep + "Izq3.png"))
        self.player_sprite.walk_left_textures.append(arcade.load_texture(
            "resources" + os.path.sep + "sprites" + os.path.sep + "player" + os.path.sep + "Izquierda" + os.path.sep + "Izq4.png"))
        self.player_sprite.walk_left_textures.append(arcade.load_texture(
            "resources" + os.path.sep + "sprites" + os.path.sep + "player" + os.path.sep + "Izquierda" + os.path.sep + "Izq5.png"))
        self.player_sprite.walk_left_textures.append(arcade.load_texture(
            "resources" + os.path.sep + "sprites" + os.path.sep + "player" + os.path.sep + "Izquierda" + os.path.sep + "Izq6.png"))
        self.player_sprite.walk_left_textures.append(arcade.load_texture(
            "resources" + os.path.sep + "sprites" + os.path.sep + "player" + os.path.sep + "Izquierda" + os.path.sep + "Izq7.png"))
        self.player_sprite.walk_left_textures.append(arcade.load_texture(
            "resources" + os.path.sep + "sprites" + os.path.sep + "player" + os.path.sep + "Izquierda" + os.path.sep + "Izq8.png"))

        # Cargamos las texturas para el movimiento abajo
        self.player_sprite.walk_down_textures = []
        self.player_sprite.walk_down_textures.append(arcade.load_texture(
            "resources" + os.path.sep + "sprites" + os.path.sep + "player" + os.path.sep + "Abajo" + os.path.sep + "Abj0.png"))
        self.player_sprite.walk_down_textures.append(arcade.load_texture(
            "resources" + os.path.sep + "sprites" + os.path.sep + "player" + os.path.sep + "Abajo" + os.path.sep + "Abj1.png"))
        self.player_sprite.walk_down_textures.append(arcade.load_texture(
            "resources" + os.path.sep + "sprites" + os.path.sep + "player" + os.path.sep + "Abajo" + os.path.sep + "Abj2.png"))
        self.player_sprite.walk_down_textures.append(arcade.load_texture(
            "resources" + os.path.sep + "sprites" + os.path.sep + "player" + os.path.sep + "Abajo" + os.path.sep + "Abj3.png"))
        self.player_sprite.walk_down_textures.append(arcade.load_texture(
            "resources" + os.path.sep + "sprites" + os.path.sep + "player" + os.path.sep + "Abajo" + os.path.sep + "Abj4.png"))
        self.player_sprite.walk_down_textures.append(arcade.load_texture(
            "resources" + os.path.sep + "sprites" + os.path.sep + "player" + os.path.sep + "Abajo" + os.path.sep + "Abj5.png"))
        self.player_sprite.walk_down_textures.append(arcade.load_texture(
            "resources" + os.path.sep + "sprites" + os.path.sep + "player" + os.path.sep + "Abajo" + os.path.sep + "Abj6.png"))
        self.player_sprite.walk_down_textures.append(arcade.load_texture(
            "resources" + os.path.sep + "sprites" + os.path.sep + "player" + os.path.sep + "Abajo" + os.path.sep + "Abj7.png"))
        self.player_sprite.walk_down_textures.append(arcade.load_texture(
            "resources" + os.path.sep + "sprites" + os.path.sep + "player" + os.path.sep + "Abajo" + os.path.sep + "Abj8.png"))

        # Cargamos las texturas para el movimiento de arriba
        self.player_sprite.walk_up_textures = []
        self.player_sprite.walk_up_textures.append(arcade.load_texture(
            "resources" + os.path.sep + "sprites" + os.path.sep + "player" + os.path.sep + "Arriba" + os.path.sep + "Arr0.png"))
        self.player_sprite.walk_up_textures.append(arcade.load_texture(
            "resources" + os.path.sep + "sprites" + os.path.sep + "player" + os.path.sep + "Arriba" + os.path.sep + "Arr1.png"))
        self.player_sprite.walk_up_textures.append(arcade.load_texture(
            "resources" + os.path.sep + "sprites" + os.path.sep + "player" + os.path.sep + "Arriba" + os.path.sep + "Arr2.png"))
        self.player_sprite.walk_up_textures.append(arcade.load_texture(
            "resources" + os.path.sep + "sprites" + os.path.sep + "player" + os.path.sep + "Arriba/Arr3.png"))
        self.player_sprite.walk_up_textures.append(arcade.load_texture(
            "resources" + os.path.sep + "sprites" + os.path.sep + "player" + os.path.sep + "Arriba" + os.path.sep + "Arr4.png"))
        self.player_sprite.walk_up_textures.append(arcade.load_texture(
            "resources" + os.path.sep + "sprites" + os.path.sep + "player" + os.path.sep + "Arriba" + os.path.sep + "Arr5.png"))
        self.player_sprite.walk_up_textures.append(arcade.load_texture(
            "resources" + os.path.sep + "sprites" + os.path.sep + "player" + os.path.sep + "Arriba" + os.path.sep + "Arr6.png"))
        self.player_sprite.walk_up_textures.append(arcade.load_texture(
            "resources" + os.path.sep + "sprites" + os.path.sep + "player" + os.path.sep + "Arriba" + os.path.sep + "Arr7.png"))
        self.player_sprite.walk_up_textures.append(arcade.load_texture(
            "resources" + os.path.sep + "sprites" + os.path.sep + "player" + os.path.sep + "Arriba" + os.path.sep + "Arr8.png"))

        # Posición de inicio del jugador
        self.player_sprite.center_x = 85
        self.player_sprite.center_y = 537.5

        self.player_list.append(self.player_sprite)

        #Sistema de habitaciones
        self.has_perdido = False
        self.has_ganado = False

        self.top_rooom = 1
        self.current_room = 0
        self.rooms = []

        room = setup_pueblo()
        self.rooms.append(room)
        room = setup_room_1()
        self.rooms.append(room)
        room = setup_combate()
        self.rooms.append(room)
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.rooms[self.current_room].wall_list)

        ###################Registro de fakemon################################
        prueba1 = Objeto_Pokemon.Pokemon("prueba1","estelar",30,20,3,200,200,"")
        prueba2 = Objeto_Pokemon.Pokemon("prueba2","estelar",30,20,200,200,200,"")

        ###################Registro de entrenadores################################
        self.jugador = Objeto_Entrenador.Entrenador("jugador")
        self.jugador.lista_equipo.append(prueba1)


        #Establecemos dos variables globales para el combate
        self.current_enemy = prueba2
        self.current_ally = self.jugador.lista_equipo[0]



    # Esta funcion recibe el texto dentro de los sprites y dibuja el cuadro de texto
    def genera_texto(self, text):

        arcade.draw_lrwh_rectangle_textured(self.view_left, self.player_sprite.center_y / 5.15, WIDTH, HEIGHT / 2,
                                            arcade.load_texture(
                                                "resources" + os.path.sep + "sprites" + os.path.sep + "messages" + os.path.sep + text))

    def on_draw(self):

        arcade.start_render()
        self.rooms[self.current_room].textura.draw()
        self.rooms[self.current_room].wall_list.draw()
        self.player_list.draw()

        # Cuadros de texto correspondientes al pueblo
        if (self.current_room == 0 and self.player_sprite.center_x == 471 and self.player_sprite.center_y == 681.5):
            self.genera_texto("cuadrado.png")
        if (self.current_room == 0 and self.player_sprite.center_x == 745 and self.player_sprite.center_y == 649.5):
            self.genera_texto("cuadrado.png")

        arcade.draw_text("Nombre Pokemon1 + LVL", 534, 253, arcade.color.BLACK, 12)
        arcade.draw_text("HP Pokemon1", 534, 223, arcade.color.BLACK, 12)
        arcade.draw_text("Nombre Pokemon1", 300, 530, arcade.color.BLACK, 12)
        arcade.draw_text("HP Pokemon2", 300, 510, arcade.color.BLACK, 12)

        # Mapa de coordenadas utilizado para saber la dirección
        arcade.draw_text("Coordenada x:" + str(self.player_sprite.center_x), self.player_sprite.center_x + 10,
                         self.player_sprite.center_y, arcade.color.WHITE)
        arcade.draw_text("Coordenada y:" + str(self.player_sprite.center_y), self.player_sprite.center_x + 10,
                         self.player_sprite.center_y - 10, arcade.color.WHITE)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.player_sprite.change_y = MOVEMENT_SPEED
        if key == arcade.key.A:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        if key == arcade.key.S:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        if key == arcade.key.D:
            self.player_sprite.change_x = MOVEMENT_SPEED

        if key == arcade.key.F:
            self.set_fullscreen(not self.fullscreen)

            width, height = self.get_size()
            self.set_viewport(0, width, 0, height)

        # ERROR
        if (self.current_room == 2 ):
            if key == arcade.key.KEY_1:

                self.room_victoria = self.current_room
                self.x_victoria = self.player_sprite.center_x
                self.y_victoria = self.player_sprite.center_y


                Combate.atacar(self.current_enemy,self.current_ally)
                print("Aliado ataca enemigo")
                print("HP enemigo:"+ str(self.current_enemy.HP))
                print("HP aliado:" + str(self.current_ally.HP))
                self.has_perdido, self.has_ganado = Combate.checkeo(self.jugador, self.current_ally,self.current_enemy)


            if key == arcade.key.KEY_2:      pass
            if key == arcade.key.KEY_3:      pass

            if key == arcade.key.KEY_4:      pass
        # ERROR
        if (self.combate == True and self.cambio == True):
            if key == arcade.key.KEY_1:
                cambiar_pokemon(self.jugador, 1)
                self.cambio = False
            if key == arcade.key.KEY_2:
                cambiar_pokemon(self.jugador, 2)
                self.cambio = False
            if key == arcade.key.KEY_3:
                cambiar_pokemon(self.jugador, 3)
                self.cambio = False
            if key == arcade.key.KEY_4:
                cambiar_pokemon(self.jugador, 4)
                self.cambio = False
        # ERROR Falta meter los mensajes para cuando no hay dinero y se ha comprado un producto
        if (self.tienda == True):
            if key == arcade.key.KEY_1 and self.jugador.dinero <50 :
                self.jugador.restar_dinero(50)
                self.jugador.inventario["Poción"] += 1
            if key == arcade.key.KEY_2 and self.jugador.dinero <50:
                self.jugador.restar_dinero(50)
                self.jugador.inventario["Cuerda huida"] += 1

        if key == arcade.key.Q and self.current_room != 0 and self.jugador.inventario["Cuerda Huida"] != 0:
            self.cuerda_huida = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W or key == arcade.key.S:
            self.player_sprite.change_y = 0

        elif key == arcade.key.A or key == arcade.key.D:
            self.player_sprite.change_x = 0




    def on_update(self, delta_time):
        # Call update on all sprites (The sprites don't do much in this example though.)
        self.player_list.update()
        self.player_list.update_animation()
        self.physics_engine.update()

        #Volver si has ganado
        if self.has_ganado:

            self.current_room = self.room_victoria
            self.player_sprite.center_x = self.x_victoria
            self.player_sprite.center_y = self.y_victoria
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.has_ganado = False


        #Volver al inicio
        if self.has_perdido:

            self.current_room = 0
            self.player_sprite.center_x = 840
            self.player_sprite.center_y = 120
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.has_perdido = False

        # Sistema para comprobar el mayor de los pisos y cambiar al piso donde se encontraba el jugador cuando sale de la torre
        if (self.current_room > self.top_rooom and self.current_room != 10):
            self.top_rooom = self.current_room
        # Carga el piso donde se encontraba el jugador por ultima vez
        if (self.current_room == 0 and self.player_sprite.center_x == 843 and self.player_sprite.center_y == 137.5):
            self.current_room = self.top_rooom
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = 165
            self.player_sprite.center_y = 465

        # Carga el piso del pueblo al salir del primer piso
        if (self.current_room == 1 and self.player_sprite.center_x == 169 and self.player_sprite.center_y == 470.5):
            self.current_room = 0
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = 840
            self.player_sprite.center_y = 120



        # Prueba combate
        if (self.current_room == 1 and self.player_sprite.center_x == 873 and self.player_sprite.center_y == 425.5):
            self.current_room = 2
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = 300
            self.player_sprite.center_y = 55
            self.player_sprite.center_x = 400
            self.player_sprite.center_y = 55





        # Sistema para regresar al pueblo con cuerda huida
        if (self.cuerda_huida):
            self.jugador.inventario["Cuerda Huida"] -= 1
            self.cuerda_huida = False
            self.current_room = 0
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = 70
            self.player_sprite.center_y = 537.5

        #Sistema de tiendas
        if (self.current_room == 0 and self.player_sprite.center_x == 745 and self.player_sprite.center_y == 649.5):
            self.tienda = True

        # Sistema para restaurar HP de todos los fakemon
        if (self.current_room == 0 and self.player_sprite.center_x == 471 and self.player_sprite.center_y == 681.5):
            if self.top_rooom == 1:
                self.jugador.lista_equipo[0].sumar_HP(999999)
            elif self.top_rooom == 2:
                for i in range(0, 1):
                    self.jugador.lista_equipo[i].sumar_HP(999999)
            elif self.top_rooom == 3:
                for i in range(0, 2):
                    self.jugador.lista_equipo[i].sumar_HP(999999)
            elif self.top_rooom == 4:
                for i in range(0, 3):
                    self.jugador.lista_equipo[i].sumar_HP(999999)
            elif self.top_rooom == 5:
                for i in range(0, 4):
                    self.jugador.lista_equipo[i].sumar_HP(999999)
            elif self.top_rooom == 6:
                for i in range(0, 5):
                    self.jugador.lista_equipo[i].sumar_HP(999999)
            elif self.top_rooom == 7:
                for i in range(0, 6):
                    self.jugador.lista_equipo[i].sumar_HP(999999)


        # Sistema de camara para jugador
        changed = False
        # Scroll left
        left_bndry = self.view_left + VIEWPORT_LEFT_MARGIN
        if self.player_sprite.left < left_bndry:
            self.view_left -= left_bndry - self.player_sprite.left
            changed = True

        # Scroll right
        right_bndry = self.view_left + WIDTH - VIEWPORT_RIGHT_MARGIN
        if self.player_sprite.right > right_bndry:
            self.view_left += self.player_sprite.right - right_bndry
            changed = True

        # Scroll up
        top_bndry = self.view_bottom + HEIGHT - VIEWPORT_MARGIN_TOP
        if self.player_sprite.top > top_bndry:
            self.view_bottom += self.player_sprite.top - top_bndry
            changed = True

        # Scroll down
        bottom_bndry = self.view_bottom + VIEWPORT_MARGIN_BOTTOM
        if self.player_sprite.bottom < bottom_bndry:
            self.view_bottom -= bottom_bndry - self.player_sprite.bottom
            changed = True

        # If we need to scroll, go ahead and do it.
        if changed:
            self.view_left = int(self.view_left)
            self.view_bottom = int(self.view_bottom)
            arcade.set_viewport(self.view_left,
                                WIDTH + self.view_left,
                                self.view_bottom,
                                HEIGHT + self.view_bottom)













































def main():
    window = MyGame()
    window.setup()
    arcade.run()


main()
