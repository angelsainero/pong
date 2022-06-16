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

FPS = 60

PUNTOS_PARTIDA = 3

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

        # velocidad_x_valor_valido = False
        # while not velocidad_x_valor_valido:
        #     self.velocidad_x = randint(-VEL_MAX_PELOTA, VEL_MAX_PELOTA)
        #     velocidad_x_valor_valido = self.velocidad_x != 0

        self.velocidad_x = 0
        while self.velocidad_x == 0:
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


class Marcador:
    """
    - ¿qué?    guardar números, pintar
    - ¿dónde?  ------
    - ¿cómo?   ------
    - ¿cuándo? cuando la pelota sale del campo


    letra_marcador

    """

    def __init__(self):
        self.letra_marcador = pygame.font.SysFont('roboto', 100)
        self.letra_mensaje = pygame.font.SysFont('roboto', 40)
        self.inicializar()

    def comprobar_ganador(self):
        if self.partida_finalizada:
            return True
        if self.valor[0] == PUNTOS_PARTIDA:
            self.mensaje_ganador = "Ha ganado el jugador 1"
            self.partida_finalizada = True
        elif self.valor[1] == PUNTOS_PARTIDA:
            self.mensaje_ganador = "Ha ganado el jugador 2"
            self.partida_finalizada = True
        return self.partida_finalizada

    def inicializar(self):
        self.valor = [0, 0]
        self.partida_finalizada = False

    def pintar(self, pantalla):
        texto = pygame.font.Font.render(self.letra_marcador, str(self.valor[0]), False, C_BLANCO)
        pos_x =  (ANCHO/2 - MARGEN_LATERAL - ANCHO_PALETA)/2 - texto.get_width()/2 + MARGEN_LATERAL + ANCHO_PALETA
        pos_y =  MARGEN_LATERAL
        pygame.Surface.blit(pantalla, texto, (pos_x, pos_y))

        texto = pygame.font.Font.render(self.letra_marcador, str(self.valor[1]), False, C_BLANCO)
        pos_x =  (ANCHO/2 - MARGEN_LATERAL - ANCHO_PALETA)/2 - texto.get_width()/2 + ANCHO/2
        pos_y =  MARGEN_LATERAL
        pygame.Surface.blit(pantalla, texto, (pos_x, pos_y))

        if self.partida_finalizada:
            texto = pygame.font.Font.render(self.letra_mensaje, self.mensaje_ganador, False, C_BLANCO)
            pos_x =  ANCHO/2 - texto.get_width()/2
            pos_y =  ALTO/2 - texto.get_height()/2 - MARGEN_LATERAL
            pygame.Surface.blit(pantalla, texto, (pos_x, pos_y))


class Pong:

    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        self.clock = pygame.time.Clock()

        # Vamos a prepararnos para pintar texto
        pygame.font.init()

        self.jugador1 = Paleta(
            MARGEN_LATERAL,               # coordenada x (left)
            (ALTO-ALTO_PALETA)/2)         # coordenada y (top)

        self.jugador2 = Paleta(
            ANCHO-MARGEN_LATERAL-ANCHO_PALETA,
            (ALTO-ALTO_PALETA)/2)

        self.pelota = Pelota()
        self.marcador = Marcador()

    def bucle_principal(self):
        salir = False
        while not salir:
            for evento in pygame.event.get():
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        print("Adiós, te has escapado")
                        salir = True
                    if evento.key == pygame.K_r:
                        print("Iniciamos nueva partida")
                        self.marcador.inicializar()
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

            if not self.marcador.comprobar_ganador():
                self.pelota.muevete()
                self.colision_paletas()
                self.comprobar_punto()

            self.pantalla.fill(C_NEGRO)
            pygame.draw.line(self.pantalla, C_BLANCO, (ANCHO/2, 0), (ANCHO/2, ALTO))
            pygame.draw.rect(self.pantalla, C_BLANCO, self.jugador1)
            pygame.draw.rect(self.pantalla, C_BLANCO, self.jugador2)
            pygame.draw.rect(self.pantalla, C_BLANCO, self.pelota)
            self.marcador.pintar(self.pantalla)

            # refresco de pantalla
            pygame.display.flip()
            self.clock.tick(FPS)

    def colision_paletas(self):
        """
        Comprueba si la pelota ha colisionado con una de las paletas
        y le cambia la dirección. (pygame.Rect.colliderect(Rect))
        """
        if pygame.Rect.colliderect(self.pelota, self.jugador1) or pygame.Rect.colliderect(self.pelota, self.jugador2):
            self.pelota.velocidad_x = -self.pelota.velocidad_x
            self.pelota.velocidad_y = randint(-VEL_MAX_PELOTA, VEL_MAX_PELOTA)

    def comprobar_punto(self):
        if self.pelota.x < 0:
            self.marcador.valor[1] = self.marcador.valor[1] + 1
            print(f"El nuevo marcador es {self.marcador.valor}")
            self.pelota.velocidad_x = randint(-VEL_MAX_PELOTA, -1)
            self.iniciar_punto()
        elif self.pelota.x > ANCHO:
            self.marcador.valor[0] = self.marcador.valor[0] + 1
            print(f"El nuevo marcador es {self.marcador.valor}")
            self.pelota.velocidad_x = randint(1, VEL_MAX_PELOTA)
            self.iniciar_punto()

    def iniciar_punto(self):
        self.pelota.x = (ANCHO - TAMANYO_PELOTA)/2
        self.pelota.y = (ALTO - TAMANYO_PELOTA)/2
        self.pelota.velocidad_y = randint(-VEL_MAX_PELOTA, VEL_MAX_PELOTA)



if __name__ == "__main__":
    juego = Pong()
    juego.bucle_principal()