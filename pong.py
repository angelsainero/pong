import pygame
import time

"""
  - algo de herencia:

  - color, ancho, alto
  - hay cosas fijas como el color y el tamaño

  - método moverse: solo hacia arriba y hacia abajo
  - método de chocar: límite para no salirse de la pantalla

  - método para interactuar con la pelota???
"""

class Paleta(pygame.Rect):
    pass


class Pong:

    _ANCHO = 640
    _ALTO = 480
    _MARGEN_LATERAL = 40

    _ANCHO_PALETA = 5
    _ALTO_PALETA = _ALTO / 5


    def __init__(self):
        print("Construyendo un objeto pong")
        pygame.init()
        self.pantalla = pygame.display.set_mode((self._ANCHO, self._ALTO))

        self.jugador1 = Paleta(
            self._MARGEN_LATERAL,               # coordenada x (left)
            (self._ALTO-self._ALTO_PALETA)/2,   # coordenada y (top)
            self._ANCHO_PALETA,                 # ancho (width)
            self._ALTO_PALETA)                  # alto (height)

        self.jugador2 = Paleta(
            self._ANCHO-self._MARGEN_LATERAL-self._ANCHO_PALETA,
            (self._ALTO-self._ALTO_PALETA)/2,
            self._ANCHO_PALETA,
            self._ALTO_PALETA)

    def bucle_principal(self):
        print("Estoy en el bucle principal")
        while True:
            pygame.draw.rect(self.pantalla, (255, 255, 255), self.jugador1)
            pygame.draw.rect(self.pantalla, (255, 255, 255), self.jugador2)
            pygame.display.flip()

if __name__ == "__main__":
    juego = Pong()
    juego.bucle_principal()