"""
FUNCIONES POR SI LUEGO NOS HACEN FALTA
"""

"""
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
"""
"""
Esto estaba en Juego_snake_player: en la fucnión finDelJuego(), pero es que en 
refresh() ya representamos los puntos de las serpientes por pantalla:

        #Representación puntuación black snake
        gameOver_surface = ('Black snake score:' + str(self.score[0]), True, GREEN)
        gameOver_rect1 = gameOver_surface.get_rect()
        gameOver_rect1.midtop = (pantalla[X]//2, pantalla[Y]//6)
        pantalla.blit(gameOver_surface, gameOver_rect1)
        
        #Representación jugador blue snake
        gameOver_surface2 = letra.render('Blue snake score:' + str(self.score[1]), True, BLUE)
        gameOver_rect2 = gameOver_surface2.get_rect()
        gameOver_rect2.midtop = (pantalla[X]//2, pantalla[Y]//3)
        pantalla.blit(gameOver_surface2, gameOver_rect2)
""" 