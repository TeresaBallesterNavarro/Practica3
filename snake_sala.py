"""
PARTICIPANTES:
Apellidos1: Ballester Navarro
Nombre1: Teresa

Apellidos2: González Morala
Nombre2: David
"""
from multiprocessing.connection import Listener
from multiprocessing import Process, Manager, Value, Lock
import traceback
import sys
import random, pygame


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0,255,0)
YELLOW = (255,255,0)

BLACK_SNAKE = 0
BLUE_SNAKE = 1
SNAKE_WIDTH = 10
SNAKE_HEIGHT = 10
SNAKES_COLORS = [BLACK, BLUE]
LEFT = "left"
RIGHT = "right"
UP = "up"
DOWN = "down"


APPLE_COLOR = RED
APPLE_SIZE = 10
SIZE = (800,650)
X = 0
Y = 1  
FPS = 60

class Snake(): 

    def __init__(self, color): #El color diferencia al jugador 1 del 2
        self.color = color

        if self.color == BLACK_SNAKE :
            self.head = [100,300]
            self.direction = RIGHT   #Defino una dirección inicial para black_snake
                
        else : #BLUE_SNAKE = 1
            self.head = [SIZE[X] -100, SIZE[Y] - 300]
            self.direction = LEFT       #Defino una dirección inicial para blue_snake
        
        self.change = self.direction
            
    def get_color(self):
        return self.color
    
    def get_pos_head(self):
        return self.head
    
    def set_pos_head(self,head):
        self.head = head
        
    def get_direction(self):
        return self.direction
    
    def set_direction(self, direction): 
        self.direction = direction
       
    def change_direction(self, direction): #Cambio de dirección
        self.change = direction
        #No podemos cambiar dirección de arriba a abajo, primero hay que moverse hacia uno de los lados
        if self.change == UP and self.direction != DOWN:
            self.direction = UP 
        elif self.change == DOWN and self.direction != UP:
            self.direction = DOWN
       #Igual que antes, no podemos cambiar el sentido directamente dentro de la misma dirección
        if self.change == LEFT and self.direction != RIGHT:
            self.direction = LEFT 
        elif self.change == RIGHT and self.direction !=LEFT:
            self.direction = RIGHT
    
    def moveUp(self):
        	self.head[Y] -= 50

    def moveDown(self):
        	self.head[Y] += 50
    
    def moveRight(self):
        	self.head[X] += 50
    
    def moveLeft(self):
           self.head[X] -= 50
     
    def __str__(self):
        return f"S<{SNAKES_COLORS[self.color], self.head}>"
        

class Apple(): #Representa la manzana en el juego

    def __init__(self): #La manzana tiene color y posición
        self.pos = [None, None]
        x3 = random.randint(1, 10)*50 
        y3 = random.randint(1, 10)*50
        self.pos = [x3, y3]
        snake1 = Snake(BLACK_SNAKE)
        snake2 = Snake(BLUE_SNAKE)
        while snake1.get_pos_head() == self.pos or snake2.get_pos_head() == self.pos : #mientras se de el caso en que la manzana aparezca en la misma posición que una de las 2 snakes
              x3, y3 = random.randint(1, 16)*50, random.randint(1, 13)*50 #actualizamos pos de la manzana
    
    def get_pos(self):
        return self.pos
    
    def set_pos(self, pos):
        self.pos = pos

    def __str__(self):
        return f"A<{self.pos}>"

class Game(): #Representamos el estado del juego

    def __init__(self, manager):   
        self.snakes = manager.list([Snake(i) for i in range(2)])
        self.apple = manager.list([ Apple() ]) 
        self.score = manager.list( [0,0] )
        self.game_over = Value('i', 0) # Estado de game over inicial. 0 = No hay game over. 1 = Gana snake BLACK. 2 = Gana snake BLUE.
        self.running = Value('i', 1) # 1 = running
        self.lock = Lock()

    def get_snake(self, color):
        return self.snakes[color]
        
    def get_pos_snake(self, color):
        return self.snakes[color].get_pos_head()
        
    def set_pos_snake(self, color, pos):
        self.snakes[color].set_pos_head(pos)
        
    def get_snake_direction(self, color):
        return self.snakes[color].get_direction()
        
    def set_snake_direction(self, color, direction):
        self.snakes[color].set_direction(direction)

    def get_apple_pos(self):
        return self.apple[0].get_pos()
    
    def set_pos_apple(self, pos):
        self.apple.set_pos(pos)

    def get_score(self,color):
        return self.score[color]
    
    def set_score(self, color):
        self.score[color] += 1
        
    def is_running(self):
        return self.running.value == 1
    
    def get_game_over(self):
        return self.game_over.value

    def set_game_over(self, i): #Cambia el estado de gameover (partida acabada o no)
        self.game_over.value = i
    
    def stop(self):
        self.running.value = 0

    
    def change_dir(self, color, key): #Snake cambia de dirección
        self.lock.acquire()
        p = self.snakes[color]
        p.change_direction(key)
        self.snakes[color] = p
        self.lock.release()
     
    
    def move(self, color, key):
        self.lock.acquire()
        p = self.snakes[color]
        
        if key == UP:
           p.moveUp()
        if key == DOWN:
           p.moveDown()
        if key == LEFT:
           p.moveLeft()
        if key == RIGHT:
           p.moveRight()
            
        self.snakes[color] = p
        self.lock.release()
        
         
    def get_info(self):
        info = {
            'pos_black_snake': self.snakes[0].get_pos_head(),
            'pos_blue_snake': self.snakes[1].get_pos_head(),
            'pos_apple': self.apple[0].get_pos(),
            'score': list(self.score),
            'game_over': self.game_over.value,
            'is_running': self.running.value == 1
        }
        return info
    
    def __str__(self):
        return f"G<{self.snakes[BLACK_SNAKE]}:{self.snakes[BLUE_SNAKE]}:{self.apple[0]}>"
    
