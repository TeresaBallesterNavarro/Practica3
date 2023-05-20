"""
JUEGO SNAKE: Hay 2 serpientes que luchan por comer una manzana, aquella serpiente
            que coma más manzanas, gana. 
    CLASES
    -------
    - Manzana
        - Posición (aleatoria dentro del tablero (no bordes) y no puede coincidir con la pos de snake)
        - Generar posiciones random
    - Snake (player)
        - Posición
        - Tamaño
        - Método para agrandar su tamaño
        - Método para su movimiento (arriba, abajo, izq, dcha con CONDICIONES)
    - Game
        - Manzana
        - Snakes
        - Contador de puntos
        - Límite de tiempo para FIN del juego
        - Métodos para mover a Snake
        - Método para agrandar el tamaño de Snake
        - Método para generar la posición aleatoria de Manzana
        
    - Display --> para representar por pantalla el juego
    
"""
from multiprocessing.connection import Client
import traceback
import pygame
from pygame.locals import *
import sys
import time
from multiprocessing import Value


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0,255,0)
YELLOW = (255,255,0)

BLACK_SNAKE = 0
BLUE_SNAKE = 1
SNAKE_WIDTH = 50
SNAKE_HEIGHT = 50
SNAKES_COLORS = [BLACK, BLUE]
SNAKES_IMAGES = ['snake_black.png','snake_blue.png']

APPLE_COLOR = RED
APPLE_SIZE = 50
SIZE = (800,650)
X = 0
Y = 1  
FPS = 60

class Snake(): #[[x1,y1],[x2,y2],[x3,y3]...] = Snake

    def __init__(self, color): #El color diferencia al jugador 1 del 2
        self.head = [None, None] #Posición de la cabeza
        self.color = color # 0 = BLACK, 1 = BLUE
        self.direction = None #Indica hacia donde se dirige
    
    def get_color(self):
        return self.color
    
    def get_pos_head(self):
        return self.head
    
    def set_pos_head(self,head): #Cambia la posición de snake
        self.head = head
        
    def get_direction(self): #obtener dirección 
        return self.direction
    
    def set_direction(self, direction):
        self.direction = direction    

    def __str__(self):
        return f"S<{self.color, self.head}>"   
        
    
class Apple(): #Representa la manzana en el juego

    def __init__(self): #La manzana tiene color y posición
        self.pos = [None, None]
    
    def get_pos(self):
        return self.pos
    
    def set_pos(self,pos): #cambia la posición de la manzana
        self.pos = pos

def __str__(self):
        return f"A<{self.pos}>"


class Game(): #Representamos el estado del juego

    def __init__(self):
        self.snakes = [Snake(i) for i in range(2)] #Snake(0) -> BLACK_SNAKE, Snake(1) -> BLUE_SNAKE
        self.apple = Apple()
        self.score = [0,0]
        self.game_over = 0 # 0 = no hay game over
        self.running = True
        
    def get_snake(self, color):
    	return self.snakes[color]
    

    def get_apple(self):
    	return self.apple 
        
    def get_pos_snake(self, color): #color = 0 -> BLACK, color = 1 -> BLUE
        return self.snakes[color].get_pos_head()

    def set_pos_snake(self, color, head): #Cambia la posición de snake
        self.snakes[color].set_pos_head(head)
    
    def get_snake_direction(self, color):
        self.snakes[color].get_direction
        
    def set_snake_direction(self, color, direction):
    	self.snakes[color].set_direction(direction)

    def get_pos_apple(self):
        return self.apple.get_pos()
    
    def set_pos_apple(self, pos): #Cambia la posición de apple
        self.apple.set_pos(pos)

    def get_score(self):
        return self.score
    
    def set_score(self, score):
        self.score = score

    def get_game_over(self):
        return self.game_over
    
    def set_game_over(self, i): #Cambia el estado de game over: 0 = No hay game over. 1 = Gana BLACK snake. 2 = Gana snake BLUE. 3 = Posible empate.
        self.game_over = i

    def update(self,gameinfo): #  Actualiza la información del juego recibida en gameinfo
    
        self.set_pos_snake(0, gameinfo['pos_black_snake']) #he cambiado BLACK_SNAKE Y BLUE_SNAKE por 0 y 1 porque los jugadores estan guardados en una lista
        self.set_pos_snake(1, gameinfo['pos_blue_snake'])
        self.set_pos_apple(gameinfo['pos_apple'])
        self.set_score(gameinfo['score'])
        self.game_over = gameinfo['game_over']
        self.running = gameinfo['is_running']
        
    def is_running(self):
        return self.running
    
    def stop(self):
        self.running = False

    def __str__(self):
        return f"G<{self.snakes[0]}:{self.snakes[1]}:{self.apple}>"
    
