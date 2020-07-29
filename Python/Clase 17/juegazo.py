"""
Documentacion del Juego
"""
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
            self.camina_izquierda.append(pygame.image.load("img/"+fuente+"/L"+str(x)+".png"))
            self.camina_derecha.append(pygame.image.load("img/"+fuente+"/R"+str(x)+".png"))

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
                cuadro.blit(self.quieto, (self.x, self.y))
            
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

    def se_mueve_segun(self, t, iz, de, ar, ab, sa):
        if t[iz] and self.x > self.velocidad:
            self.va_izquierda = True
            self.va_derecha = False
            self.x -= self.velocidad
        
        elif t[de] and self.x < ANCHO_VENTANA - self.ancho - self.velocidad:
            self.x += self.velocidad
            self.va_derecha = True
            self.va_izquierda = False
        else:
            self.va_izquierda = False
            self.va_derecha = False
            self.contador_pasos = 0

        if self.ha_saltado: # accion de saltar
            if self.impulso_salto >= -10:
                if self.impulso_salto < 0:
                    self.y -= int((self.impulso_salto**2) * 0.5 * -1)
                else:
                    self.y -= int((self.impulso_salto**2) * 0.5)
                self.impulso_salto -= 1
            else:
                self.ha_saltado = False
                self.impulso_salto = 10
        else:
            if t[ar] and self.y > self.velocidad:
                self.y -= self.velocidad
            if t[ab] and self.y < ALTO_VENTANA - self.alto - self.velocidad:
                self.y += self.velocidad

            if t[sa]:
                self.ha_saltado = True
                self.va_derecha = False
                self.va_izquierda = False
                self.contador_pasos = 0

    def se_mueve_solo(self, nivel):
        if self.velocidad > 0:
            if self.x + self.velocidad < self.camino[1]: # dentro del rango del camino predefinido
                self.x += self.velocidad * nivel
                self.va_derecha = True
                self.va_izquierda = False
            else:
                self.velocidad *= -1
                self.contador_pasos = 0
        else:
            if self.x - self.velocidad > self.camino[0]: # dentro del rango del camino
                self.x += self.velocidad * nivel
                self.va_izquierda = True
                self.va_derecha = False
            else:
                self.velocidad *= -1
                self.contador_pasos = 0

    def se_encuentra_con(self, alguien):
        R1_ab = self.zona_impacto[1] + self.zona_impacto[3] # posicion de y+alto
        R1_ar = self.zona_impacto[1] # posicion y
        R1_iz = self.zona_impacto[0] # posicion x
        R1_de = self.zona_impacto[0] + self.zona_impacto[2] # posicion x+ancho

        R2_ab = alguien.zona_impacto[1] + alguien.zona_impacto[3] # posicion de y+alto
        R2_ar = alguien.zona_impacto[1] # posicion y
        R2_iz = alguien.zona_impacto[0] # posicion x
        R2_de = alguien.zona_impacto[0] + alguien.zona_impacto[2] # posicion x+ancho

        return R1_de > R2_iz and R1_iz < R2_de and R1_ar < R2_ab and R1_ab > R2_ar

    def es_golpeado(self):
        self.ha_saltado = False
        self.va_derecha = False
        self.va_izquierda = False
        self.impulso_salto = 10
        self.contador_pasos = 0
        self.x = 100
        self.y = 410
        self.salud -= 5
        pygame.time.delay(2000)


class proyectil(object):
    def __init__(self, x, y, radio, color, direccion):
        self.x = x
        self.y = y
        self.radio = radio
        self.color = color
        self.direccion = direccion
        self.velocidad = 8 * direccion
        self.zona_impacto = (self.x - self.radio, self.y - self.radio, self.radio * 2, self.radio * 2)

    def dibujar(self, cuadro):
        self.zona_impacto = (self.x - self.radio, self.y - self.radio, self.radio * 2, self.radio * 2)
        pygame.draw.circle(cuadro, self.color, (self.x, self.y), self.radio)
        pygame.draw.rect(cuadro, (255, 0, 0), self.zona_impacto, 2)

    def impacta_a(self, alguien):
        if alguien.salud > 0:
            alguien.salud -= 1
        else:
            alguien.es_invisible = False
            del(alguien)


