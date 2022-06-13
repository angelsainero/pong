import pygame
import time

ALTO_PALETA = 40
ANCHO_PALETA = 5


"""
  - algo de herencia:

  - color, ancho, alto
  - hay cosas fijas como el color y el tamaño

  - método moverse: solo hacia arriba y hacia abajo
  - método de chocar: límite para no salirse de la pantalla

  - método para interactuar con la pelota???
"""

class Paleta(pygame.Rect):

    ARRIBA = True
    ABAJO = False

    def __init__(self, x, y):
        super(Paleta, self).__init__(x, y, ANCHO_PALETA, ALTO_PALETA)
        self.velocidad = 5

    def muevete(self, direccion):
        if direccion == self.ARRIBA:
            print("Muevete hacia arriba")
        else:
            print("Muevete hacia abajo")

            
'''
el movimiento es cosa de la paleta
aumentar o disminuir el valor del eje y (posición de la paleta)
quien tiene que capturar el evento es el bucle principal 


'''

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
            (self._ALTO-ALTO_PALETA)/2  # coordenada y (top)
        )    
        self.jugador2 = Paleta(
            self._ANCHO-self._MARGEN_LATERAL-self._ANCHO_PALETA,
            (self._ALTO-ALTO_PALETA)/2
        )

    def bucle_principal(self):
        print("Estoy en el bucle principal")
        salir = False
        while not salir:
            for evento in pygame.event.get():
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        print("Adiós, te has escapado")
                        salir = True
                    elif evento.key == pygame.K_a:
                        self.jugador1.muevete(Paleta.ARRIBA)
                    elif evento.key == pygame.K_z:
                        self.jugador1.muevete(Paleta.ABAJO)
                    elif evento.key == pygame.K_UP:
                        self.jugador2.muevete(Paleta.ARRIBA)
                    elif evento.key == pygame.K_DOWN:
                        self.jugador2.muevete(Paleta.ABAJO)

                if evento.type == pygame.QUIT:
                    salir = True

            pygame.draw.line(self.pantalla,(255,255,255),(self._ANCHO/2,0),(self._ANCHO/2, self._ALTO), 2)
            pygame.draw.rect(self.pantalla, (255, 255, 255), self.jugador1)
            pygame.draw.rect(self.pantalla, (255, 255, 255), self.jugador2)
            pygame.display.flip()


if __name__ == "__main__":
    juego = Pong()
    juego.bucle_principal()