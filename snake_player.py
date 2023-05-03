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
import sys
import time
from multiprocessing import Value



snake_speed = 15

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
        #self.change = self.direction #Hacia donde se va a dirigir en el prox movimiento
    
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
      self.image = pygame.Surface([SNAKE_WIDTH, SNAKE_HEIGHT])
      self.image.fill(BLACK)
      self.image.set_colorkey(BLACK) #drawing the snake
      self.snake = snake
      color = SNAKES_COLORS[self.snake.get_color()]
      pygame.draw.rect(self.image, color, [0, 0, SNAKE_WIDTH, SNAKE_HEIGHT]) #Dibuja sanke con su color y su tamanyo predefinidos
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
        self.image = pygame.Surface((APPLE_SIZE, APPLE_SIZE))
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.rect(self.image, APPLE_COLOR, [0, 0, APPLE_SIZE, APPLE_SIZE]) #Dibuja la manzana con su posición y color predefinido
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
            
        #if pygame.sprite.collide_rect(self.snakes[BLUE_SNAKE], self.snakes[BLACK_SNAKE]): 
        #   events.append("collide")

        return events




    def pantalla_inicio(self): 
	     self.screen.blit(self.background, (0,0))
	     letra = pygame.font.SysFont('arial', 70)
	     text = letra.render('SNAKE GAME', True, YELLOW)
	     self.screen.blit(text, (SIZE[X] // 2, SIZE[Y] // 2))
	     text = letra.render('INSTRUCTIONS:' + '\n' + '1. Gana la snake que coma más manzanas' + '\n' + '2. No puedes tocar a otro jugador ni las paredes de la pantalla'\
		 + '\n' + '3. Usa las flechas de tu teclado para desplazarte, sin poder retroceder hacia atrás', True, YELLOW)
	     self.screen.blit(text, (SIZE[X] // 2, SIZE[Y] // 2))
	     text = letra.render('Pulsa una flecha para empezar', True, YELLOW)
	     self.screen.blit(text, (SIZE[X] // 2, SIZE[Y] * 3/4))
	     pygame.display.flip()


    def finDelJuego(self, i , pantalla): #Para mostrar la pantalla cuando hay game_over
    
       # Obtengo las dimensiones de la pantalla
        pantalla_width = pantalla.get_width()
        pantalla_height = pantalla.get_height()
        
    
        self.screen.fill(BLACK) # 'pintamos' la pantalla de negro
        letra = pygame.font.SysFont('times new roman', 50)
    
        #Veamos los casos de game_over y en cada uno mostraremos una cosa por pantalla:
        if i == 1: #Gana BLACK snake
            winner_surface = letra.render("GAME OVER: Black snake ha ganado!", True, YELLOW)
            winner_rect = winner_surface.get_rect()
            winner_rect.midtop = (pantalla_width//2, pantalla_height//2)
            pantalla.blit(winner_surface, winner_rect) 
        elif i == 2: #Gana BLUE snake
            winner_surface = letra.render("GAME OVER: Blue snake ha ganado!", True, YELLOW)
            winner_rect = winner_surface.get_rect()
            winner_rect.midtop = (pantalla_width//2, pantalla_height//2)
            pantalla.blit(winner_surface, winner_rect) 
            
        elif i == 3: #Empate
            if self.score[0] > self.score[1]:
                winner_surface = letra.render("GAME OVER: Black snake ha ganado!", True, YELLOW)
                winner_rect = winner_surface.get_rect()
                winner_rect.midtop = (pantalla_width//2, pantalla_height//2)
                pantalla.blit(winner_surface, winner_rect) 
            elif self.score[0] < self.score[1]:
                winner_surface = letra.render("GAME OVER: Blue snake ha ganado!", True, YELLOW)
                winner_rect = winner_surface.get_rect()
                winner_rect.midtop = (pantalla_width//2, pantalla/_height/2)
                pantalla.blit(winner_surface, winner_rect)
            elif self.score[0] == self.score[1]:
                winner_surface = letra.render("GAME OVER: Ha habido EMPATE!", True, YELLOW)
                winner_rect = winner_surface.get_rect()
                winner_rect.midtop = (pantalla_width//2, pantalla_height//2)
                pantalla.blit(winner_surface, winner_rect)  
       
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
        #self.screen.blit(text1, (50, 10))
        text2 = letra.render('Blue snake score:' + str(score[1]), True, BLUE) #Dibuja los puntos de blue snake en la pantallea
        score_rect2 = text2.get_rect()
        score_rect2.midtop = (SIZE[Y]-80,10)
        #score_surface = pygame.Surface((800, 60))
        #score_surface.fill((255, 255, 255))
        #score_surface.blit(text, (0, 0))
        #self.screen.blit(text2, (SIZE[X]-120, 10))
        self.all_sprites.draw(self.screen)
        
        pantalla.blit(text1, score_rect1)
        pantalla.blit(text2, score_rect2)
        pygame.display.flip() #Actualiza la pantalla completa

    def tick(self):
        self.clock.tick(FPS) #FPS = 60, ya definidio previamente

    @staticmethod
    def quit():
        pygame.quit()

def main(ip_address):
    try:
        with Client((ip_address, 6000), authkey=b'secret password') as conn:
            
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
                
                #direction = game.get_snake_direction(color)
                pantalla.fill(BLACK)
                events = display.analyze_events(color)
                for ev in events:
                    conn.send(ev)
                    if ev == "quit":
                        game.stop()

                conn.send("next")
                gameinfo = conn.recv()
                game.update(gameinfo)

                #Actualizo la pantalla y muestro las puntuaciones (refresh):
                display.refresh(pantalla)
                
                # ¿ Ha terminado la partida ? 
                if game.game_over == 1:
                    display.finDelJuego(1, pantalla)
                    game.stop()
                elif game.game_over == 2:
                    display.finDelJuego(2, pantalla)
                    game.stop() 
                elif game.game_over == 3:
                    display.finDelJuego(3, pantalla)
                    game.stop()

                display.tick()
                pygame.display.update()
                #Para ver si me sale bien la snake dibujada (como un cuadrado)
                #snake = SnakeSprite()
                #snake.draw()
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
