# Practica3
En esta práctica realizamos un programa que consiste en el juego multiusuario de 'Snake', en concreto para dos usuarios. Es un programa que tiene información distribuida y esta se comparte entre los clientes.

El juego clásico de 'Snake' consiste en que un jugador controla la serpiente con el teclado y trata de comerse el máximo número de manzanas posibles con dos condiciones:
1. La serpiente no puede tocar las parades de la pantalla.
2. Una vez el jugador ha decidido mover a la serpiente hacia arriba, no puede moverse hacia abajo en el siguiente movimiento y viceversa. Análogamente cuando el jugador mueve la serpiente hacia la derecha, el siguiente movimiento no puede ser a la izquierda y viceversa.

El juego de 'Snake' multijugador que proponemos consiste en que aquel jugador que consiga comer el máximo número de manzanas posibles, en un tiempo limitado, gana. Siempre y cuando se cumplan las dos condiciones anteriores del juego clásico de 'Snake'. En el caso de que uno de los jugadores toque la pared de la pantalla, este ha perdido. Si ambos jugadores se salen de la pantalla, han perdido los dos. Sin embargo, la segunda condición del juego simplemente restringe los movimientos de los jugadores, pero no los descalifica.