class SnakeSprite(pygame.sprite.Sprite): #Representa las snakes por pantalla

    def __init__(self, snake):
      super().__init__()
      self.snake = snake
      if self.snake.get_color() == BLACK_SNAKE :
    	  self.image = pygame.image.load(SNAKES_IMAGES[0])
      elif self.snake.get_color() == BLUE_SNAKE :
          self.image = pygame.image.load(SNAKES_IMAGES[1])

      self.rect = self.image.get_rect()
      self.update()

    def update(self):
        pos = self.snake.get_pos_head()
        self.rect.centerx, self.rect.centery = pos

    def __str__(self):
        return f"S<{self.snake}>"
    
class AppleSprite(pygame.sprite.Sprite): #Representa la manzana por pantalla

    def __init__(self, apple):
        super().__init__()
        self.apple= apple
        self.image = pygame.image.load('apple.png')
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.update()

    def update(self): #Nueva posicion de la manzana
        pos = self.apple.get_pos()
        self.rect.centerx, self.rect.centery = pos
        
        
class Display(): #Representa el juego por pantalla

    def __init__(self, game):
        self.game = game 
        self.apple = AppleSprite(self.game.get_apple())
        self.snakes = [SnakeSprite(self.game.get_snake(i)) for i in range(2)] 
        #Tenemos varios objetos sprite, los agrupamos en la clase Group para administrarlos juntos:
        self.all_sprites = pygame.sprite.Group()
        for snake in self.snakes:
            self.all_sprites.add(snake)
        self.all_sprites.add(self.apple)

        self.screen = pygame.display.set_mode(SIZE) #Crea la ventana del juego con el tamanyo predefinido SIZE
        
        self.clock =  pygame.time.Clock()  #FPS
        self.background = pygame.image.load('fondo2.png') #Carga la imagen de fondo
        self.inicio = pygame.image.load('inicio_snake.png') #Carga la imagen de fondo

        pygame.init() #Inicializamos todos los módulos pygame

    def analyze_events(self, color):
        events = []
        
        for event in pygame.event.get():
            
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_ESCAPE: #Esc keyboard
                    events.append("quit")
                elif event.key == pygame.K_UP : #si me estoy moviendo hacia abajo y quiero ir hacia arriba no puedo
                    events.append("up")
                elif event.key == pygame.K_DOWN : #si me estoy moviendo hacia arriba y quiero ir hacia abajo no puedo
                    events.append("down")
                elif event.key == pygame.K_RIGHT : #si me estoy moviendo hacia la derecha y quiero ir hacia la izquierda no puedo
                    events.append("right")
                elif event.key == pygame.K_LEFT : #si me estoy moviendo hacia derecha y quiero ir hacia la izquierda no puedo
                    events.append("left")
                   
            elif event.type == pygame.QUIT: #Verifica si el evento es 'cerrar' la ventana
                events.append("quit")
                
        if pygame.sprite.collide_rect(self.apple, self.snakes[color]): #Verifica si la manzana y alguna snake colisionan
            events.append("collide")
 
        return events


    def finDelJuego(self, i , pantalla): #Para mostrar la pantalla cuando hay game_over
    
       # Obtengo las dimensiones de la pantalla
        pantalla_width = pantalla.get_width()
        pantalla_height = pantalla.get_height()
        
        self.screen.blit(self.background, (0, 0)) #Ponemos un fondo 
        letra = pygame.font.SysFont('times new roman', 50)
    
        #Veamos los casos de game_over y en cada uno mostraremos una cosa por pantalla:
        if i == 1: #Gana BLACK snake
            winner_text = letra.render("GAME OVER: Black snake ha ganado!", True, BLACK)
            winner_rect = winner_text.get_rect()
            winner_rect.midtop = (pantalla_width//2, pantalla_height//2)
            pantalla.blit(winner_text, winner_rect) 
        elif i == 2: #Gana BLUE snake
            winner_text = letra.render("GAME OVER: Blue snake ha ganado!", True, BLUE)
            winner_rect = winner_text.get_rect()
            winner_rect.midtop = (pantalla_width//2, pantalla_height//2)
            pantalla.blit(winner_text, winner_rect) 
     
        pygame.display.flip() #Actualiza la pantalla
        time.sleep(20)
        pygame.quit() #Como ha habido 'game over', se cierra el programa
        quit()
   
    def refresh(self,pantalla): #Para actualizar la pantalla del juego
    
        self.all_sprites.update()
        self.screen.blit(self.background, (0, 0)) #Ponemos un fondo 
        score = self.game.get_score()
        letra = pygame.font.SysFont('times new roman', 20) 
        text1 = letra.render('Black snake score:' + str(score[0]), True, BLACK) #Dibuja los puntos de black snake en la pantalla
        score_rect1 = text1.get_rect()
        score_rect1.midtop = (90,10)
        text2 = letra.render('Blue snake score:' + str(score[1]), True, BLUE) #Dibuja los puntos de blue snake en la pantallea
        score_rect2 = text2.get_rect()
        score_rect2.midtop = (SIZE[Y]-80,10)
     
        self.all_sprites.draw(self.screen)
        
        pantalla.blit(text1, score_rect1)
        pantalla.blit(text2, score_rect2)

        pygame.display.flip() #Actualiza la pantalla completa
        
        
    def tick(self):
        self.clock.tick(FPS) #FPS = 60, ya definidio previamente

        self.game_over = Value('i', 0) # Estado de game over inicial.
        
    def pantalla_inicio(self):
        pantalla_width = self.screen.get_width()
        pantalla_height = self.screen.get_height()
        letra = pygame.font.SysFont('times new roman', 50)
        sigue_en_intro = True
        while sigue_en_intro:
    	   
          for evento in pygame.event.get():
             if evento.type == pygame.QUIT:
                quit()
    	   
          self.screen.blit(self.inicio, (0,0))
          titulo = letra.render("BIENVENIDO A SNAKE GAME", True, RED)
          instrucciones = letra.render('Presione ENTER para continuar', True, RED)
          self.screen.blit(titulo, (pantalla_width//2 - titulo.get_width()//2, 20))
          self.screen.blit(instrucciones, (pantalla_width//2 - instrucciones.get_width()//2, 400))
          key = pygame.key.get_pressed()
    	   
          if key[pygame.K_RETURN]:
              sigue_en_intro = False
          
          pygame.display.update()
    	       

    @staticmethod
    def quit():
        pygame.quit()

def main(ip_address):
    try:
        with Client((ip_address, 6112), authkey=b'secret password') as conn:
            
            game = Game()
            color,gameinfo = conn.recv()
            
            pantalla = pygame.display.set_mode((SIZE[X], SIZE[Y]))
            
            pygame.display.set_caption("SNAKE GAME")
            pygame.display.set_icon(pygame.image.load('icono.png'))
            print(f"I am playing {color}")
            print(f'c1 {gameinfo}')
            game.update(gameinfo)
            display = Display(game)
            
            display.pantalla_inicio()
            #Bucle principal
            while game.is_running(): 
                
                pantalla.fill(BLACK)
                events = display.analyze_events(color)
                for ev in events:
                    conn.send(ev)
                    if ev == "quit":
                        game.stop()

                conn.send("next")
                gameinfo = conn.recv()
                game.update(gameinfo)
                 
                # ¿ Ha terminado la partida ? 
                if game.game_over == 1:
                    display.finDelJuego(1, pantalla)
                    game.stop()
                elif game.game_over == 2:
                    display.finDelJuego(2, pantalla)
                    game.stop() 
    
                    
                #Actualizo la pantalla y muestro las puntuaciones (refresh):
                display.refresh(pantalla)
               
                display.tick()
                pygame.display.update()

    except:
        traceback.print_exc()
        
    finally:
        pygame.quit()
        quit() #Para asegurar que el programa se cierra por completo

if __name__=="__main__":
    ip_address = "127.0.0.1" 
    if len(sys.argv)>1:
        ip_address = sys.argv[1]
    main(ip_address)