def subir_nivel():
    global nivel
    global nivel_maximo
    global heroe
    global villano
    global musica_fondo
    global ventana
    global esta_jugando
    global gana

    nivel += 1

    texto = pygame.font.SysFont('comicsans', 100)
    marcador = texto.render("GANASTE!", 1, (255, 0, 0))
    ventana.blit(marcador, (marcador.get_width()//2, 200))
    pygame.display.update()
    pygame.time.delay(2000)

    if nivel > nivel_maximo:
        pygame.mixer.music.stop()
        gana = True
        esta_jugando = False
    else:
        villano = villanos[nivel]
        pygame.mixer.music.stop()
        musica_fondo = pygame.mixer.music.load(ruta_musica[nivel])
        pygame.mixer.music.play(-1)

def repitar_cuadro_juego():

    if nivel <= nivel_maximo:
        ventana.blit(imagen_fondo[nivel], (0,0))
    else:
        ventana.fill((0,0,0))
    heroe.dibujar(ventana)
    villano.dibujar(ventana)
    for bala in balas:
        bala.dibujar(ventana)
    pygame.display.update()

# Dentro del Ciclo principal
repetir = True

while repetir:

    nivel = 0
    nivel_maximo = 3
    gana = False

    heroe = personaje(ANCHO_VENTANA//2, ALTO_VENTANA//2, "heroe", ANCHO_VENTANA)
    villanos = [personaje(10, ALTO_VENTANA//2, "villano", 800), personaje(10, ALTO_VENTANA//2, "villano", 800), personaje(10, ALTO_VENTANA//2, "villano", 800), personaje(10, ALTO_VENTANA//2, "villano", 800)]
    villano = villanos[nivel]

    imagen_fondo = [pygame.image.load('img/bg0.jpg'), pygame.image.load('img/bg.jpg'),pygame.image.load('img/bg1.jpg'), pygame.image.load('img/bg2.jpg')]
    ruta_musica = ["snd/dubstep.mp3","snd/moose.mp3","snd/evolution.mp3","snd/epic.mp3"]
    musica_fondo = pygame.mixer.music.load(ruta_musica[nivel])
    pygame.mixer.music.play(-1) # entero -> cantidad de veces que se puede repetir la musica, si es -1 es repetir infinitamente
    pygame.mixer.music.set_volume(0.1)

    balas = []
    direccion = 0 # 1 se mueve a la derecha -> -1 se mueve a la izquierda -> 0 no se mueve
    tanda_disparos = 0
    tiempo_entre_disparo = 0
    sonido_disparo = pygame.mixer.Sound("snd/bullet.wav")
    sonido_impacto = pygame.mixer.Sound("snd/hit.wav")

    """
    Ciclo de Introduccion
    """
    texto_intro = pygame.font.SysFont('console', 30, True)
    personaje_intro = personaje(50, 150, "heroe", 700)
    esta_en_intro = True
    while esta_en_intro:
        reloj.tick(27)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()

        ventana.fill((0,0,0))
        titulo = texto_intro.render("EL JUEGAZO", 1, (255, 0, 0))
        instrucciones = texto_intro.render("Presione ENTER para comenzar el Juegazo...", 1, (255,255,255))
        personaje_intro.se_mueve_solo(2)

        ventana.blit(titulo, ((ANCHO_VENTANA//2) - titulo.get_width()//2, 10))
        ventana.blit(instrucciones, ((ANCHO_VENTANA//2) - instrucciones.get_width()//2, 300))

        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_RETURN]:
            esta_en_intro = False
            esta_jugando = True
        
        personaje_intro.dibujar(ventana)
        pygame.display.update()

    """
    Ciclo del Juego
    """
    while esta_jugando:
        reloj.tick(27)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()

        teclas = pygame.key.get_pressed()
        heroe.se_mueve_segun(teclas, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_SPACE)
        #villano.se_mueve_segun(teclas, pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_x)
        villano.se_mueve_solo(nivel)

        if villano.se_encuentra_con(heroe):
            heroe.es_golpeado()

        #Manejo de los disparos
        if tanda_disparos > 0:
            tanda_disparos += 1
        if tanda_disparos > 3:
            tanda_disparos = 0
        
        # manejo del tiempo entre disparos
        tiempo_entre_disparo += 1
        if tiempo_entre_disparo > 1:
            tiempo_entre_disparo = 0

        if teclas[pygame.K_x] and tanda_disparos == 0 and tiempo_entre_disparo == 0:
            if heroe.va_izquierda:
                direccion = -1
            elif heroe.va_derecha:
                direccion = 1
            else:
                direccion = 0
            
            if len(balas) < 5 and direccion != 0:
                balas.append(proyectil(round(heroe.x + heroe.ancho//2), round(heroe.y + heroe.alto//2), 10, (0, 0, 0), direccion))
                sonido_disparo.play()
                #print(len(balas))

        for bala in balas:
            if villano.se_encuentra_con(bala):
                bala.impacta_a(villano)
                balas.pop(balas.index(bala))
                sonido_impacto.play()

            # Movimiento del proyectil (cada proyectil)
            if bala.x < ANCHO_VENTANA and bala.x > 0:
                bala.x += bala.velocidad
            else:
                balas.pop(balas.index(bala))

        # COnsultar si se sube de nivel o se pierde
        if villano.salud <= 0:
            subir_nivel()

        if heroe.salud <= 0:
            esta_jugando = False
            repetir = False

        repitar_cuadro_juego()
pygame.quit()