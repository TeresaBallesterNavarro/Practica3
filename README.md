# Practica3
En esta práctica realizamos un programa que consiste en el juego multiusuario de 'Snake', en concreto para dos usuarios. Es un programa que tiene información distribuida y esta se comparte entre los clientes.

FUNCIONAMIENTO DEL JUEGO:
El juego clásico de 'Snake' consiste en que un jugador controla la serpiente con el teclado y trata de comerse el máximo número de manzanas posibles con dos condiciones:
1. La serpiente no puede tocar las parades de la pantalla.
2. Una vez el jugador ha decidido mover a la serpiente hacia arriba, no puede moverse hacia abajo en el siguiente movimiento y viceversa. Análogamente cuando el jugador mueve la serpiente hacia la derecha, el siguiente movimiento no puede ser a la izquierda y viceversa.

El juego de 'Snake' multijugador que proponemos consiste en que aquel jugador que consiga comer antes 20 manzanas, gana. Siempre y cuando se cumplan las dos condiciones anteriores del juego clásico de 'Snake'. En el caso de que uno de los jugadores toque la pared de la pantalla, este ha perdido. Si ambos jugadores se salen de la pantalla, han perdido los dos. Sin embargo, la segunda condición del juego simplemente restringe los movimientos de los jugadores, pero no los descalifica.

SCRIPTS :
- 'Snake_sala.py' -->  El script de la sala es responsable de coordinar y administrar la lógica del juego en general.
- 'Snake_player.py' -->  El script del jugador se encarga de manejar las acciones y eventos específicos de un jugador individual. Definimos las siguientes clases:
    - Snake : representa la serpiente en el juego.
    - Apple : representa la manzana en el juego.
    - Game : representa el estado del juego.
    - SnakeSprite : representa las snakes por pantalla.
    - AppleSprite : representa la manzana por pantalla.
    - Display : representa el juego por pantalla
En ambos hacemos uso de la librería pygame y multiporcessing de Python. Además, ambos códigos están comentados.

¿ CÓMO EMPEZAR A JUGAR ? :
Hay dos scripts : 'snake_sala.py' y 'snake_player.py', ambos necesarios para ejecutar el juego de manera distribuida. Para que dos jugadores puedan jugar, es necesario que se abra desde uno de los ordenadores el scrip de snake_sala y, a continuación, que cada jugador abra desde su ordenador snake_play pero siempre con la misma dirección ip.

Nota: Las imágenes .png son necesarias para representar correctamente el juego por pantalla.

### AMPLIACIÓN ###
Una vez finalizamos el juego de la snake, intentamos hacer otra versión de la snake en la que el cuerpo fuese aumentando a medida que la snake comiese manzanas.  
El problema de esta nueva versión es que no conseguimos que nos funcione correctamente y no conseguimos ver el/los error/es que estamos cometiendo.
Los archivos asociados a esta nueva versión son :
         - snake_sala2.py
         - snake_player2.py
