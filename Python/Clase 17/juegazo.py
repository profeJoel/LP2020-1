import pygame
from pygame.locals import *

pygame.init()

ANCHO_VENTANA = 850
ALTO_VENTANA = 480
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("EL JUEGAZO DE LP")
reloj = pygame.time.Clock()

# Seccion del personaje
class personaje(object):
    def __init__(self, x, y, fuente, limite):
        self.x = x
        self.y = y
        self.velocidad = 5
        # variables de movimiento
        self.ha_saltado = False
        self.va_izquierda = False
        self.va_derecha = False
        self.contador_pasos = 0
        self.impulso_salto = 10
        self.camino = [self.x, limite]
        self.salud = 10
        self.es_visible = True
        # jugabilidad
        self.zona_impacto = (self.x+15, self.y+10, 30, 50) # ajuste al cuerpo del personaje
        self.camina_izquierda = []
        self.camina_derecha = []
        self.quieto = pygame.image.load("img/"+fuente+"/standing.png")
        self.ancho = self.quieto.get_width()
        self.alto = self.quieto.get_height()
        for x in range(1,10):
            self.camina_izquierda.append(pygame.image.load("img/"+fuente+"/L"+x+".png"))
            self.camina_derecha.append(pygame.image.load("img/"+fuente+"/R"+x+".png"))

    def dibujar(self, cuadro): #cuadro es la ventana en donde se juega

        if self.contador_pasos + 1 > 27:
            self.contador_pasos = 0

        if self.es_visible:
            if self.va_izquierda:
                cuadro.blit(self.camina_izquierda[self.contador_pasos//3], (self.x, self.y))
                self.contador_pasos += 1

            elif self.va_derecha:
                cuadro.blit(self.camina_derecha[self.contador_pasos//3], (self.x, self.y))
                self.contador_pasos += 1

            else:
                cuadro.blit(self.quieto, (self.x,self.y))
            
            self.zona_impacto = (self.x+15, self.y+10, 30, 50)
            #crear la barra de vida
            pygame.draw.rect(cuadro, (255,0,0), (self.zona_impacto[0], self.zona_impacto[1] - 20, 50, 10))
            pygame.draw.rect(cuadro, (0,128,0), (self.zona_impacto[0], self.zona_impacto[1] - 20, 50 - (5 * (10 - self.salud)), 10)) # 45, 245, 0

            pygame.draw.rect(cuadro, (255,0,0), self.zona_impacto, 2)
        
        else:
            if self.zona_impacto[0] != -1:
                texto = pygame.font.SysFont('comicsans', 100)
                marcador = texto.render("GANASTE!", 1, (255,0,0))
                cuadro.blit(marcador, (250 - (marcador.get_width()//2), 200))
                pygame.display.update()
                pygame.time.delay(2000)
            self.zona_impacto = (-1,-1,-1,-1)


# Dentro del Ciclo principal
repetir = True

while repetir:

    esta_jugando = True

    while esta_jugando:
        reloj.tick(27)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()


pygame.quit()