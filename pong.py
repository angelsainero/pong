from random import randint

import pygame


ALTO_PALETA = 40
ANCHO_PALETA = 5
VELOCIDAD_PALA = 5

ANCHO = 640
ALTO = 480
MARGEN_LATERAL = 40

TAMANYO_PELOTA = 6
VEL_MAX_PELOTA = 5

C_NEGRO = (0, 0, 0)
C_BLANCO = (255, 255, 255)

FPS = 30

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
        self.velocidad = VELOCIDAD_PALA

    def muevete(self, direccion):
        if direccion == self.ARRIBA:
            self.y = self.y - self.velocidad
            if self.y < 0:
                self.y = 0
        else:
            self.y = self.y + self.velocidad
            if self.y > ALTO - ALTO_PALETA:
                self.y = ALTO - ALTO_PALETA

class Pelota(pygame.Rect):
    def __init__(self):
        super(Pelota, self).__init__(
            (ANCHO-TAMANYO_PELOTA)/2, (ALTO-TAMANYO_PELOTA)/2,
            TAMANYO_PELOTA, TAMANYO_PELOTA
        )
        self.velocidad_x = randint(-VEL_MAX_PELOTA, VEL_MAX_PELOTA)
        self.velocidad_y = randint(-VEL_MAX_PELOTA, VEL_MAX_PELOTA)

    def muevete(self):
        self.x = self.x + self.velocidad_x
        self.y = self.y + self.velocidad_y
        if self.y < 0:
            self.y = 0
            self.velocidad_y = -self.velocidad_y
        if self.y > ALTO-TAMANYO_PELOTA:
            self.y = ALTO-TAMANYO_PELOTA
            self.velocidad_y = -self.velocidad_y

"""
el movimiento es cosa de la paleta
    aumentar o disminuir el valor del eje y (posición de la paleta)
quien tiene que capturar el evento de pulsar la tecla es el bucle principal
redibujar la paleta cada vez
"""


class Pong:

    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        self.clock = pygame.time.Clock()

        self.jugador1 = Paleta(
            MARGEN_LATERAL,               # coordenada x (left)
            (ALTO-ALTO_PALETA)/2)         # coordenada y (top)

        self.jugador2 = Paleta(
            ANCHO-MARGEN_LATERAL-ANCHO_PALETA,
            (ALTO-ALTO_PALETA)/2)

        self.pelota = Pelota()

    def bucle_principal(self):
        salir = False
        while not salir:
            for evento in pygame.event.get():
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        print("Adiós, te has escapado")
                        salir = True
                if evento.type == pygame.QUIT:
                    salir = True

            estado_teclas = pygame.key.get_pressed()
            if estado_teclas[pygame.K_a]:
                self.jugador1.muevete(Paleta.ARRIBA)
            if estado_teclas[pygame.K_z]:
                self.jugador1.muevete(Paleta.ABAJO)
            if estado_teclas[pygame.K_UP]:
                self.jugador2.muevete(Paleta.ARRIBA)
            if estado_teclas[pygame.K_DOWN]:
                self.jugador2.muevete(Paleta.ABAJO)
            self.pelota.muevete()

            self.colision_paletas()

            self.pantalla.fill(C_NEGRO)
            pygame.draw.line(self.pantalla, C_BLANCO, (ANCHO/2, 0), (ANCHO/2, ALTO))
            pygame.draw.rect(self.pantalla, C_BLANCO, self.jugador1)
            pygame.draw.rect(self.pantalla, C_BLANCO, self.jugador2)
            pygame.draw.rect(self.pantalla, C_BLANCO, self.pelota)

            # refresco de pantalla
            pygame.display.flip()
            self.clock.tick(FPS)

    def colision_paletas(self):
        """
        Comprueba si la pelota ha colisionado con una de las paletas
        y le cambia la dirección. (pygame.Rect.colliderect(Rect))
        """
        # if self.pelota.colliderect(self.jugador1) or self.pelota.colliderect(self.jugador2):
        # if self.jugador1.colliderect(self.pelota) or self.pelota.colliderect(self.jugador2):
        if pygame.Rect.colliderect(self.pelota, self.jugador1) or pygame.Rect.colliderect(self.pelota, self.jugador2):
            self.pelota.velocidad_x = -self.pelota.velocidad_x
            self.pelota.velocidad_y = randint(-VEL_MAX_PELOTA, VEL_MAX_PELOTA)



if __name__ == "__main__":
    juego = Pong()
    juego.bucle_principal()