def pararPartida(game):  #### Condiciones para parar la partida ####
   
    pos_BlackSnake = game.get_pos_snake(BLACK_SNAKE)
    pos_BlueSnake = game.get_pos_snake(BLUE_SNAKE)
     
    # 1. Alguno alcanza la puntuación máxima
    if game.score[0] == 20:
        game.set_game_over(1) #Ha ganado black_snake
          
    elif game.score[1] == 20:
         game.set_game_over(2) #Ha ganado blue_snake
          
    # 3. Ambos jugadores se salen de la pantalla -> Empate, los 2 han perdido
    elif ((pos_BlackSnake[0] < 0 or pos_BlackSnake[0] > SIZE[X]\
          or pos_BlackSnake[1] < 0 or pos_BlackSnake[1] > SIZE[Y]))\
        and ((pos_BlueSnake[0] < 0 or pos_BlueSnake[0] > SIZE[X]\
              or pos_BlueSnake[1] < 0 or pos_BlueSnake[1] > SIZE[Y])):
            
            game.set_game_over(3)
         
    # 4. La snake BLACK se sale de la pantalla -> Gana BLUE snake
    elif pos_BlackSnake[0] < 0 or pos_BlackSnake[0] > SIZE[X] or\
        pos_BlackSnake[1] < 0 or pos_BlackSnake[1] > SIZE[Y]:
            
        game.set_game_over(2)
             
    # 5. La snake BLUE se sale de la pantalla -> Gana BLACK snake
    elif pos_BlueSnake[0] < 0 or pos_BlueSnake[0] > SIZE[X] or\
        pos_BlueSnake[1] < 0 or pos_BlueSnake[1] > SIZE[Y]:
            
        game.set_game_over(1)
     
                 
def snake(color, conn, game): 
    
    try: 
        print(f"starting player {SNAKES_COLORS[color]}:{game.get_info()}")
        conn.send( (color, game.get_info()) )
        while game.is_running():
            
            command = ""
            direction = game.get_snake(color).get_direction()
            while command != "next":
                command = conn.recv()
                if command == UP and direction != DOWN :
                    game.change_dir(color,UP)
                    print(f"{game.get_snake_direction(color)}")
                    game.move(color,UP)
                elif command == DOWN and direction != UP:
                    game.change_dir(color,DOWN)
                    print(f"{game.get_snake_direction(color)}")
                    game.move(color,DOWN)
                elif command == RIGHT and direction != LEFT:
                    game.change_dir(color,RIGHT)
                    print(f"{game.get_snake_direction(color)}")
                    game.move(color,RIGHT)
                elif command == LEFT and direction != RIGHT:
                    game.change_dir(color, LEFT)
                    print(f"{game.get_snake_direction(color)}")
                    game.move(color,LEFT)
                elif command == "quit":
                    game.stop()
                else:
                    print("Si sale este mensaje es que se ha metido en el else")
                  
                # Aquí vemos cuando la serpiente se come la manzana
                if game.get_pos_snake(color) == game.get_apple_pos(): 
                    game.set_score(color) # Se suman los puntos
                    print(game.score)
                    game.apple[0] = Apple() # Se crea una nueva manzana aleatoria
                    
                pararPartida(game) 
                
            conn.send(game.get_info())
                
    except:
        traceback.print_exc()
        conn.close()

    finally:
        print(f"Game ended {game}")

def main(ip_address):
    manager = Manager()
    try:
        with Listener((ip_address, 6112),
                      authkey=b'secret password') as listener:
            n_snake = 0
            snakes = [None, None]
            game = Game(manager)
            while True:
                print(f"accepting connection {n_snake}")
                conn = listener.accept()
                snakes[n_snake] = Process(target=snake,
                                            args=(n_snake, conn, game))
                n_snake += 1
                if n_snake == 2:
                    snakes[0].start()
                    snakes[1].start()
                    n_snake = 0
                    snakes = [None, None]
                    game = Game(manager)

    except Exception as e:
        traceback.print_exc()
        
if __name__=="__main__":
    ip_address = "127.0.0.1" 
    if len(sys.argv)>1:
        ip_address = sys.argv[1]
    main(ip_address)
